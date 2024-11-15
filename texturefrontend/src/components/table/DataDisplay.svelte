<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { TableClient } from "./TableClient";
  import {
    mosaicSelection,
    compareSimilarID,
    datasetInfo,
    tableSortColStore,
    tableSortDescStore,
    tableSchemaStore,
  } from "../../stores";
  import { onDestroy } from "svelte";
  import RowView from "./RowView.svelte";
  import TablePlaceholder from "../utils/TablePlaceholder.svelte";

  export let currentColToggleStates: Record<string, boolean> = {};

  let myTableClient: TableClient;
  let previousClient: TableClient;
  let ready = false;

  function createClient(_dsInfo, _currentColToggleStates, filter) {
    // only get columns with toggle on; remove duplicate pk
    let plotcols = Object.keys(_currentColToggleStates).filter(
      (col) =>
        _currentColToggleStates[col] &&
        col !== _dsInfo.primary_key.name &&
        _dsInfo.columns.find((c) => c.name === col).table_name == null, // dont include cols from another table bc breaks mosaic client
    );

    // always include pk
    plotcols.push(_dsInfo.primary_key.name);

    let client = new TableClient({
      filterBy: filter,
      from: _dsInfo.name,
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
      $datasetInfo,
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

    tableSortColStore.set(myTableClient.sortColumn);
    tableSortDescStore.set(myTableClient.sortDesc);
    tableSchemaStore.set(myTableClient.schema);
  }

  $: ({ schema, data, loaded } = myTableClient);

  $: colTypeMap = $datasetInfo.columns.reduce((acc, col) => {
    acc[col.name] = col.type;
    return acc;
  }, {});
</script>

<div class="h-full">
  {#if ready}
    {#if $schema}
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
              />
            {/each}

            {#if !$loaded}
              <button
                class="hover:bg-gray-100 text-gray-500 text-sm px-2 py-1 rounded"
                on:click={() => {
                  myTableClient.loadMoreData();
                }}
              >
                Load more rows
              </button>
            {/if}
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
