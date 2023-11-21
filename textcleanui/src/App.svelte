<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { datasets } from "./shared/colConfig";
  import type { DatabaseConnection } from "./database/db";
  import type { DatasetInfo, TableOption } from "./shared/types";
  import { filters } from "./stores";

  import Sidebar from "./components/Sidebar.svelte";
  import InstanceView from "./components/InstanceView.svelte";
  import { Button, Select, Popover } from "flowbite-svelte";
  import {
    AdjustmentsHorizontalOutline,
    InfoCircleOutline,
  } from "flowbite-svelte-icons";

  export let databaseConnection: DatabaseConnection;

  let selectedValue: string = Object.keys(datasets)[0];
  let datasetInfo: DatasetInfo;
  let tableOption: TableOption = "all";

  let datasetSize: number;

  async function setDataset() {
    console.log("setting dataset...");
    const info = datasets[selectedValue];
    await databaseConnection.initAndLoad(info.name, info.filename);
    datasetInfo = info;
    // create new brush to clear selections from old dataset
    $filters = {
      brush: vg.Selection.crossfilter(),
    };

    let q = vg.Query.from(info.name).select({ count: vg.count() });
    let r = await vg.coordinator().query(q, { type: "json" });
    datasetSize = r[0]?.["count"];
  }

  function updateData() {
    dataPromise = setDataset();
  }

  function resetBrush() {
    $filters = {
      brush: vg.Selection.crossfilter(),
    };
  }

  let dataPromise: Promise<any> = setDataset();
</script>

<div class="bg-gradient-to-r from-blue-100 to-blue-700 p-5 flex gap-2 flex-row">
  <span
    class="self-center whitespace-nowrap text-2xl font-semibold text-blue-900"
    >Text Clean</span
  >
  <div class="grow" />

  <div class="self-center text-l text-white">
    Total size: {datasetSize}
  </div>

  <!-- <Button id="settingsToggle" on:click={resetBrush} color="light">
  </Button> -->
  <div>
    <Button color="light" outline id="settingsToggle">
      <AdjustmentsHorizontalOutline size="sm" />
    </Button>
    <Popover
      triggeredBy="#settingsToggle"
      class="w-64 text-sm font-light text-gray-500 bg-white z-10"
      title="Settings"
    >
      <div class="p-3 flex flex-col gap-2">
        <Button size="sm" on:click={resetBrush} color="light"
          >Reset filters</Button
        >

        <Select
          size="sm"
          items={[
            { value: "all", name: "All cols" },
            { value: "text", name: "Only text" },
          ]}
          placeholder="Select columns"
          bind:value={tableOption}
        />
      </div>
    </Popover>
  </div>

  <div>
    <Button color="light" outline id="demoToggle">
      <InfoCircleOutline size="sm" />
    </Button>
    <Popover
      triggeredBy="#demoToggle"
      class="w-64 text-sm font-light text-gray-500 bg-white z-10"
      title="Demo"
    >
      <div class="p-3 flex flex-col gap-2">
        <Select
          size="sm"
          items={Object.keys(datasets).map((k) => ({
            value: datasets[k].name,
            name: datasets[k].name,
          }))}
          placeholder="Select dataset"
          bind:value={selectedValue}
          on:change={updateData}
        />
      </div>
    </Popover>
  </div>

  <!-- <div class="self-center">
    <span class="text-white text-l pr-2">Table: </span>
    <select
      class="text-gray-900 bg-gray-50 border border-gray-300 rounded focus:ring-primary-500 focus:border-primary-500"
      bind:value={tableOption}
    >
      <option value="all">All cols</option>
      <option value="text">Only text</option>
    </select>
  </div>
  <div class="self-center">
    <span class="text-white text-l pr-2">Data: </span>
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
  </div> -->
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
