<script lang="ts">
  import { datasetSchema } from "../stores";
  import ScatterProjection from "./charts/ScatterProjection.svelte";
  import type { Column } from "../backendapi";
  import { Select } from "flowbite-svelte";
  import { projectionColorColumn } from "../stores";
  import Toggle from "./Toggle.svelte";
  import { CogOutline } from "flowbite-svelte-icons";

  export let colorCols: Column[] = [];
  let showSettings = false;
  let plotOpacity = 0.4;
</script>

<Toggle active={$datasetSchema.has_projection}>
  <div slot="title">Dataset Overview</div>
  <div slot="body">
    {#if $datasetSchema.has_projection}
      <div class="flex flex-col">
        <div class="flex justify-end">
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
          <button
            class="hover:bg-secondary-200 text-gray-500 p-1 rounded inline"
            on:click={() => {
              showSettings = !showSettings;
            }}
          >
            <CogOutline size="xs" />
          </button>
        </div>

        {#if showSettings}
          <div
            class="px-4 py-2 mx-2 mt-2 rounded bg-gray-100 flex gap-2 items-center"
          >
            <input
              type="range"
              min={0}
              max={1}
              step={0.1}
              class="bg-gray-100 border-gray-300 dark:ring-offset-gray-800 me-2 dark:bg-gray-700 dark:border-gray-600 rounded text-primary-600"
              bind:value={plotOpacity}
            />
            <span class="text-sm text-gray-500">
              Opacity value is {plotOpacity}
            </span>
          </div>
        {/if}
        <ScatterProjection
          mainDatasetName={$datasetSchema.name}
          columnX="umap_x"
          columnY="umap_y"
          colorColName={$projectionColorColumn}
          opacity={plotOpacity}
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
</Toggle>
