<script lang="ts">
  import {
    AngleRightOutline,
    AngleDownOutline,
    FilterOutline,
  } from "flowbite-svelte-icons";
  import { formatValue } from "../../shared/format";
  import SpanIndexHighlight from "./SpanIndexHighlight.svelte";
  import SubstringHighlight from "./SubstringHighlight.svelte";
  import {
    datasetSchema,
    selectionDisplay,
    compareSimilarID,
  } from "../../stores";
  import type { Column } from "../../backendapi";
  import { shouldHighlight } from "../../shared/utils";

  export let idSchema: Column;
  export let colSchema: Column[];
  export let mainTableData;
  export let highlight = false;

  let toggle = false;

  $: textColSchemas = colSchema.filter((c) => c.type === "text");
  $: metaColSchemas = [idSchema, ...colSchema.filter((c) => c.type !== "text")];

  const wordSpanMap = undefined;
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
        $compareSimilarID = Number(mainTableData[idSchema.name]);
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

    {#each textColSchemas as textSchema, idx (textSchema.name)}
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
          {#if wordSpanMap && textSchema.name in wordSpanMap}
            <SpanIndexHighlight
              highlights={wordSpanMap[textSchema.name]}
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
        <div class="flex px-2">
          <div
            class="whitespace-normal text-ellipsis overflow-hidden text-sm font-light text-secondary-600 shrink-0 w-[165px]"
            title={String(metaSchema.name)}
          >
            {metaSchema.name}
          </div>
          <div
            class={`whitespace-normal break-words text-sm pl-1 grow ${mainTableData[metaSchema.name] == undefined ? "text-gray-300 italic" : "text-gray-800"}`}
            class:bg-highlight-300={metaSchema.name in $selectionDisplay &&
              shouldHighlight(
                mainTableData[metaSchema.name],
                $selectionDisplay[metaSchema.name],
                metaSchema.type,
              )}
          >
            <div>
              {formatValue(mainTableData[metaSchema.name], {
                type: metaSchema.type,
                colName: metaSchema.name,
              })}
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
