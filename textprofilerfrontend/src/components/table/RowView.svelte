<script lang="ts">
  import { AngleRightOutline, AngleDownOutline } from "flowbite-svelte-icons";
  import { formatValue } from "../../shared/format";
  import { type SelectionMap } from "../../shared/types";
  import SpanIndexHighlight from "./SpanIndexHighlight.svelte";
  import SubstringHighlight from "./SubstringHighlight.svelte";
  import {
    datasetInfo,
    selectionDisplay,
    databaseConnection,
  } from "../../stores";
  import type { DatasetInfo } from "../../backendapi";
  import { Spinner } from "flowbite-svelte";
  import { shouldHighlight } from "../../shared/utils";

  export let id: number;
  export let textData: Array<[string, unknown]>;
  export let metadata: Array<[string, unknown]>;
  export let highlight = false;
  export let selection: any = undefined; // vgplot.Selection

  $: plotMetadata = [["id", id], ...metadata];

  let toggle = false;

  async function getWordSpans(
    id: number,
    textCols: string[],
    selectionMap: SelectionMap,
    datasetInfo: DatasetInfo,
    _selection?: any,
  ): Promise<undefined | Record<string, unknown[]>> {
    if (!datasetInfo || !selection || !Object.keys(selectionMap).length) {
      return undefined;
    }

    let spanMap = {};

    for (let textCol of textCols) {
      let derivedCol = datasetInfo.columns.find(
        (col) =>
          col.derived_from === textCol &&
          col.table_name &&
          col.table_name !== datasetInfo.name,
      );

      if (
        derivedCol &&
        derivedCol.table_name &&
        derivedCol.name in selectionMap
      ) {
        let spans = await databaseConnection.getSpansPerDoc(
          derivedCol.table_name,
          derivedCol.name,
          datasetInfo.primary_key.name,
          id,
          _selection,
        );

        spanMap[textCol] = spans;
      }
    }

    return spanMap;
  }

  /**
   * BUG: this is called twice now, once when $selectionDisplay updates, and then again once textData prop
   * updates, not sure how to batch these?
   *
   */
  $: wordSpans = getWordSpans(
    id,
    textData.map((d) => d[0]),
    $selectionDisplay,
    $datasetInfo,
    selection,
  );
</script>

<div
  class={`rounded border bg-white flex ${highlight ? "border-dashed border-primary-500" : "border-solid border-gray-300"} ${toggle ? "max-h-96" : "max-h-48"}`}
>
  <div
    class="flex flex-col items-center border-r border-gray-300 p-1 gap-1 w-8 max-w-10 shrink-0"
  >
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
  </div>

  <div
    class={`w-full px-2 pt-2 pb-4 text-gray-800 flex flex-col gap-1 border-gray-300 border-r ${toggle ? "overflow-auto" : "overflow-hidden"}`}
  >
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
          <div class="border-b border-gray-300 font-light text-secondary-700">
            {textColName}
          </div>

          <!-- TODO: can be both, but right now only doing one at a time -->
          {#if wordSpanMap && textColName in wordSpanMap}
            <SpanIndexHighlight
              highlights={wordSpanMap[textColName]}
              value={textColData}
            />
          {:else if textColName in $selectionDisplay}
            <SubstringHighlight
              highlights={$selectionDisplay[textColName]}
              value={textColData}
            />
          {:else}
            <div class="text-gray-800">
              {formatValue(textColData, { type: "text" })}
            </div>
          {/if}
        </div>
      {/each}
    {/await}
  </div>

  {#if plotMetadata.length}
    <div
      class={`w-80 shrink-0 pt-2 ${toggle ? "overflow-auto" : "overflow-hidden"}`}
    >
      {#each plotMetadata as [itemKey, itemValue] (itemKey)}
        {@const itemType = $datasetInfo?.columns.find(
          (col) => col.name === itemKey,
        )?.type}
        <div class="flex px-2">
          <div
            class="whitespace-normal text-ellipsis overflow-hidden text-sm font-light text-secondary-700 w-1/3"
            title={String(itemKey)}
          >
            {itemKey}
          </div>
          <div
            class={`whitespace-normal break-words text-sm pl-1 w-2/3 ${itemValue == undefined ? "text-gray-300 italic" : "text-gray-800"}`}
            class:bg-highlight-300={itemKey in $selectionDisplay &&
              shouldHighlight(itemValue, $selectionDisplay[itemKey], itemType)}
          >
            <div>
              {formatValue(itemValue, { type: itemType, colName: itemKey })}
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
