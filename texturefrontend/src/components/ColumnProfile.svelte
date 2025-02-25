<script lang="ts">
  import type { ColumnSummary } from "../shared/types";
  import DataTypeIcon from "./icons/DataTypeIcon.svelte";
  import Histogram from "./charts/Histogram.svelte";
  import CategoricalChart from "./charts/CategoricalChart.svelte";
  import DateChart from "./charts/DateChart.svelte";
  import NullDisplay from "./NullDisplay.svelte";
  import CardinalityDisplay from "./CardinalityDisplay.svelte";
  import {
    datasetSchema,
    showBackgroundDistMap,
    projectionColorColumn,
  } from "../stores";
  import { getUUID } from "../shared/utils";
  import DerivedIcon from "./icons/DerivedIcon.svelte";
  import { CogOutline } from "flowbite-svelte-icons";
  import Search from "./Search.svelte";
  import type { Column } from "../backendapi";
  import Toggle from "./layout/Toggle.svelte";

  export let displayCol: Column;
  export let colSummary: ColumnSummary | undefined;

  let id = getUUID();

  let active = true;
  let showSettings = false;
  $: showChartForType =
    displayCol.type === "number" ||
    displayCol.type === "categorical" ||
    displayCol.type === "date";
</script>

<Toggle bind:active>
  <svelte:fragment slot="title">
    {#if displayCol.derivedSchema?.derived_how}
      <div class="w-2 h-8 bg-green-600 -ml-2" />
    {/if}

    <DataTypeIcon {id} type={displayCol.type} />

    <p
      class:font-medium={active}
      class="overflow-hidden text-ellipsis text-left grow"
    >
      {displayCol.name}
    </p>
    {#if displayCol.derivedSchema?.derived_how}
      <div class="text-gray-400 flex items-center">
        <span>(from {displayCol.derivedSchema.derived_from}</span>
        <span class="ml-1">
          <DerivedIcon derived_how={displayCol.derivedSchema.derived_how} />
        </span>
        <span>)</span>
      </div>
    {/if}

    {#if colSummary?.cardinality !== undefined}
      <CardinalityDisplay cardinality={colSummary.cardinality} />
    {/if}
    {#if colSummary?.null_percentage !== undefined}
      <div class="-ml-1">
        <NullDisplay nullPercentage={parseFloat(colSummary.null_percentage)} />
      </div>
    {/if}
  </svelte:fragment>

  <div slot="body" class="w-full pl-4 py-1 mb-2">
    {#if displayCol.extra?.["search_id"] != undefined}
      Similarity to id: {displayCol.extra?.["search_id"]}
    {/if}
    {#if displayCol.extra?.["search_query"] != undefined}
      <span class="italic">Similarity to:</span>
      "{displayCol.extra?.["search_query"]}"
    {/if}

    {#if displayCol.type === "number"}
      <Histogram
        mainDatasetName={displayCol.derivedSchema?.table_name ??
          $datasetSchema.name}
        columnName={displayCol.name}
        showBackground={$showBackgroundDistMap[displayCol.name]}
        shouldBin={colSummary?.cardinality == undefined ||
          colSummary.cardinality >= 10}
      />
    {:else if displayCol.type === "categorical"}
      <CategoricalChart
        mainDatasetName={displayCol.derivedSchema?.table_name ??
          $datasetSchema.name}
        columnName={displayCol.name}
        showBackground={$showBackgroundDistMap[displayCol.name]}
        colorColName={$projectionColorColumn === displayCol.name
          ? displayCol.name
          : undefined}
        initialCardinality={colSummary
          ? colSummary.cardinality +
            Number(parseFloat(colSummary.null_percentage) > 0)
          : undefined}
      />
    {:else if displayCol.type === "date"}
      <DateChart
        mainDatasetName={displayCol.derivedSchema?.table_name ??
          $datasetSchema.name}
        columnName={displayCol.name}
      />
    {:else if displayCol.type === "text"}
      <span></span>
    {/if}

    <div class="flex gap-1 mx-2">
      <div class="grow">
        <Search
          tableName={displayCol.derivedSchema?.table_name ??
            $datasetSchema.name}
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
      <div class="px-4 py-2 mx-2 mt-2 rounded bg-gray-100">
        <label class="flex items-center gap-2 text-sm text-gray-500">
          <input
            type="checkbox"
            class="w-4 h-4 bg-gray-100 border-gray-300 dark:ring-offset-gray-800 focus:ring-2 me-2 dark:bg-gray-700 dark:border-gray-600 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600"
            bind:checked={$showBackgroundDistMap[displayCol.name]}
          />
          <span> Show background distribution </span>
        </label>
      </div>
    {/if}
  </div>
</Toggle>
