<script lang="ts">
  import { AngleRightOutline, AngleDownOutline } from "flowbite-svelte-icons";
  import { formatValue } from "../../shared/format";
  import { type SelectionMap, isStringArray } from "../../shared/types";
  import SpanIndexHighlight from "./SpanIndexHighlight.svelte";
  import SubstringHighlight from "./SubstringHighlight.svelte";
  import Regular from "./Regular.svelte";
  import type { JoinInfo } from "../../backendapi";
  import { filters, selectionDisplay, databaseConnection } from "../../stores";
  import type { DatasetInfo } from "../../backendapi";
  import type { TableClient } from "./TableClient";
  import { Spinner } from "flowbite-svelte";

  export let id: number;
  export let textData: Array<[string, unknown]>;
  export let metadata: Array<[string, unknown]>;
  export let highlight = false;
  export let datasetInfo: DatasetInfo | undefined = undefined;
  export let tableClient: TableClient | undefined = undefined;

  let toggle = false;

  function renderValue(
    value: any,
    colName: string,
    selections: SelectionMap,
    joinInfo?: JoinInfo,
    datatype?: string,
  ) {
    let highlights: string[] = [];

    if (
      joinInfo?.joinColumn.associated_text_col_name === colName &&
      joinInfo?.joinColumn.name in selections &&
      isStringArray(selections[joinInfo.joinColumn.name])
    ) {
      highlights = [
        ...highlights,
        ...(selections[joinInfo.joinColumn.name] as string[]),
      ];
    }
    if (colName in selections && isStringArray(selections[colName])) {
      highlights = [...highlights, ...(selections[colName] as string[])];
    }

    if (highlights.length) {
      return {
        component: SubstringHighlight,
        props: {
          value: value,
          highlights,
        },
      };
    }

    return {
      component: Regular,
      props: { value: formatValue(value, { type: datatype }) },
    };
  }

  async function getWordSpans(
    datasetInfo: DatasetInfo | undefined,
    id: number,
    filterBy,
    selectionMap: SelectionMap,
    tableClient: TableClient | undefined,
    textCols: string[],
    joinInfo?: JoinInfo,
  ): Promise<undefined | Record<string, unknown[]>> {
    // console.log("[getWordsPerDoc] selection is: ", filterBy);
    // console.log("[getWordsPerDoc] selectionMap is: ", selectionMap);
    if (!datasetInfo) {
      console.log("no dataset info");
      return undefined;
    }

    if (!Object.keys(selectionMap).length) {
      console.log("no selectionmap");
      return undefined;
    }

    // TODO might be able to just do this with table client and so selection
    if (!tableClient) {
      console.log("no table client");
      return undefined;
    }

    let spanMap = {};
    const filters = tableClient.filterBy?.predicate(tableClient);

    for (let textCol of textCols) {
      if (
        joinInfo?.joinColumn.associated_text_col_name === textCol &&
        joinInfo?.joinColumn.name in selectionMap
      ) {
        let spans = await databaseConnection.getSpansPerDoc(
          datasetInfo,
          id,
          filters,
        );
        spanMap[textCol] = spans;
      }
    }

    console.log("words::: ", spanMap);

    return spanMap;
  }

  $: wordSpans = getWordSpans(
    datasetInfo,
    id,
    $filters.brush,
    $selectionDisplay, // for reactivity to filter updates
    tableClient,
    textData.map((d) => d[0]),
    $filters.joinDatasetInfo,
  );
</script>

<div
  class={`rounded border bg-white ${highlight ? "border-dashed border-primary-500" : "border-solid border-gray-300"}`}
>
  <div class="flex items-center border-b border-gray-300 p-2 gap-1">
    <button
      class="hover:bg-gray-100 text-gray-500 p-1 rounded"
      on:click={() => (toggle = !toggle)}
    >
      {#if toggle}
        <AngleDownOutline size="xs" />
      {:else}
        <AngleRightOutline size="xs" />
      {/if}
    </button>
    <slot name="optionButtons" />
    <slot name="title" />

    <div class="grow"></div>
    <div class="text-gray-500">{id}</div>
  </div>

  <div
    class={`flex  ${toggle ? "max-h-96 overflow-auto " : "max-h-48 overflow-hidden"}`}
  >
    <div class={`w-full px-2 pt-2 pb-4 text-gray-800 flex flex-col gap-1`}>
      {#await wordSpans}
        {#each textData as [textColName, textColData] (textColName)}
          <div>
            <div class="border-b border-gray-300 italic">
              {textColName}
              <Spinner class="ml-1" size="4" />
            </div>

            <div>
              {formatValue(textColData, { type: "text" })}
            </div>
          </div>
        {/each}
      {:then wordSpanMap}
        {#each textData as [textColName, textColData] (textColName)}
          <div>
            <div class="border-b border-gray-300 italic">
              {textColName}
            </div>

            {#if wordSpanMap && textColName in wordSpanMap}
              <SpanIndexHighlight
                highlights={wordSpanMap[textColName]}
                value={textColData}
              />
            {:else}
              <div>
                {formatValue(textColData, { type: "text" })}
              </div>
            {/if}
          </div>
        {/each}
      {/await}
    </div>

    {#if metadata.length}
      <div class="bg-gray-50 w-80 shrink-0 h-full">
        {#each metadata as [itemKey, itemValue] (itemKey)}
          {@const renderComponent = renderValue(
            itemValue,
            itemKey,
            $selectionDisplay,
            $filters.joinDatasetInfo,
            datasetInfo?.column_info.find((col) => col.name === itemKey)?.type,
          )}
          <div class="flex border-b border-gray-200 px-2">
            <div
              class="whitespace-normal text-ellipsis overflow-hidden text-sm w-1/3 font-semibold italic"
              title={itemKey}
            >
              {itemKey}
            </div>
            <div
              class={`whitespace-normal break-words text-sm w-2/3 ${itemValue == undefined ? "text-gray-300 italic" : "text-gray-800"}`}
            >
              <svelte:component
                this={renderComponent.component}
                {...renderComponent.props}
              />
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>
