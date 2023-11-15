<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { datasets } from "./shared/colConfig";
  import type { DatabaseConnection } from "./database/db";
  import type { DatasetInfo, TableOption } from "./shared/types";
  import Sidebar from "./components/Sidebar.svelte";
  import InstanceView from "./components/InstanceView.svelte";
  import { brush } from "./stores";

  export let databaseConnection: DatabaseConnection;

  let selectedValue: string = Object.keys(datasets)[0];
  let datasetInfo: DatasetInfo;
  let tableOption: TableOption = "all";

  async function setDataset() {
    const info = datasets[selectedValue];
    await databaseConnection.initAndLoad(info.name, info.filename);
    datasetInfo = info;
    // create new brush to clear selections from old dataset
    $brush = vg.Selection.crossfilter();
  }

  function updateData() {
    dataPromise = setDataset();
  }

  function resetBrush() {
    $brush = vg.Selection.crossfilter();
  }

  let dataPromise: Promise<any> = setDataset();
</script>

<div class="bg-gradient-to-r from-blue-100 to-blue-700 p-5 flex gap-2 flex-row">
  <span
    class="self-center whitespace-nowrap text-2xl font-semibold text-blue-900"
    >Text Clean</span
  >
  <div class="grow" />

  <button class="py-2 px-4 rounded bg-white" on:click={resetBrush}>
    Reset filters
  </button>
  <div class="self-center">
    <span class="text-white text-xl pr-2">Table: </span>
    <select
      class="text-gray-900 bg-gray-50 border border-gray-300 rounded focus:ring-primary-500 focus:border-primary-500"
      bind:value={tableOption}
    >
      <option value="all">All cols</option>
      <option value="text">Only text</option>
    </select>
  </div>
  <div class="self-center">
    <span class="text-white text-xl pr-2">Data: </span>
    <select
      class="text-gray-900 bg-gray-50 border border-gray-300 rounded focus:ring-primary-500 focus:border-primary-500"
      bind:value={selectedValue}
      on:change={updateData}
    >
      {#each Object.keys(datasets) as datasetKey}
        <option value={datasets[datasetKey].name}
          >{datasets[datasetKey].name}</option
        >
      {/each}
    </select>
  </div>
</div>

{#await dataPromise}
  <div class="p-4">Loading data...</div>
{:then}
  <div class="flex flex-row">
    <div class="w-1/3 h-screen overflow-scroll">
      <Sidebar {datasetInfo} />
    </div>
    <div class="w-2/3 h-screen overflow-scroll">
      <InstanceView {datasetInfo} {tableOption} />
    </div>
  </div>
{:catch error}
  <div>Error: {error.message}</div>
{/await}
