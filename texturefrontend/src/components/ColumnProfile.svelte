<script lang="ts">
  import type { ColumnSummary } from "../shared/types";
  import DataTypeIcon from "./icons/DataTypeIcon.svelte";
  import Histogram from "./charts/Histogram.svelte";
  import CategoricalChart from "./charts/CategoricalChart.svelte";
  import DateChart from "./charts/DateChart.svelte";
  import NullDisplay from "./NullDisplay.svelte";
  import { datasetInfo, showBackgroundDistMap } from "../stores";
  import { stopwords } from "../shared/stopwords";
  import { getUUID } from "../shared/utils";
  import DerivedIcon from "./icons/DerivedIcon.svelte";
  import { CogOutline } from "flowbite-svelte-icons";
  import { Toggle } from "flowbite-svelte";
  import Search from "./Search.svelte";
  import type { Column, DatasetInfo } from "../backendapi";

  export let displayCol: Column;
  export let colSummary: ColumnSummary | undefined;

  let id = getUUID();

  let active = true;
  let showSettings = false;
  let mouseOver = false;
  $: showChartForType =
    displayCol.type === "number" ||
    displayCol.type === "categorical" ||
    displayCol.type === "date";

  function getSearchInfo(col: Column, dsInfo: DatasetInfo): string {
    if (
      col.table_name &&
      col.table_name !== dsInfo.name &&
      (col.type === "categorical" || col.type === "text")
    ) {
      return col.table_name;
    }

    return dsInfo.name;
  }
</script>

<div
  on:mouseover={() => (mouseOver = true)}
  on:focus={() => (mouseOver = true)}
  on:mouseout={() => (mouseOver = false)}
  on:blur={() => (mouseOver = false)}
  role="group"
>
  <!-- shadow is green-600 -->
  <button
    class={`space-between flex h-9 w-full items-center justify-between border-t-2 border-secondary-200 gap-2 px-2 hover:bg-gray-200 ${displayCol.derived_how ? "shadow-[inset_4px_0_0_0_#16a34a]" : ""}`}
    class:bg-gray-100={active}
    on:click={() => {
      active = !active;
    }}
  >
    <DataTypeIcon {id} type={displayCol.type} />

    <p
      class:font-medium={active}
      class="max-w-sm overflow-hidden text-ellipsis text-left"
    >
      {displayCol.name}
    </p>
    {#if displayCol.derived_from}
      <div class="text-gray-400 flex items-center">
        <span>(from {displayCol.derived_from}</span>
        <span class="ml-1">
          <DerivedIcon derived_how={displayCol.derived_how} />
        </span>
        <span>)</span>
      </div>
    {/if}

    <div class="grow" />

    {#if colSummary?.null_percentage}
      <NullDisplay nullPercentage={parseFloat(colSummary.null_percentage)} />
    {/if}
  </button>
  <div class="w-full pl-4 py-1 mb-2" class:hidden={!active}>
    {#if displayCol.table_name && displayCol.table_name !== $datasetInfo.name}
      {#if displayCol.type === "categorical" || displayCol.type === "text"}
        <CategoricalChart
          mainDatasetName={displayCol.table_name}
          columnName={displayCol.name}
          excludeList={$datasetInfo.columns.find(
            (c) => c.name === displayCol.derived_from,
          )?.type === "text"
            ? $stopwords
            : undefined}
          plotNulls={true}
          isDerivedTable={true}
          showBackground={$showBackgroundDistMap[displayCol.name]}
        />
      {:else}
        Not currently supporting quantitative columns from another table...
      {/if}
    {:else if displayCol.type === "number"}
      <Histogram
        mainDatasetName={$datasetInfo.name}
        showBackground={$showBackgroundDistMap[displayCol.name]}
        columnName={displayCol.name}
      />
    {:else if displayCol.type === "categorical"}
      <CategoricalChart
        mainDatasetName={$datasetInfo.name}
        showBackground={$showBackgroundDistMap[displayCol.name]}
        columnName={displayCol.name}
      />
    {:else if displayCol.type === "date"}
      <DateChart
        mainDatasetName={$datasetInfo.name}
        columnName={displayCol.name}
      />
    {:else if displayCol.type === "text"}
      <span></span>
    {/if}

    <div class="flex gap-1 mx-2">
      <div class="grow">
        <Search
          tableName={getSearchInfo(displayCol, $datasetInfo)}
          column={displayCol}
        />
      </div>
      {#if showChartForType}
        <button
          class="hover:bg-secondary-200 text-gray-500 p-1 rounded inline"
          id={"chartSettings-" + id}
          on:click={() => {
            showSettings = !showSettings;
          }}
        >
          <CogOutline size="xs" />
        </button>
      {/if}
    </div>

    {#if showSettings}
      <div class="px-4 py-2 mx-2 mt-2 rounded bg-gray-100 flex">
        <Toggle
          size="small"
          bind:checked={$showBackgroundDistMap[displayCol.name]}
        />
        <span class="text-sm text-gray-500"> Show original distribution </span>
      </div>
    {/if}
  </div>
</div>
