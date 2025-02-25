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
    sidebarWidth,
  } from "./stores";
  import Sidebar from "./components/Sidebar.svelte";
  import TableView from "./components/table/TableView.svelte";
  import ColumnTransformModal from "./components/addColumn/ColumnTransformModal.svelte";
  import { Popover, Spinner } from "flowbite-svelte";
  import {
    AdjustmentsHorizontalOutline,
    BullhornOutline,
  } from "flowbite-svelte-icons";
  import SettingsPanel from "./components/settings/SettingsPanel.svelte";
  import TextureIcon from "./components/icons/TextureIcon.svelte";
  import FilterBar from "./components/FilterBar.svelte";
  import TableSort from "./components/table/TableSort.svelte";
  import { formatNumber } from "./shared/format";
  import Draggable from "./components/layout/Draggable.svelte";

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
        acc[col.name] = false;

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
  <div
    class="flex items-center gap-4 border-b-2 border-gray-300 bg-secondary-200 p-4"
  >
    <TextureIcon size={40} />

    <div class="grow">
      <FilterBar />
    </div>
    <div>
      {formatNumber($filteredCount)} / {formatNumber(datasetSize)} documents
    </div>
    <TableSort />
    <AdjustmentsHorizontalOutline
      title="Settings"
      id="settingsToggle"
      size="md"
      class="text-gray-500 hover:text-gray-700"
    />
    <a
      href="https://forms.gle/seACEDSvJLey17M57"
      target="_blank"
      class="text-gray-500 hover:text-highlight-700"
      title="Feedback form"
    >
      <BullhornOutline id="settingsToggle" size="md" />
    </a>

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
      <!-- <div class="w-[450px] shrink-0 overflow-auto border-r-2 border-gray-300">
        <Sidebar bind:showAddColModal {allowDeriveNew} {datasetColSummaries} />
      </div> -->

      <Draggable minWidth={300} bind:width={$sidebarWidth}>
        <Sidebar bind:showAddColModal {allowDeriveNew} {datasetColSummaries} />
      </Draggable>
      <div class="flex-1 min-w-[450px] overflow-y-auto">
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
