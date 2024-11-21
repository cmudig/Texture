<script lang="ts">
  import {
    AngleRightOutline,
    AngleDownOutline,
    FilterOutline,
  } from "flowbite-svelte-icons";
  import { formatValue } from "../../shared/format";
  import { type SelectionMap } from "../../shared/types";
  import SpanIndexHighlight from "./SpanIndexHighlight.svelte";
  import SubstringHighlight from "./SubstringHighlight.svelte";
  import {
    datasetSchema,
    selectionDisplay,
    databaseConnection,
    compareSimilarID,
  } from "../../stores";
  import type { DatasetSchema } from "../../backendapi";
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
    datasetSchema: DatasetSchema,
    _selection?: any,
  ): Promise<undefined | Record<string, unknown[]>> {
    if (!datasetSchema || !selection || !Object.keys(selectionMap).length) {
      return undefined;
    }

    let spanMap = {};

    for (let textCol of textCols) {
      // TODO: this is buggy because the col might not always be the first found -- but will probably be replaced anyway
      let derivedCol = datasetSchema.columns.find(
        (col) =>
          col.derivedSchema?.is_segment &&
          col.derivedSchema?.derived_from === textCol,
      );

      // console.log("DERIVED_COL: ", derivedCol);

      if (derivedCol != undefined && derivedCol.name in selectionMap) {
        let spans = await databaseConnection.getSpansPerDoc(
          derivedCol.derivedSchema?.table_name as string,
          derivedCol.name,
          datasetSchema.primary_key.name,
          id,
          _selection,
        );

        spanMap[textCol] = spans;
      }
    }

    // console.log("SpanMap: ", spanMap);

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
    $datasetSchema,
    selection,
  );
</script>

<div
  class={`rounded border bg-white flex ${highlight ? "border-dashed border-primary-500" : "border-solid border-gray-300"} ${toggle ? "max-h-96" : "max-h-40"}`}
>
  <div
    class="flex flex-col items-center border-r border-gray-300 p-1 gap-1 w-8 max-w-10 shrink-0"
  >
    <button
      title="Toggle"
      class="hover:bg-gray-100 text-gray-500 p-1 rounded"
      on:click={() => (toggle = !toggle)}
    >
      {#if toggle}
        <AngleDownOutline size="xs" />
      {:else}
        <AngleRightOutline size="xs" />
      {/if}
    </button>
    <button
      title="Show similar"
      class="hover:bg-gray-100 text-gray-500 p-1 rounded"
      on:click={() => {
        $compareSimilarID = id;
      }}
      class:hidden={!$datasetSchema.has_embeddings}
    >
      <FilterOutline size="xs" />
    </button>
  </div>

  <div
    class={`w-full px-2 pt-2 pb-4 text-gray-800 flex flex-col gap-1 border-gray-300 border-r ${toggle ? "overflow-auto" : "overflow-hidden"}`}
  >
    <slot name="title" />

    {#await wordSpans}
      {#each textData as [textColName, textColData], idx (textColName)}
        <div
          class={idx !== textData.length - 1 ? "border-b border-gray-300" : ""}
        >
          <div class="font-light text-secondary-600 inline animate-pulse">
            {textColName}:
          </div>

          <div class="text-gray-800 inline animate-pulse whitespace-pre-wrap">
            {formatValue(textColData, { type: "text" })}
          </div>
        </div>
      {/each}
    {:then wordSpanMap}
      {#each textData as [textColName, textColData], idx (textColName)}
        <div
          class={idx !== textData.length - 1 ? "border-b border-gray-300" : ""}
        >
          <div class="font-light text-secondary-600 inline">
            {textColName}:
          </div>

          <div class="text-gray-800 inline">
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
              <span class="whitespace-pre-wrap">
                {formatValue(textColData, { type: "text" })}
              </span>
            {/if}
          </div>
        </div>
      {/each}
    {/await}
  </div>

  {#if plotMetadata.length}
    <div
      class={`w-[300px] shrink-0 pt-2 ${toggle ? "overflow-auto" : "overflow-hidden"}`}
    >
      {#each plotMetadata as [itemKey, itemValue] (itemKey)}
        {@const itemType = $datasetSchema?.columns.find(
          (col) => col.name === itemKey,
        )?.type}
        <div class="flex px-2">
          <div
            class="whitespace-normal text-ellipsis overflow-hidden text-sm font-light text-secondary-600 shrink-0 w-[165px]"
            title={String(itemKey)}
          >
            {itemKey}
          </div>
          <div
            class={`whitespace-normal break-words text-sm pl-1 grow ${itemValue == undefined ? "text-gray-300 italic" : "text-gray-800"}`}
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
