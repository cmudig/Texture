<script lang="ts">
  import {
    AngleRightOutline,
    AngleDownOutline,
    MapPinAltSolid,
  } from "flowbite-svelte-icons";
  import { formatValue } from "../../shared/format";
  import SpanIndexHighlight from "./SpanIndexHighlight.svelte";
  import SubstringHighlight from "./SubstringHighlight.svelte";
  import {
    databaseConnection,
    datasetSchema,
    selectionDisplay,
    showSegmentValues,
    setSchema,
  } from "../../stores";
  import type { Column } from "../../backendapi";
  import { shouldHighlight } from "../../shared/utils";
  import type { SelectionMap } from "../../shared/types";
  import ArrayDisplay from "./ArrayDisplay.svelte";

  export let idSchema: Column;
  export let colSchema: Column[];
  export let mainTableData: object[];
  export let arrayTableMap: Map<string, object[]> | undefined = undefined; // {colname: [data]}
  export let highlight = false;

  let toggle = false;

  $: textColSchemas = colSchema.filter((c) => c.type === "text");
  $: metaColSchemas = [idSchema, ...colSchema.filter((c) => c.type !== "text")];

  /**
   * For a given text column, finds cols in current selection that are derived from it
   * and then gets the span values for those selections
   */
  function getSpanHighlights(
    textCol: Column,
    currentSelections: SelectionMap,
    segmentTables,
    schemas: Column[],
  ): undefined | any[] {
    // get cols that correspond to this text
    const matching_selections = Object.entries(currentSelections).filter(
      ([k, v]) => {
        const match = schemas.find((c) => c.name === k);
        return (
          match &&
          match.derivedSchema?.is_segment &&
          match.derivedSchema?.derived_from === textCol.name
        );
      },
    );

    if (!matching_selections.length) {
      return undefined;
    }

    // get only the matching values from each segment table
    const colSpanMap = new Map<string, any[]>();
    for (let [colName, selection] of matching_selections as [string, any[]][]) {
      const segmentTable = segmentTables.get(colName);
      if (!segmentTable) {
        continue;
      }
      const matching_spans = segmentTable.filter((v) =>
        selection.includes(v[colName]),
      );
      colSpanMap.set(colName, matching_spans);
    }

    // combine selections into one list
    const combinedSpans = Array.from(colSpanMap.values()).flat();

    // FUTURE: keep the keys and highlight different colors
    return combinedSpans;
  }

  function runSimilaritySearch(id, table) {
    console.log("Starting similarity search", { id, table });
    const prom = databaseConnection.api.runEmbedSearch(table, id);

    prom.then((res) => {
      console.log("Finished similarity search", res);
      setSchema();

      // TODO issue #136: hack to force table reload
      window.location.reload();
    });
  }
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
      title="Calculate similar"
      class="hover:bg-gray-100 text-gray-500 p-1 rounded"
      on:click={() => {
        runSimilaritySearch(
          Number(mainTableData[idSchema.name]),
          $datasetSchema.name,
        );
      }}
      class:hidden={!$datasetSchema.has_embeddings}
    >
      <MapPinAltSolid size="xs" />
    </button>
  </div>

  <div
    class={`w-full px-2 pt-2 pb-4 text-gray-800 flex flex-col gap-1 border-gray-300 border-r ${toggle ? "overflow-auto" : "overflow-hidden"}`}
  >
    <slot name="title" />

    {#each textColSchemas as textSchema, idx (textSchema.name)}
      {@const wordSpans = getSpanHighlights(
        textSchema,
        $selectionDisplay,
        arrayTableMap,
        colSchema,
      )}
      <div
        class={idx !== textColSchemas.length - 1
          ? "border-b border-gray-300"
          : ""}
      >
        <div class="font-light text-secondary-600 inline">
          {textSchema.name}:
        </div>

        <div class="text-gray-800 inline">
          <!-- TODO: can be both, but right now only doing one at a time -->
          {#if wordSpans != undefined}
            <SpanIndexHighlight
              highlights={wordSpans}
              value={mainTableData[textSchema.name]}
            />
          {:else if textSchema.name in $selectionDisplay}
            <SubstringHighlight
              highlights={$selectionDisplay[textSchema.name]}
              value={mainTableData[textSchema.name]}
            />
          {:else}
            <span class="whitespace-pre-wrap">
              {formatValue(mainTableData[textSchema.name], { type: "text" })}
            </span>
          {/if}
        </div>
      </div>
    {/each}
  </div>

  {#if metaColSchemas.length}
    <div
      class={`w-[300px] shrink-0 pt-2 ${toggle ? "overflow-auto" : "overflow-hidden"}`}
    >
      {#each metaColSchemas as metaSchema (metaSchema.name)}
        {@const name = metaSchema.name}
        {@const table = metaSchema.derivedSchema
          ? arrayTableMap?.get(name)
          : mainTableData}
        {@const hasValue = metaSchema.derivedSchema
          ? arrayTableMap?.get(name) != null
          : mainTableData[name] != null}

        <div class="flex px-2 mb-[2px]">
          <div
            class="whitespace-normal text-ellipsis overflow-hidden text-sm font-light text-secondary-600 shrink-0 w-[165px]"
            title={String(name)}
          >
            {name}
          </div>
          <div
            class={`whitespace-normal break-words text-sm pl-1 grow ${hasValue ? "text-gray-800" : "text-gray-300 italic"}`}
            class:bg-highlight-100={name in $selectionDisplay &&
              shouldHighlight(
                mainTableData[name],
                $selectionDisplay[name],
                metaSchema.type,
              )}
          >
            <div>
              {#if metaSchema.derivedSchema?.is_segment}
                {#if $showSegmentValues}
                  <ArrayDisplay {name} type={metaSchema.type} data={table} />
                {:else}
                  <span class="italic text-gray-500">
                    {table?.length ?? 0} items
                  </span>
                {/if}
              {:else if metaSchema.derivedSchema && arrayTableMap}
                <ArrayDisplay
                  {name}
                  type={metaSchema.type}
                  data={table}
                  highlights={$selectionDisplay[name]}
                />
              {:else}
                {formatValue(table?.[name], {
                  type: metaSchema.type,
                  colName: metaSchema.name,
                })}
              {/if}
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
