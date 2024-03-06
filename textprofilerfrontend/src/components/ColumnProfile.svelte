<script lang="ts">
  import type { ColumnSummary } from "../shared/types";
  import type { Column } from "../backendapi/models/Column";
  import DataTypeIcon from "./DataTypeIcon.svelte";
  import Histogram from "./charts/Histogram.svelte";
  import CategoricalChart from "./charts/CategoricalChart.svelte";
  import DateChart from "./charts/DateChart.svelte";
  import NullDisplay from "./NullDisplay.svelte";
  import { datasetInfo, showBackgroundDist } from "../stores";
  import { stopwords } from "../shared/stopwords";

  export let displayCol: Column;
  export let colSummary: ColumnSummary | undefined;

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
    {#if displayCol.derived_from}
      <p class="text-gray-400 italic">
        (derived from {displayCol.derived_from})
      </p>
    {/if}

    <div class="grow" />

    {#if colSummary?.null_percentage}
      <NullDisplay nullPercentage={parseFloat(colSummary.null_percentage)} />
    {/if}
  </button>
  <div class="w-full">
    <div class="ml-4 my-1" class:hidden={!active}>
      {#if displayCol.table_name && displayCol.table_name !== $datasetInfo.name}
        {#if displayCol.type === "categorical" || displayCol.type === "text"}
          <CategoricalChart
            mainDatasetName={displayCol.table_name}
            columnName={displayCol.name}
            limit={20}
            excludeList={$datasetInfo.columns.find(
              (c) => c.name === displayCol.derived_from,
            )?.type === "text"
              ? $stopwords
              : undefined}
            plotNulls={true}
            isDerivedTable={true}
          />
        {:else}
          Not currently supporting quantitative columns from another table...
        {/if}
      {:else if displayCol.type === "number"}
        <Histogram
          mainDatasetName={$datasetInfo.name}
          showBackground={$showBackgroundDist}
          columnName={displayCol.name}
        />
      {:else if displayCol.type === "categorical"}
        <CategoricalChart
          mainDatasetName={$datasetInfo.name}
          showBackground={$showBackgroundDist}
          columnName={displayCol.name}
        />
      {:else if displayCol.type === "date"}
        <DateChart
          mainDatasetName={$datasetInfo.name}
          columnName={displayCol.name}
        />
      {:else}
        <div>
          {displayCol.name}: Unsupported column type ({displayCol.type})
        </div>
      {/if}
    </div>
  </div>
</div>
