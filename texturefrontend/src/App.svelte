<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import type { ColumnSummary } from "./shared/types";
  import type { DatasetInfo } from "./backendapi";
  import {
    mosaicSelection,
    datasetInfo,
    databaseConnection,
    compareSimilarID,
    showBackgroundDistMap,
    filteredCount,
  } from "./stores";
  import Sidebar from "./components/Sidebar.svelte";
  import DataDisplay from "./components/table/DataDisplay.svelte";
  import SimilarView from "./components/SimilarView.svelte";
  import ColumnTransformModal from "./components/addColumn/ColumnTransformModal.svelte";
  import { Popover, Spinner } from "flowbite-svelte";
  import { AdjustmentsHorizontalOutline } from "flowbite-svelte-icons";
  import SettingsPanel from "./components/settings/SettingsPanel.svelte";
  import TextureIcon from "./components/icons/TextureIcon.svelte";
  import FilterBar from "./components/FilterBar.svelte";
  import TableSort from "./components/table/TableSort.svelte";
  import { formatNumber } from "./shared/format";

  // Locals
  let datasets: Record<string, DatasetInfo>;
  let currentDatasetName: string;
  let currentColToggleStates: Record<string, boolean> = {}; // TODO create ignore list by name to not plot columns with umap_x, umap_y, or id
  let datasetSize: number;
  let showAddColModal = false;
  let datasetColSummaries: Map<string, ColumnSummary>;
  let dataPromise: Promise<any> = populateDataTables();

  async function populateDataTables(
    datasetName?: string,
    resetCrossfilter = true,
  ): Promise<void> {
    let d = await databaseConnection.api.readDatasetInfo();

    if (Object.keys(d).length === 0) {
      throw new Error(
        "No datasets found! Please pass a dataset to texture.run()",
      );
    }

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

    $showBackgroundDistMap = $datasetInfo.columns.reduce(
      (acc: Record<string, boolean>, col) => {
        if (col.name === "word") {
          acc[col.name] = false;
        } else {
          acc[col.name] = true;
        }

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
  <div class="flex gap-2 border-b-4 border-secondary-400 bg-secondary-200 p-4">
    <div class="mr-8"><TextureIcon size={40} /></div>

    <div class="grow self-center">
      <FilterBar />
    </div>
    <div class="text-md self-center">
      {formatNumber($filteredCount)} / {formatNumber(datasetSize)} rows
    </div>

    <TableSort />

    <AdjustmentsHorizontalOutline
      id="settingsToggle"
      size="md"
      class="ml-4 self-center text-gray-500 hover:text-gray-700"
    />
    <Popover
      triggeredBy="#settingsToggle"
      trigger="click"
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

    <ColumnTransformModal
      bind:panelOpen={showAddColModal}
      finishedCommitHandler={() => {
        dataPromise = populateDataTables(currentDatasetName, false);
        showAddColModal = false; // close modal when complete
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
      <div class="flex-1 min-w-[450px] overflow-auto bg-gray-50">
        {#if $compareSimilarID !== undefined}
          <SimilarView
            similarDocID={$compareSimilarID}
            clearFunc={() => {
              $compareSimilarID = undefined;
            }}
          />
        {:else}
          <DataDisplay {currentColToggleStates}>
            <svelte:fragment slot="navBar"></svelte:fragment>
          </DataDisplay>
        {/if}
      </div>
    </div>
  {:catch error}
    <div class="p-4">
      <span class="italic text-red-600">Error fetching data:</span>
      {error.message}
    </div>
  {/await}
</div>
