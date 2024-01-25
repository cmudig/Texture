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
