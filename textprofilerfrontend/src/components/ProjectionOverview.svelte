<script lang="ts">
  import { datasetInfo } from "../stores";
  import ScatterProjection from "./charts/ScatterProjection.svelte";

  let active = true;
</script>

<div>
  <button
    class="space-between flex h-9 w-full items-center justify-between gap-2 px-2 hover:bg-gray-100"
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
      <ScatterProjection
        mainDatasetName={$datasetInfo.name}
        columnName="projection_xy"
      />
    </div>
  </div>
</div>
