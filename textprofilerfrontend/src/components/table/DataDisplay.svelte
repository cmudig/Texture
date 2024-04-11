<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { TableClient } from "./TableClient";
  import { mosaicSelection, compareSimilarID, datasetInfo } from "../../stores";
  import { onDestroy } from "svelte";
  import {
    FilterOutline,
    ArrowUpSolid,
    ArrowDownSolid,
  } from "flowbite-svelte-icons";
  import RowView from "./RowView.svelte";
  import { Select } from "flowbite-svelte";
  import TablePlaceholder from "../utils/TablePlaceholder.svelte";

  export let currentColToggleStates: Record<string, boolean> = {};

  let myTableClient: TableClient;
  let previousClient: TableClient;
  let ready = false;

  function createClient(_mainDatasetName, _currentColToggleStates, filter) {
    let fromClause = _mainDatasetName;

    // only get columns with toggle on; remove duplicate pk
    let plotcols = Object.keys(_currentColToggleStates).filter(
      (col) =>
        _currentColToggleStates[col] && col !== $datasetInfo.primary_key.name,
    );

    // always include pk
    plotcols.push($datasetInfo.primary_key.name);

    let client = new TableClient({
      filterBy: filter,
      from: fromClause,
      columns: plotcols,
    });

    return client;
  }

  onDestroy(() => {
    vg.coordinator().disconnect(myTableClient);
  });

  function displaySimilar(id: number) {
    $compareSimilarID = id;
  }

  $: {
    myTableClient = createClient(
      $datasetInfo.name,
      currentColToggleStates,
      $mosaicSelection,
    );

    if (previousClient) {
      vg.coordinator().disconnect(previousClient);
    }
    previousClient = myTableClient;

    vg.coordinator()
      .connect(myTableClient)
      .then(() => {
        ready = true;
      });
  }

  // BUG #71: I think these stores are not triggering reload when new TableClient created
  $: ({ schema, data, sortColumn, sortDesc } = myTableClient);

  $: colTypeMap = $datasetInfo.columns.reduce((acc, col) => {
    acc[col.name] = col.type;
    return acc;
  }, {});
</script>

<div class="h-full">
  {#if ready}
    {#if $schema}
      <div class="flex gap-2 justify-end items-center text-gray-500 px-4 pb-1">
        <slot name="navBar" />

        <div class="flex gap-1 items-center">
          <Select
            class="max-w-40"
            size="sm"
            items={[
              { value: undefined, name: "Not sorted" },
              ...Object.keys(colTypeMap).map((k) => ({ value: k, name: k })),
            ]}
            bind:value={$sortColumn}
            placeholder="Sort by..."
          />

          <button
            class={`hover:bg-gray-200 bg-gray-50 text-gray-500 p-1 rounded ${
              !$sortColumn && "cursor-not-allowed !text-gray-300"
            }`}
            on:click={() => ($sortDesc = !$sortDesc)}
            title={"Toggle sort order"}
            disabled={!$sortColumn}
          >
            {#if $sortDesc}
              <ArrowDownSolid size="xs" />
            {:else}
              <ArrowUpSolid size="xs" />
            {/if}
          </button>
        </div>
      </div>
      <div
        class="max-h-screen overflow-auto"
        on:scroll={(e) => myTableClient.scroll(e)}
      >
        {#if $data}
          <div class="p-4 flex flex-col gap-2">
            {#each $data as row}
              {@const rowArr = Object.entries(row)}
              <RowView
                id={Number(row[$datasetInfo.primary_key.name])}
                textData={rowArr.filter(([k, v]) => colTypeMap[k] === "text")}
                metadata={rowArr.filter(
                  ([k, v]) =>
                    colTypeMap[k] !== "text" &&
                    k !== $datasetInfo.primary_key.name,
                )}
                selection={myTableClient.filterBy}
              >
                <div
                  slot="optionButtons"
                  class="hover:bg-gray-100 text-gray-500 p-1 rounded"
                  title="Show similar"
                >
                  <FilterOutline
                    title="filter me"
                    size="sm"
                    on:click={() =>
                      displaySimilar(
                        Number(row[$datasetInfo.primary_key.name]),
                      )}
                  />
                </div>
              </RowView>
            {/each}
          </div>
        {:else}
          <div class="p-4">
            <p class="mb-4">Loading data...</p>

            <TablePlaceholder />
          </div>
        {/if}
      </div>
    {:else}
      <div class="p-4">
        <p class="mb-4">Loading table info...</p>
      </div>
    {/if}
  {:else}
    <div class="p-4">
      <p class="mb-4">Connecting to database...</p>
    </div>
  {/if}
</div>
