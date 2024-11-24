<script lang="ts">
  import { datasetSchema } from "../stores";
  import ScatterProjection from "./charts/ScatterProjection.svelte";
  import type { Column } from "../backendapi";
  import { Select } from "flowbite-svelte";
  import { projectionColorColumn } from "../stores";
  import Toggle from "./Toggle.svelte";

  export let colorCols: Column[] = [];
</script>

<Toggle active={$datasetSchema.has_projection}>
  <div slot="title">Dataset Overview</div>
  <div slot="body">
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
          columnX="umap_x"
          columnY="umap_y"
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
</Toggle>
