<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { datasets } from "./shared/colConfig";
  import type { DatabaseConnection } from "./database/db";
  import { getCount, getColSummaries } from "./database/queries";
  import type { DatasetInfo, ColumnSummary } from "./shared/types";
  import {
    filters,
    selectionDisplay,
    showBackgroundDist,
    filteredCount,
  } from "./stores";
  import Sidebar from "./components/Sidebar.svelte";
  import InstanceView from "./components/InstanceView.svelte";
  import FilterDisplay from "./components/FilterDisplay.svelte";
  import QualityView from "./components/QualityView.svelte";
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
  } from "flowbite-svelte";
  import {
    AdjustmentsHorizontalOutline,
    FilterSolid,
    ChartMixedSolid,
    TableSolid,
    ShieldCheckSolid,
  } from "flowbite-svelte-icons";
  import { sineIn } from "svelte/easing";
  import { formatNumber } from "./shared/utils";

  export let databaseConnection: DatabaseConnection;

  let selectedValue: string = Object.keys(datasets)[0];
  let datasetInfo: DatasetInfo;
  let currentColumns: string[] = [];
  let currentColToggleStates: Record<string, boolean> = {};
  let datasetSize: number;
  let filterPanelHidden = true;
  let datasetColSummaries: ColumnSummary[];

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
      datasetName: info.name,
    };

    datasetSize = await getCount(info.name);
    datasetColSummaries = await getColSummaries(info.name);
  }

  function updateData() {
    dataPromise = setDataset();
  }

  function resetBrush() {
    $filters = {
      brush: vg.Selection.crossfilter(),
      datasetName: datasetInfo.name,
    };
  }

  let dataPromise: Promise<any> = setDataset();

  import { Tabs, TabItem } from "flowbite-svelte";
</script>

<div class="bg-gradient-to-r from-blue-100 to-blue-700 p-5 flex gap-2 flex-row">
  <span
    class="self-center whitespace-nowrap text-2xl font-semibold text-blue-900"
    >Text Profiler</span
  >
  <div class="grow" />

  <div class="self-center text-l text-white">
    {formatNumber($filteredCount)} / {formatNumber(datasetSize)} rows
  </div>

  <AdjustmentsHorizontalOutline
    id="settingsToggle"
    size="md"
    class="text-white hover:text-primary-700 self-center mx-1"
  />
  <Popover
    triggeredBy="#settingsToggle"
    class="w-64 text-sm font-light text-gray-500 bg-white z-10"
    title="Settings"
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
      <div class="mt-2">
        <Label>Background distributions</Label>

        <Toggle class="mt-2" bind:checked={$showBackgroundDist}
          >Show in plot</Toggle
        >
      </div>

      <div class="mt-2">
        <Label>Display in table</Label>
        <div class="mt-2 flex flex-col gap-1">
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

  <FilterSolid
    id="filterToggle"
    on:click={() => (filterPanelHidden = false)}
    class="text-white hover:text-primary-700 self-center mx-1"
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
      id="sidebar"
    >
      <div class="flex items-center">
        <h3
          id="drawer-label"
          class="inline-flex items-center mb-4 text-base font-semibold"
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

  <div class="flex flex-row">
    <div class="w-1/3 h-screen overflow-scroll">
      <Tabs style="underline" contentClass="">
        <TabItem open>
          <div slot="title" class="flex items-center gap-2">
            <ChartMixedSolid size="sm" />
            Explore
          </div>

          <Sidebar {datasetInfo} {datasetColSummaries} />
        </TabItem>
        <TabItem>
          <div slot="title" class="flex items-center gap-2">
            <ShieldCheckSolid size="sm" />
            Quality
          </div>
          <QualityView {datasetInfo} />
        </TabItem>
      </Tabs>
    </div>
    <div class="w-2/3 h-screen overflow-scroll">
      <Tabs style="underline" contentClass="border-l-2 border-slate-50">
        <TabItem open>
          <div slot="title" class="flex items-center gap-2">
            <TableSolid size="sm" />
            Table
          </div>

          <InstanceView {datasetInfo} {currentColToggleStates} />
        </TabItem>
      </Tabs>
    </div>
  </div>
{:catch error}
  <div>Error: {error.message}</div>
{/await}
