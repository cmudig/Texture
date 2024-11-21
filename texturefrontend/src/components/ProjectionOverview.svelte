<script lang="ts">
  import { datasetSchema } from "../stores";
  import ScatterProjection from "./charts/ScatterProjection.svelte";
  import type { Column } from "../backendapi";
  import { Select } from "flowbite-svelte";
  import { projectionColorColumn } from "../stores";

  export let colorCols: Column[] = [];
  // let colorColName: string | undefined = undefined;

  let active = getInitialToggle();

  function getInitialToggle() {
    if ($datasetSchema.has_projection) {
      return true;
    }
    return false;
  }
</script>

<div>
  <button
    class="space-between flex h-9 w-full items-center justify-between gap-2 px-2 hover:bg-gray-200 border-t-2 border-secondary-200"
    class:bg-gray-100={active}
    on:click={() => {
      active = !active;
    }}
  >
    <p
      class:font-medium={active}
      class="max-w-sm overflow-hidden text-ellipsis text-left"
    >
      Dataset Overview
    </p>
  </button>

  <div class="w-full pl-4 pt-2 pr-2" class:hidden={!active}>
    {#if $datasetSchema.has_projection}
      <div class="flex flex-col">
        {#if colorCols.length > 0}
          <Select
            class="max-w-40 py-1 self-end"
            size="sm"
            items={[
              { value: undefined, name: "No color" },
              ...colorCols.map((col) => ({
                value: col.name,
                name: col.name,
              })),
            ]}
            bind:value={$projectionColorColumn}
            placeholder="Color by..."
          />
        {/if}

        <ScatterProjection
          mainDatasetName={$datasetSchema.name}
          columnName="projection_xy"
          colorColName={$projectionColorColumn}
        />
      </div>
    {:else}
      <div class="text-gray-500 mb-2">
        No projection uploaded! Try uploading <span class="font-bold"
          >embeddings</span
        >
        or columns
        <span class="font-bold">umap_x</span>
        and <span class="font-bold">umap_y</span>.
      </div>
    {/if}
  </div>
</div>
