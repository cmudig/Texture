<script lang="ts">
  import type { JoinInfo } from "../../backendapi";
  import * as vg from "@uwdata/vgplot";
  import { TableClient } from "./TableClient";
  import { filters } from "../../stores";
  import {
    formatLocaleAuto,
    formatNumber,
    formatDate,
  } from "../../shared/format";
  import { onDestroy } from "svelte";

  export let mainDatasetName: string;
  export let joinDatasetInfo: JoinInfo | undefined = undefined;
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

    let plotcols = Object.keys(_currentColToggleStates).filter(
      (col) => _currentColToggleStates[col],
    );

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
      joinDatasetInfo,
      mainDatasetName,
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

  // Utils
  function formatColumnName(
    columnName: string,
    sortDesc: boolean,
    sortName?: string,
  ) {
    if (sortName === columnName) {
      return `${columnName} ${sortDesc ? "▾" : "▴"}`;
    }
    return columnName;
  }

  function formatValue(value: any, type: string) {
    if (type === "number") return formatNumber(value);
    if (type === "date") return formatDate(value);
    return formatLocaleAuto(value);
  }
</script>

{#if ready}
  {#if $schema}
    <div
      class="max-h-screen overflow-auto"
      on:scroll={(e) => myTableClient.scroll(e)}
    >
      <table class="w-full table-fixed">
        <thead>
          <tr>
            {#each $schema as schemaItem}
              <th
                class={`sticky top-0 font-medium bg-gray-50 hover:bg-gray-100 cursor-ns-resize border-b-2
                border-gray-300 whitespace-normal text-ellipsis overflow-hidden text-left align-bottom p-2 h-9`}
                on:click={(e) => myTableClient.sort(e, schemaItem.column)}
              >
                {formatColumnName(schemaItem.column, $sortDesc, $sortColumn)}
              </th>
            {/each}
          </tr>
        </thead>
        {#if $data}
          <tbody>
            {#each $data as row, i}
              <tr class="hover:bg-blue-50">
                {#each $schema as schemaItem}
                  {@const myValue = row[schemaItem.column]}
                  <td
                    class={`whitespace-normal text-ellipsis overflow-hidden p-2 align-top text-sm border-b border-gray-100 ${
                      myValue == undefined
                        ? "text-gray-300 italic"
                        : "text-gray-800"
                    }`}
                  >
                    {formatValue(myValue, schemaItem.type)}
                  </td>
                {/each}
              </tr>
            {/each}
          </tbody>
        {:else}
          <p class="mt-4 ml-2">Loading data...</p>
        {/if}
      </table>
    </div>
  {:else}
    <p class="mt-4 ml-2">Loading table info...</p>
  {/if}
{:else}
  <p class="mt-4 ml-2">Not ready yet...</p>
{/if}
