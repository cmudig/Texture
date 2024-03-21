<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import type { ColumnSummary } from "./shared/types";
  import type { DatasetInfo } from "./backendapi";
  import {
    mosaicSelection,
    datasetInfo,
    databaseConnection,
    compareSimilarID,
  } from "./stores";
  import Sidebar from "./components/Sidebar.svelte";
  import DataDisplay from "./components/table/DataDisplay.svelte";
  import Search from "./components/Search.svelte";
  import SimilarView from "./components/SimilarView.svelte";
  import ColumnTransformModal from "./components/addColumn/ColumnTransformModal.svelte";
  import { Popover, Spinner } from "flowbite-svelte";
  import { AdjustmentsHorizontalOutline } from "flowbite-svelte-icons";
  import OptionsBar from "./components/OptionsBar.svelte";
  import SettingsPanel from "./components/settings/SettingsPanel.svelte";

  // Locals
  let datasets: Record<string, DatasetInfo>;
  let currentDatasetName: string;
  let currentColToggleStates: Record<string, boolean> = {};
  let datasetSize: number;
  let showAddColModal = false;
  let datasetColSummaries: Map<string, ColumnSummary>;
  let dataPromise: Promise<any> = populateDataTables();

  async function populateDataTables(
    datasetName?: string,
    resetCrossfilter = true,
  ): Promise<void> {
    let d = await databaseConnection.api.readDatasetInfo();
    datasets = d;

    if (datasetName && datasetName in datasets) {
      currentDatasetName = datasetName;
    } else {
      currentDatasetName = Object.keys(datasets)[0];
    }

    return setDataset(resetCrossfilter);
  }

  async function setDataset(resetCrossfilter = true) {
    const info = datasets[currentDatasetName];
    $datasetInfo = info;

    currentColToggleStates = $datasetInfo.columns.reduce(
      (acc: Record<string, boolean>, col) => {
        acc[col.name] = true;

        return acc;
      },
      {},
    );

    // create new brush to clear selections from old dataset
    if (resetCrossfilter) {
      $mosaicSelection = vg.Selection.crossfilter();
    }
    datasetSize = await databaseConnection.getCount(info.name);
    datasetColSummaries = await databaseConnection.getColSummaries(info.name);
  }
</script>

<div class="h-screen flex flex-col">
  <!-- Top bar -->
  <div class="flex gap-2 bg-gradient-to-r from-primary-900 to-primary-500 p-4">
    <span class="self-center whitespace-nowrap text-2xl text-white">
      Text<span class="font-light ml-1"> Profiler</span>
    </span>
    <div class="grow" />

    <Search
      columnNames={$datasetInfo?.columns
        .filter((col) => col.type === "text")
        .map((col) => col.name)}
      tableName={$datasetInfo?.name}
    />

    <!-- <FilePlusSolid
    id="addDatasetIcon"
    size="md"
    class="mx-1 self-center text-white hover:text-primary-700"
    on:click={() => (showAddDataModal = true)}
  />
  <Tooltip class="z-10" triggeredBy="#addDatasetIcon" type="light"
    >Add new dataset</Tooltip
  > -->

    <AdjustmentsHorizontalOutline
      id="settingsToggle"
      size="md"
      class="mx-1 self-center text-white hover:text-gray-300"
    />
    <Popover
      triggeredBy="#settingsToggle"
      class="z-10 w-80 bg-white text-sm font-light text-gray-500"
      title="Settings"
    >
      <SettingsPanel
        {datasets}
        updateData={() => {
          dataPromise = setDataset();
        }}
        bind:currentDatasetName
        bind:currentColToggleStates
      />
    </Popover>

    <!-- <UploadDataModal
    bind:panelOpen={showAddDataModal}
    finishedUploadHandler={(name) => {
      dataPromise = populateDataTables(name);
    }}
  /> -->

    <ColumnTransformModal
      bind:panelOpen={showAddColModal}
      finishedCommitHandler={() => {
        dataPromise = populateDataTables(currentDatasetName, false);
      }}
    />
  </div>

  <!-- Main content -->
  {#await dataPromise}
    <div class="p-4">
      <Spinner />
    </div>
  {:then}
    <div class="flex flex-1 overflow-hidden">
      <div class="w-[450px] shrink-0 overflow-auto border-r border-gray-300">
        <Sidebar bind:showAddColModal {datasetColSummaries} />
      </div>
      <div class="flex-1 min-w-[450px] overflow-auto pt-2 bg-gray-50">
        {#if $compareSimilarID !== undefined}
          <SimilarView
            similarDocID={$compareSimilarID}
            clearFunc={() => {
              $compareSimilarID = undefined;
            }}
          />
        {:else}
          <DataDisplay {currentColToggleStates}>
            <svelte:fragment slot="navBar">
              <OptionsBar {datasetSize} />
            </svelte:fragment>
          </DataDisplay>
        {/if}
      </div>
    </div>
  {:catch error}
    <div>Error: {error.message}</div>
  {/await}
</div>
