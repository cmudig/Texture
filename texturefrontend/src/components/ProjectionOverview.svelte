<script lang="ts">
  import { datasetInfo } from "../stores";
  import ScatterProjection from "./charts/ScatterProjection.svelte";

  let active = getInitialToggle();

  function getInitialToggle() {
    if ($datasetInfo.has_projection) {
      return true;
    }
    return false;
  }
</script>

<div>
  <button
    class="space-between flex h-9 w-full items-center justify-between gap-2 px-2 hover:bg-gray-100 border-t-2 border-gray-100"
    class:bg-gray-50={active}
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
  <div class="w-full">
    <div class="ml-4 mt-2" class:hidden={!active}>
      {#if $datasetInfo.has_projection}
        <ScatterProjection
          mainDatasetName={$datasetInfo.name}
          columnName="projection_xy"
        />
      {:else}
        <div class="text-gray-500 mb-2">
          No projection uploaded! Try uploading <span class="font-bold"
            >embeddings</span
          >
          or columns
          <span class="font-bold">umap_x</span>
          and <span class="font-bold">umap_y</span> to see overview projection.
        </div>
      {/if}
    </div>
  </div>
</div>
