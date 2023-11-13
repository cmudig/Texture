<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { datasets } from "./shared/colConfig";
  import type { DatabaseConnection } from "./database/db";
  import Sidebar from "./components/Sidebar.svelte";
  import InstanceView from "./components/InstanceView.svelte";

  export let databaseConnection: DatabaseConnection;

  // selectors
  let selectedValue: string = "opus";
  let textColumns: string[];
  let datasetName = selectedValue;

  const brush = vg.Selection.crossfilter();

  async function setDataset() {
    const info = datasets[selectedValue];
    await databaseConnection.initAndLoad(info.name, info.filename);
    textColumns = info.textColumns;
    datasetName = info.name;
  }

  function updateData() {
    dataPromise = setDataset();
  }

  let dataPromise: Promise<any> = setDataset();
</script>

<div class="bg-gradient-to-r from-blue-100 to-blue-700 p-5 flex gap-2 flex-row">
  <span
    class="self-center whitespace-nowrap text-2xl font-semibold text-blue-900"
    >Text Clean</span
  >
  <div class="grow" />
  <div class="self-center">
    <span class="text-white text-xl pr-2">Dataset: </span>
    <select
      class="h-10 text-gray-900 bg-gray-50 border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
      bind:value={selectedValue}
      on:change={updateData}
    >
      <option value="opus">Opus</option>
      <option value="dolly">Dolly</option>
      <option value="squad">Squad</option>
    </select>
  </div>
</div>

{#await dataPromise}
  <div>Loading data...</div>
{:then}
  <div class="flex flex-row">
    <div class="w-1/3 h-screen overflow-scroll">
      <Sidebar {textColumns} {datasetName} {brush} />
    </div>
    <div class="w-2/3 h-screen overflow-scroll">
      <InstanceView {textColumns} {datasetName} {brush} />
    </div>
  </div>
{:catch error}
  <div>Error: {error.message}</div>
{/await}
