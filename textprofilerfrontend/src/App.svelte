<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import type { ColumnSummary } from "./shared/types";
  import type { DatasetInfo } from "./backendapi/models/DatasetInfo";
  import {
    filters,
    selectionDisplay,
    showBackgroundDist,
    filteredCount,
    databaseConnection,
  } from "./stores";
  import Sidebar from "./components/Sidebar.svelte";
  import Table from "./components/table/Table.svelte";
  import FilterDisplay from "./components/FilterDisplay.svelte";
  import UploadDataModal from "./components/uploadData/UploadDataModal.svelte";
  import Search from "./components/Search.svelte";
  import {
    Button,
    Select,
    Popover,
    Toggle,
    Label,
    Drawer,
    CloseButton,
    Tooltip,
    Spinner,
    Tabs,
    TabItem,
  } from "flowbite-svelte";
  import {
    AdjustmentsHorizontalOutline,
    FilterSolid,
    ChartMixedSolid,
    TableSolid,
    FilePlusSolid,
  } from "flowbite-svelte-icons";
  import { sineIn } from "svelte/easing";
  import { formatNumber } from "./shared/format";

  // Locals
  let datasets: Record<string, DatasetInfo>;
  let currentDatasetName: string;
  let datasetInfo: DatasetInfo;
  // let currentColumns: Column[] = [];
  let currentColToggleStates: Record<string, boolean> = {};
  let datasetSize: number;
  let filterPanelHidden = true;
  let showAddDataModel = false;
  let datasetColSummaries: ColumnSummary[];
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
    datasetInfo = info;

    currentColToggleStates = datasetInfo.column_info.reduce(
      (acc: Record<string, boolean>, col) => {
        // Only show text columns in table view by default
        if (col.type === "text") {
          acc[col.name] = true;
        } else {
          acc[col.name] = false;
        }
        return acc;
      },
      {},
    );

    // create new brush to clear selections from old dataset
    $filters = {
      brush: vg.Selection.crossfilter(),
      datasetName: info.name,
      joinDatasetInfo: info.joinDatasetInfo,
    };

    datasetSize = await databaseConnection.getCount(info.name);
    datasetColSummaries = await databaseConnection.getColSummaries(info.name);
  }

  function updateData() {
    dataPromise = setDataset();
  }

  function resetBrush() {
    $filters = {
      brush: vg.Selection.crossfilter(),
      datasetName: datasetInfo.name,
      joinDatasetInfo: datasetInfo.joinDatasetInfo,
    };
  }
</script>

<div class="flex flex-row gap-2 bg-gradient-to-r from-blue-100 to-blue-700 p-5">
  <span
    class="self-center whitespace-nowrap text-2xl font-semibold text-blue-900"
    >Text Profiler</span
  >
  <div class="grow" />

  <Search
    columnNames={datasetInfo?.column_info
      .filter((col) => col.type === "text")
      .map((col) => col.name)}
  />

  <FilePlusSolid
    id="addDatasetIcon"
    size="md"
    class="mx-1 self-center text-white hover:text-primary-700"
    on:click={() => (showAddDataModel = true)}
  />
  <Tooltip class="z-10" triggeredBy="#addDatasetIcon" type="light"
    >Add new dataset</Tooltip
  >

  <AdjustmentsHorizontalOutline
    id="settingsToggle"
    size="md"
    class="mx-1 self-center text-white hover:text-primary-700"
  />
  <Popover
    triggeredBy="#settingsToggle"
    class="z-10 w-80 bg-white text-sm font-light text-gray-500"
    title="Settings"
  >
    <div class="flex flex-col gap-2 p-3">
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

      <div class="mt-2">
        <Label>Background distributions</Label>

        <Toggle class="mt-2" bind:checked={$showBackgroundDist}
          >Show in plot</Toggle
        >
      </div>

      <div class="mt-2">
        <Label>Display in table</Label>
        <div class="mt-2 flex flex-col gap-1">
          {#each datasetInfo.column_info as col}
            <Toggle bind:checked={currentColToggleStates[col.name]}>
              <span class="overflow-hidden text-ellipsis">
                {col.name}
              </span>
            </Toggle>
          {/each}
        </div>
      </div>
    </div>
  </Popover>

  <UploadDataModal
    bind:panelOpen={showAddDataModel}
    finishedUploadHandler={(name) => {
      dataPromise = populateDataTables(name);
    }}
  />

  <FilterSolid
    id="filterToggle"
    on:click={() => (filterPanelHidden = false)}
    class="mx-1 self-center text-white hover:text-primary-700"
    size="md"
  />
  <Tooltip class="z-10" triggeredBy="#filterToggle" type="light"
    >Display filters</Tooltip
  >
</div>

{#await dataPromise}
  <div class="p-4">
    <Spinner />
  </div>
{:then}
  <div>
    <Drawer
      placement="right"
      transitionType="fly"
      transitionParams={{
        x: 320,
        duration: 200,
        easing: sineIn,
      }}
      bind:hidden={filterPanelHidden}
      id="sidebar-filter-display"
    >
      <div class="flex items-center">
        <h3
          id="drawer-label"
          class="mb-4 inline-flex items-center text-base font-semibold"
        >
          Applied filters
        </h3>
        <CloseButton
          on:click={() => (filterPanelHidden = true)}
          class="mb-4 dark:text-white"
        />
      </div>
      <div class="flex flex-col gap-2">
        {#if Object.keys($selectionDisplay).length === 0}
          <div class="italic">No filters applied</div>
        {:else}
          {#each Object.keys($selectionDisplay) as k}
            <FilterDisplay colName={k} filterRange={$selectionDisplay[k]} />
          {/each}
        {/if}
      </div>
      <div>
        <Button class="mt-6 w-full" on:click={resetBrush}
          >Reset all filters</Button
        >
      </div>
    </Drawer>
  </div>

  <!-- Dataset info -->
  <div class="flex gap-2 justify-end pr-7 py-2 text-gray-500 bg-gray-100">
    <div class="text-md self-center">
      {formatNumber($filteredCount)} / {formatNumber(datasetSize)} rows
    </div>

    <div class="text-md self-center font-semibold">
      {currentDatasetName}
    </div>
  </div>

  <div class="flex flex-row">
    <div class="h-screen w-1/3 overflow-scroll">
      <Tabs style="underline" contentClass="">
        <TabItem open>
          <div slot="title" class="flex items-center gap-2">
            <ChartMixedSolid size="sm" />
            Explore
          </div>

          <Sidebar {datasetInfo} {datasetColSummaries} />
        </TabItem>
      </Tabs>
    </div>
    <div class="h-screen w-2/3 overflow-scroll">
      <Tabs style="underline" contentClass="border-l-2 border-slate-50">
        <TabItem open>
          <div slot="title" class="flex items-center gap-2">
            <TableSolid size="sm" />
            Table
          </div>

          <Table
            mainDatasetName={datasetInfo.name}
            joinDatasetInfo={datasetInfo.joinDatasetInfo}
            {currentColToggleStates}
          />
        </TabItem>
      </Tabs>
    </div>
  </div>
{:catch error}
  <div>Error: {error.message}</div>
{/await}
