<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { TableClient } from "./TableClient";
  import {
    mosaicSelection,
    datasetSchema,
    tableSortColStore,
    tableSortDescStore,
    tableSchemaStore,
  } from "../../stores";
  import type { DatasetSchema, Column } from "../../backendapi";
  import { onDestroy } from "svelte";
  import RowView from "./RowView.svelte";
  import TablePlaceholder from "../utils/TablePlaceholder.svelte";

  let myTableClient: TableClient;
  let previousClient: TableClient;
  let ready = false;

  function createClient(schema: DatasetSchema, filter) {
    const mainTableCols: Column[] = [];
    const otherTableCols: Column[] = [];

    for (let col of schema.columns) {
      if (col.derivedSchema == undefined) {
        mainTableCols.push(col);
      } else {
        otherTableCols.push(col);
      }
    }

    let client = new TableClient({
      filterBy: filter,
      from: schema.name,
      idColumn: schema.primary_key,
      mainColumns: mainTableCols,
      otherColumns: otherTableCols,
    });

    return client;
  }

  onDestroy(() => {
    vg.coordinator().disconnect(myTableClient);
  });

  $: {
    myTableClient = createClient($datasetSchema, $mosaicSelection);

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

  $: ({ schema, data, loaded, arrayColData } = myTableClient);
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
              {@const id = row[$datasetSchema.primary_key.name]}
              {@const thisRowData = new Map(
                Array.from($arrayColData, ([key, value]) => [
                  key,
                  value.filter(
                    (item) => item[$datasetSchema.primary_key.name] == id,
                  ),
                ]),
              )}
              <RowView
                idSchema={$datasetSchema.primary_key}
                colSchema={$datasetSchema.columns}
                mainTableData={row}
                arrayTableMap={thisRowData}
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
