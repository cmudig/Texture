<script lang="ts">
  import { slide } from "svelte/transition";
  import type { ColumnSummary } from "../shared/types";
  import type { Column } from "../backendapi/models/Column";
  import DataTypeIcon from "./DataTypeIcon.svelte";
  import Histogram from "./charts/Histogram.svelte";
  import CategoricalChart from "./charts/CategoricalChart.svelte";
  import DateChart from "./charts/DateChart.svelte";
  import NullDisplay from "./NullDisplay.svelte";
  import Projection from "./charts/Projection.svelte";
  import { filters, showBackgroundDist } from "../stores";

  export let displayCol: Column;
  export let plotCols: Column[];
  export let colSummary: ColumnSummary | undefined = undefined;
  export let colType: string | undefined = undefined;

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
    <div class="ml-4 mt-2" class:hidden={!active}>
      {#if colType === "point"}
          <Projection
            mainDatasetName="projection"
            joinDatasetInfo={{
              joinDatasetName: $filters.datasetName,
              joinKey: "id",
              joinColumn: undefined,
            }}
            columnName="projection_xy"
            showBackground={$showBackgroundDist}
          />
      {:else}

      {#if colType === "text" && $filters.joinDatasetInfo}
        <h3 class="italic">{$filters.joinDatasetInfo.joinColumn.name}</h3>

        <CategoricalChart
          mainDatasetName={$filters.joinDatasetInfo.joinDatasetName}
          joinDatasetInfo={{
            joinDatasetName: $filters.datasetName,
            joinKey: $filters.joinDatasetInfo.joinKey,
            joinColumn: undefined,
          }}
          columnName={$filters.joinDatasetInfo.joinColumn.name}
          showBackground={false}
          limit={20}
        />
      {/if}

      <div class="flex flex-col">
        {#if colType === "text" && plotCols.length}
          <h3 class="italic">Extracted metadata</h3>
        {/if}

        {#each plotCols as col}
          {#if col.type === "number"}
            <Histogram
              mainDatasetName={$filters.datasetName}
              joinDatasetInfo={$filters.joinDatasetInfo}
              showBackground={$showBackgroundDist}
              columnName={col.name}
            />
          {:else if col.type === "categorical"}
            <CategoricalChart
              mainDatasetName={$filters.datasetName}
              joinDatasetInfo={$filters.joinDatasetInfo}
              showBackground={$showBackgroundDist}
              columnName={col.name}
            />
          {:else if col.type === "date"}
            <DateChart
              mainDatasetName={$filters.datasetName}
              joinDatasetInfo={$filters.joinDatasetInfo}
              columnName={col.name}
            />
          {:else}
            <div>{col.name}: Unsupported column type ({col.type})</div>
          {/if}
        {/each}
      </div>
      
      {/if}
    </div>
  </div>
</div>
