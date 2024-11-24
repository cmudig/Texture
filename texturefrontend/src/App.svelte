<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import type { ColumnSummary } from "./shared/types";
  import {
    mosaicSelection,
    datasetSchema,
    databaseConnection,
    showBackgroundDistMap,
    filteredCount,
    setSchema,
  } from "./stores";
  import Sidebar from "./components/Sidebar.svelte";
  import TableView from "./components/table/TableView.svelte";
  import ColumnTransformModal from "./components/addColumn/ColumnTransformModal.svelte";
  import { Popover, Spinner } from "flowbite-svelte";
  import { AdjustmentsHorizontalOutline } from "flowbite-svelte-icons";
  import SettingsPanel from "./components/settings/SettingsPanel.svelte";
  import TextureIcon from "./components/icons/TextureIcon.svelte";
  import FilterBar from "./components/FilterBar.svelte";
  import TableSort from "./components/table/TableSort.svelte";
  import { formatNumber } from "./shared/format";

  // Locals
  let datasetSize: number;
  let showAddColModal = false;
  let datasetColSummaries: Map<string, ColumnSummary>;
  let readyToLoad: Promise<any> = initialLoad();
  let allowDeriveNew = false;

  async function initialLoad() {
    await setSchema();

    $showBackgroundDistMap = $datasetSchema.columns.reduce(
      (acc: Record<string, boolean>, col) => {
        acc[col.name] = col.name !== "word";

        return acc;
      },
      {},
    );

    // create new brush to clear selections from old dataset
    $mosaicSelection = vg.Selection.crossfilter();
    datasetSize = await databaseConnection.getCount($datasetSchema.name);
    datasetColSummaries =
      await databaseConnection.getColSummaries($datasetSchema);
  }
</script>

<div class="h-screen flex flex-col">
  <!-- Top bar -->
  <div class="flex gap-2 border-b-2 border-gray-300 bg-secondary-200 p-4">
    <div class="mr-8"><TextureIcon size={40} /></div>

    <div class="grow self-center">
      <FilterBar />
    </div>
    <div class="text-md self-center">
      {formatNumber($filteredCount)} / {formatNumber(datasetSize)} documents
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
      <SettingsPanel bind:allowDeriveNew />
    </Popover>

    <ColumnTransformModal
      bind:panelOpen={showAddColModal}
      finishedCommitHandler={() => {
        showAddColModal = false; // close modal when complete
      }}
    />
  </div>

  <!-- Main content -->
  {#await readyToLoad}
    <div class="p-4">
      <Spinner />
    </div>
  {:then}
    <div class="flex flex-1 overflow-hidden bg-gray-50">
      <div class="w-[450px] shrink-0 overflow-auto border-r-2 border-gray-300">
        <Sidebar bind:showAddColModal {allowDeriveNew} {datasetColSummaries} />
      </div>
      <div class="flex-1 min-w-[450px] overflow-auto">
        <TableView />
      </div>
    </div>
  {:catch error}
    <div class="p-4">
      <span class="italic text-red-600">Error getting data:</span>
      {error.message}
    </div>
  {/await}
</div>
