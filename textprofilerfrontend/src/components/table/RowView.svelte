<script lang="ts">
  import { AngleRightOutline, AngleDownOutline } from "flowbite-svelte-icons";
  import { formatValue } from "../../shared/format";
  import { type SelectionMap } from "../../shared/types";
  import SpanIndexHighlight from "./SpanIndexHighlight.svelte";
  import SubstringHighlight from "./SubstringHighlight.svelte";
  import type { JoinInfo } from "../../backendapi";
  import { filters, selectionDisplay, databaseConnection } from "../../stores";
  import type { DatasetInfo } from "../../backendapi";
  import { Spinner } from "flowbite-svelte";
  import { shouldHighlight } from "../../shared/utils";

  export let id: number;
  export let textData: Array<[string, unknown]>;
  export let metadata: Array<[string, unknown]>;
  export let highlight = false;
  export let datasetInfo: DatasetInfo | undefined = undefined;
  export let selection: any = undefined; // vgplot.Selection

  let toggle = false;

  async function getWordSpans(
    id: number,
    textCols: string[],
    selectionMap: SelectionMap,
    _selection?: any,
    datasetInfo?: DatasetInfo,
    joinInfo?: JoinInfo,
  ): Promise<undefined | Record<string, unknown[]>> {
    if (!datasetInfo || !selection || !Object.keys(selectionMap).length) {
      return undefined;
    }

    let spanMap = {};

    for (let textCol of textCols) {
      if (
        joinInfo?.joinColumn.associated_text_col_name === textCol &&
        joinInfo?.joinColumn.name in selectionMap
      ) {
        let spans = await databaseConnection.getSpansPerDoc(
          datasetInfo,
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
    selection,
    datasetInfo,
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
          {@const itemType = datasetInfo?.column_info.find(
            (col) => col.name === itemKey,
          )?.type}
          <div class="flex border-b border-gray-200 px-2">
            <div
              class="whitespace-normal text-ellipsis overflow-hidden text-sm w-1/3 font-semibold italic"
              title={itemKey}
            >
              {itemKey}
            </div>
            <div
              class={`whitespace-normal break-words text-sm w-2/3 ${itemValue == undefined ? "text-gray-300 italic" : "text-gray-800"}`}
              class:bg-yellow-200={itemKey in $selectionDisplay &&
                shouldHighlight(
                  itemValue,
                  $selectionDisplay[itemKey],
                  itemType,
                )}
            >
              <div>
                {formatValue(itemValue, { type: itemType })}
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>
