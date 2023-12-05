<script lang="ts">
  import { slide } from "svelte/transition";
  import type { Column, ColumnSummary } from "../shared/types";
  import DataTypeIcon from "./DataTypeIcon.svelte";
  import Histogram from "./charts/Histogram.svelte";
  import CategoricalChart from "./charts/CategoricalChart.svelte";
  import SearchBar from "./charts/SearchBar.svelte";
  import DateChart from "./charts/DateChart.svelte";
  import NullDisplay from "./NullDisplay.svelte";

  export let displayCol: Column;
  export let plotCols: Column[];
  export let colSummary: ColumnSummary | undefined = undefined;

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
    <DataTypeIcon type={displayCol.type} />

    <p
      class:font-medium={active}
      class="max-w-sm overflow-hidden text-ellipsis text-left"
    >
      {displayCol.name}
    </p>

    <div class="grow" />

    {#if colSummary?.null_percentage}
      <NullDisplay nullPercentage={parseFloat(colSummary.null_percentage)} />
    {/if}
  </button>
  <div class="w-full">
    {#if active}
      <div transition:slide|local={{ duration: 200 }} class="ml-4 mt-2">
        {#if displayCol.type === "text"}
          <SearchBar columnName={displayCol.name} />
        {/if}

        <div class="flex flex-col">
          {#each plotCols as col}
            {#if col.type === "number"}
              <Histogram columnName={col.name} />
            {:else if col.type === "categorical"}
              <SearchBar columnName={col.name} />
              <CategoricalChart columnName={col.name} />
            {:else if col.type === "date"}
              <DateChart columnName={col.name} />
            {:else}
              <div>{col.name}: Unsupported column type ({col.type})</div>
            {/if}
          {/each}
        </div>
      </div>
    {/if}
  </div>
</div>
