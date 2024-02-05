<script lang="ts">
  import type { DatasetInfo } from "../../backendapi";
  import * as vg from "@uwdata/vgplot";
  import { TableClient } from "./TableClient";
  import { filters, compareSimilarID } from "../../stores";
  import { onDestroy } from "svelte";
  import { FilterOutline } from "flowbite-svelte-icons";
  import RowView from "./RowView.svelte";

  export let datasetInfo: DatasetInfo;
  export let currentColToggleStates: Record<string, boolean> = {};

  let myTableClient: TableClient;
  let previousClient: TableClient;
  let ready = false;

  function createClient(
    _joinDatasetInfo,
    _mainDatasetName,
    _currentColToggleStates,
    filter,
  ) {
    let fromClause = _joinDatasetInfo
      ? vg.fromJoinDistinct({
          table: _mainDatasetName,
          rightTable: _joinDatasetInfo.joinDatasetName,
          joinKey: _joinDatasetInfo.joinKey,
        })
      : _mainDatasetName;

    // only get columns with toggle on; remove duplicate pk
    let plotcols = Object.keys(_currentColToggleStates).filter(
      (col) =>
        _currentColToggleStates[col] && col !== datasetInfo.primary_key.name,
    );

    // always include pk
    plotcols.push(datasetInfo.primary_key.name);

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

  $: {
    myTableClient = createClient(
      datasetInfo.joinDatasetInfo,
      datasetInfo.name,
      currentColToggleStates,
      $filters.brush,
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

  $: ({ schema, data, sortColumn, sortDesc } = myTableClient);

  function displaySimilar(id: number) {
    $compareSimilarID = id;
  }

  $: colTypeMap = datasetInfo.column_info.reduce((acc, col) => {
    acc[col.name] = col.type;
    return acc;
  }, {});
</script>

{#if ready}
  {#if $schema}
    <div
      class="max-h-screen overflow-auto"
      on:scroll={(e) => myTableClient.scroll(e)}
    >
      {#if $data}
        <div class="bg-gray-100 p-4 flex flex-col gap-2">
          {#each $data as row}
            {@const rowArr = Object.entries(row)}
            <RowView
              id={Number(row[datasetInfo.primary_key.name])}
              textData={rowArr.filter(([k, v]) => colTypeMap[k] === "text")}
              metadata={rowArr.filter(
                ([k, v]) =>
                  colTypeMap[k] !== "text" &&
                  k !== datasetInfo.primary_key.name,
              )}
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
                    displaySimilar(Number(row[datasetInfo.primary_key.name]))}
                />
              </div>
            </RowView>
          {/each}
        </div>
      {:else}
        <p class="mt-4 ml-2">Loading data...</p>
      {/if}
    </div>
  {:else}
    <p class="mt-4 ml-2">Loading table info...</p>
  {/if}
{:else}
  <p class="mt-4 ml-2">Not ready yet...</p>
{/if}
