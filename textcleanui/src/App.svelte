<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { datasets } from "./shared/colConfig";
  import type { DatabaseConnection } from "./database/db";
  import type { DatasetInfo } from "./shared/types";
  import { filters } from "./stores";

  import Sidebar from "./components/Sidebar.svelte";
  import InstanceView from "./components/InstanceView.svelte";
  import { Button, Select, Popover, Toggle, Label } from "flowbite-svelte";
  import {
    AdjustmentsHorizontalOutline,
    InfoCircleOutline,
  } from "flowbite-svelte-icons";

  export let databaseConnection: DatabaseConnection;

  let selectedValue: string = Object.keys(datasets)[0];
  let datasetInfo: DatasetInfo;
  let currentColumns: string[] = [];
  let currentColToggleStates: Record<string, boolean> = {};

  let datasetSize: number;

  async function setDataset() {
    const info = datasets[selectedValue];
    await databaseConnection.initAndLoad(info.name, info.filename);
    datasetInfo = info;
    currentColumns = [
      ...info.metadata.text_columns.map((c) => c.name),
      ...info.metadata.other_columns.map((c) => c.name),
    ];

    currentColToggleStates = currentColumns.reduce(
      (acc: Record<string, boolean>, col) => {
        acc[col] = true;
        return acc;
      },
      {}
    );

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

        <div>
          <Label>Display in table</Label>
          <div class="ml-2 flex flex-col gap-1">
            {#each currentColumns as col}
              <Toggle bind:checked={currentColToggleStates[col]}>
                <span class="text-ellipsis overflow-hidden">
                  {col}
                </span>
              </Toggle>
            {/each}
          </div>
        </div>
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
</div>

{#await dataPromise}
  <div class="p-4">Loading data...</div>
{:then}
  <div class="flex flex-row">
    <div class="w-1/3 h-screen overflow-scroll">
      <Sidebar {datasetInfo} />
    </div>
    <div class="w-2/3 h-screen overflow-scroll">
      <InstanceView {datasetInfo} {currentColToggleStates} />
    </div>
  </div>
{:catch error}
  <div>Error: {error.message}</div>
{/await}
