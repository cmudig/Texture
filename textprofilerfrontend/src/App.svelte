<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import type { ColumnSummary } from "./shared/types";
  import type { DatasetInfo } from "./backendapi/models/DatasetInfo";
  import {
    mosaicSelection,
    datasetInfo,
    showBackgroundDist,
    filteredCount,
    databaseConnection,
    compareSimilarID,
  } from "./stores";
  import Sidebar from "./components/Sidebar.svelte";
  import DataDisplay from "./components/table/DataDisplay.svelte";
  import Search from "./components/Search.svelte";
  import SimilarView from "./components/SimilarView.svelte";
  import FilterBar from "./components/FilterBar.svelte";
  import StopwordEditor from "./components/settings/StopwordEditor.svelte";
  import ColumnTransformModal from "./components/addColumn/ColumnTransformModal.svelte";
  import SaveTableToFile from "./components/SaveTableToFile.svelte";
  import {
    Select,
    Popover,
    Toggle,
    Label,
    Tooltip,
    Spinner,
  } from "flowbite-svelte";
  import {
    AdjustmentsHorizontalOutline,
    CirclePlusSolid,
  } from "flowbite-svelte-icons";
  import { formatNumber } from "./shared/format";

  // Locals
  let datasets: Record<string, DatasetInfo>;
  let currentDatasetName: string;
  let currentColToggleStates: Record<string, boolean> = {};
  let datasetSize: number;
  let showAddColModal = false;
  let datasetColSummaries: Map<string, ColumnSummary>;
  let dataPromise: Promise<any> = populateDataTables();

  async function populateDataTables(datasetName?: string): Promise<void> {
    let d = await databaseConnection.api.readDatasetInfo();
    datasets = d;

    if (datasetName && datasetName in datasets) {
      currentDatasetName = datasetName;
    } else {
      currentDatasetName = Object.keys(datasets)[0];
    }

    return setDataset();
  }

  async function setDataset() {
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
    $mosaicSelection = vg.Selection.crossfilter();
    datasetSize = await databaseConnection.getCount(info.name);
    datasetColSummaries = await databaseConnection.getColSummaries(info.name);
  }

  function updateData() {
    dataPromise = setDataset();
  }
</script>

<div
  class="flex flex-row gap-2 bg-gradient-to-r from-primary-700 to-secondary-600 p-4"
>
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

  <CirclePlusSolid
    id="addColIcon"
    size="md"
    class="mx-1 self-center text-white hover:text-gray-300"
    on:click={() => (showAddColModal = true)}
  />
  <Tooltip class="z-10" triggeredBy="#addColIcon" type="light"
    >Extract new column</Tooltip
  >

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
    <div class="flex flex-col gap-4 p-3">
      <div class="flex flex-col gap-2 pb-2 border-b-2 border-grey-300">
        <h3>Dataset</h3>

        <Select
          size="sm"
          items={Object.values(datasets).map((k) => ({
            value: k.name,
            name: k.origin === "example" ? `${k.name} (example)` : k.name,
          }))}
          placeholder="Select dataset"
          bind:value={currentDatasetName}
          on:change={updateData}
        />

        <SaveTableToFile />
      </div>

      <div class="flex flex-col gap-2 pb-2 border-b-2 border-grey-300">
        <h3>Stopwords</h3>
        <StopwordEditor />
      </div>

      <div class="flex flex-col gap-2">
        <h3>Display Settings</h3>

        <div>
          <Label>Background distributions</Label>

          <Toggle class="mt-2" bind:checked={$showBackgroundDist}
            >Show in plot</Toggle
          >
        </div>

        <div>
          <Label>Display in table</Label>
          <div class="mt-2 flex flex-col gap-1">
            {#each $datasetInfo.columns as col}
              <Toggle bind:checked={currentColToggleStates[col.name]}>
                <span class="overflow-hidden text-ellipsis">
                  {col.name}
                </span>
              </Toggle>
            {/each}
          </div>
        </div>
      </div>
    </div>
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
      dataPromise = populateDataTables(currentDatasetName);
    }}
  />
</div>

{#await dataPromise}
  <div class="p-4">
    <Spinner />
  </div>
{:then}
  <!-- Dataset info -->
  <div
    class="flex gap-2 justify-end pr-7 py-2 text-gray-500 bg-gray-100 min-h-14"
  >
    <div class="grow px-2 self-center">
      <FilterBar />
    </div>
    <div class="text-md self-center">
      {formatNumber($filteredCount)} / {formatNumber(datasetSize)} rows
    </div>

    <div class="text-md self-center font-semibold">
      {currentDatasetName}
    </div>
  </div>

  <div class="flex flex-row">
    <div class="h-screen w-[450px] shrink-0 overflow-scroll">
      <Sidebar {datasetColSummaries} />
    </div>
    <div class="h-screen grow overflow-scroll border-l-2 border-slate-50">
      {#if $compareSimilarID !== undefined}
        <SimilarView
          similarDocID={$compareSimilarID}
          clearFunc={() => {
            $compareSimilarID = undefined;
          }}
        />
      {:else}
        <DataDisplay {currentColToggleStates} />
      {/if}
    </div>
  </div>
{:catch error}
  <div>Error: {error.message}</div>
{/await}
