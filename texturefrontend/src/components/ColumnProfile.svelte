<script lang="ts">
  import type { ColumnSummary } from "../shared/types";
  import type { Column } from "../backendapi/models/Column";
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

  export let displayCol: Column;
  export let colSummary: ColumnSummary | undefined;

  let id = getUUID();

  let active = true;
  let showSettings = false;
  let mouseOver = false;
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
    class={`space-between flex h-9 w-full items-center justify-between border-t-2 border-gray-100 gap-2 px-2 hover:bg-gray-100 ${displayCol.derived_how ? "shadow-[inset_4px_0_0_0_#16a34a]" : ""}`}
    class:bg-gray-50={active}
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
  <div class="w-full pl-4 py-1 relative" class:hidden={!active}>
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
    {:else}
      <div>
        {displayCol.name}: Unsupported column type ({displayCol.type})
      </div>
    {/if}

    <button
      class="hover:bg-secondary-100 text-gray-500 p-1 rounded absolute bottom-2 right-4"
      id={"chartSettings-" + id}
      class:hidden={!mouseOver}
      on:click={() => {
        showSettings = !showSettings;
      }}
    >
      <CogOutline size="xs" />
    </button>

    {#if showSettings}
      <div class="mb-2">
        <Toggle
          size="small"
          class="mt-2"
          bind:checked={$showBackgroundDistMap[displayCol.name]}
        >
          Show original distribution
        </Toggle>
      </div>
    {/if}
  </div>
</div>
