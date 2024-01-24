<script lang="ts">
  import type { JoinInfo } from "../../backendapi";
  import * as vg from "@uwdata/vgplot";
  import { TableClient } from "./TableClient";
  import { filters } from "../../stores";
  import { formatLocaleAuto, formatNumber, formatDate } from "./format";
  import { onMount } from "svelte";

  export let mainDatasetName: string;
  export let joinDatasetInfo: JoinInfo | undefined = undefined;
  export let currentColToggleStates: Record<string, boolean> = {};

  //   TODO none of this is reactive right now so might not change when props change
  let fromClause = joinDatasetInfo
    ? vg.fromJoinDistinct({
        table: mainDatasetName,
        rightTable: joinDatasetInfo.joinDatasetName,
        joinKey: joinDatasetInfo.joinKey,
      })
    : mainDatasetName;

  let plotcols = Object.keys(currentColToggleStates).filter(
    (col) => currentColToggleStates[col],
  );

  let myTableClient = new TableClient({
    filterBy: $filters.brush,
    from: fromClause,
    columns: plotcols,
  });

  let { schema, data, sortColumn, sortDesc } = myTableClient;

  let ready = false;

  onMount(() => {
    vg.coordinator()
      .connect(myTableClient)
      .then(() => {
        ready = true;
      });
  });

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
      <table>
        <thead>
          <tr>
            {#each $schema as schemaItem}
              <th on:click={(e) => myTableClient.sort(e, schemaItem.column)}>
                {formatColumnName(schemaItem.column, $sortDesc, $sortColumn)}
              </th>
            {/each}
          </tr>
        </thead>
        {#if $data}
          <tbody>
            {#each $data as row, i}
              <tr>
                {#each $schema as schemaItem}
                  {@const myValue = row[schemaItem.column]}
                  <td
                    class:text-gray-300={myValue == undefined}
                    class:italic={myValue == undefined}
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

<style>
  table {
    display: table;
    position: relative;
    table-layout: fixed;
    border-collapse: separate;
    border-spacing: 0;
    font-variant-numeric: tabular-nums;
    box-sizing: border-box;
    max-width: initial;
    min-height: 33px;
    margin: 0;
    width: 100%;
    line-height: 15.6px;
  }

  thead tr th {
    position: sticky;
    top: 0;
    font-weight: 500; /* font-medium */
    background: rgb(249 250 251); /* bg-gray-50 */
    cursor: ns-resize;
    border-bottom: solid 1px #ccc;
    height: 2.25rem;
  }

  thead tr th:hover {
    background-color: rgb(243 244 246); /* hover:bg-gray-100 */
  }

  tbody tr:hover {
    background: #eff6ff;
  }

  th {
    color: #111;
    text-align: left;
    vertical-align: bottom;
  }

  td,
  th {
    white-space: wrap;
    text-overflow: ellipsis;
    overflow: hidden;
    padding: 0.5rem;
  }

  td,
  tr:not(:last-child) th {
    border-bottom: solid 1px #eee;
  }

  td {
    font-size: 14px;
    /* color: #444; */
    vertical-align: top;
  }
</style>
