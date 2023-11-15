<script lang="ts">
  import { slide } from "svelte/transition";
  import type { DataType } from "../shared/types";

  import ChartGroup from "./ChartGroup.svelte";
  import DataTypeIcon from "./DataTypeIcon.svelte";

  export let colName: string;
  export let colType: DataType;

  export let chartColNames: string[];
  export let datasetName: string;
  export let brush: any;

  let active = false;
</script>

<div>
  <button
    class="px-2 flex space-between items-center gap-2 justify-between w-full hover:bg-gray-100 h-9"
    class:bg-gray-50={active}
    on:click={() => {
      active = !active;
    }}
  >
    <DataTypeIcon type={colType} />

    <p class:font-medium={active} class="text-left flex-1">
      {colName}
    </p>
  </button>
  <div class="w-full">
    {#if active}
      <div transition:slide|local={{ duration: 200 }} class="ml-4 mt-2">
        <ChartGroup colNames={chartColNames} {datasetName} {brush} />
      </div>
    {/if}
  </div>
</div>
