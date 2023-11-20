<script lang="ts">
  import { slide } from "svelte/transition";
  import type { Column } from "../shared/types";

  import DataTypeIcon from "./DataTypeIcon.svelte";
  import Histogram from "./charts/Histogram.svelte";
  import CategoricalChart from "./charts/CategoricalChart.svelte";
  import SearchBar from "./charts/SearchBar.svelte";

  export let displayCol: Column;
  export let plotCols: Column[];
  export let datasetName: string;

  let active = true;
</script>

<div>
  <button
    class="px-2 flex space-between items-center gap-2 justify-between w-full hover:bg-gray-100 h-9"
    class:bg-gray-50={active}
    on:click={() => {
      active = !active;
    }}
  >
    <DataTypeIcon type={displayCol.type} />

    <p class:font-medium={active} class="text-left flex-1">
      {displayCol.name}
    </p>
  </button>
  <div class="w-full">
    {#if active}
      <div transition:slide|local={{ duration: 200 }} class="ml-4 mt-2">
        {#if displayCol.type === "text"}
          <SearchBar {datasetName} columnName={displayCol.name} />
        {/if}

        <div class="flex flex-col">
          {#each plotCols as col}
            {#if col.type === "number"}
              <Histogram {datasetName} columnName={col.name} />
            {:else if col.type === "categorical"}
              <SearchBar {datasetName} columnName={col.name} />
              <CategoricalChart {datasetName} columnName={col.name} />
            {:else if col.type === "date"}
              <!-- <DateChart {datasetName} columnName={col.name} /> -->
              TODO: Date chart...
            {:else}
              <div>{col.name}: Unsupported column type ({col.type})</div>
            {/if}
          {/each}
        </div>
      </div>
    {/if}
  </div>
</div>
