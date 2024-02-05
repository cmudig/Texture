<script lang="ts">
  import type { JoinInfo, DatasetInfo } from "../../backendapi";
  import * as vg from "@uwdata/vgplot";
  import { TableClient, type FieldInfo } from "./TableClient";
  import { filters, selectionDisplay, compareSimilarID } from "../../stores";
  import { formatValue } from "../../shared/format";
  import { onDestroy } from "svelte";
  import { type SelectionMap, isStringArray } from "../../shared/types";
  import Highlight from "./Highlight.svelte";
  import Regular from "./Regular.svelte";
  import { FilterOutline } from "flowbite-svelte-icons";

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

  function renderValue(
    myValue: any,
    schemaItem: FieldInfo,
    selections: SelectionMap,
    joinInfo?: JoinInfo,
  ) {
    let highlights: string[] = [];

    if (
      joinInfo?.joinColumn.associated_text_col_name == schemaItem.column &&
      joinInfo?.joinColumn.name in selections &&
      isStringArray(selections[joinInfo.joinColumn.name])
    ) {
      highlights = [...highlights, ...selections[joinInfo.joinColumn.name]];
    }
    if (
      schemaItem.column in selections &&
      isStringArray(selections[schemaItem.column])
    ) {
      highlights = [...highlights, ...selections[schemaItem.column]];
    }

    if (highlights.length) {
      return {
        component: Highlight,
        props: {
          value: myValue,
          highlights,
        },
      };
    }

    return {
      component: Regular,
      props: { value: formatValue(myValue, { type: schemaItem.type }) },
    };
  }

  function displaySimilar(id: number) {
    $compareSimilarID = id;
  }

  function handleSort(event, colName: string) {
    if (colName === $sortColumn) {
      if (event.metaKey) {
        $sortColumn = undefined;
      } else {
        $sortDesc = !$sortDesc;
      }
    } else {
      $sortColumn = colName;
      $sortDesc = false;
    }
  }
</script>

{#if ready}
  {#if $schema}
    <div
      class="max-h-screen overflow-auto"
      on:scroll={(e) => myTableClient.scroll(e)}
    >
      <table class="w-full">
        <thead>
          <tr>
            <th
              class="sticky top-0 font-medium bg-gray-50 border-b-2 border-gray-300 whitespace-normal text-ellipsis overflow-hidden text-left align-bottom p-2 h-9"
            ></th>
            {#each $schema as schemaItem}
              <!-- plot if not pk or if the pk and is toggled on -->
              {#if schemaItem.column !== datasetInfo.primary_key.name || currentColToggleStates[datasetInfo.primary_key.name]}
                <th
                  class="sticky top-0 font-medium bg-gray-50 hover:bg-gray-100 cursor-ns-resize border-b-2 border-gray-300 whitespace-normal text-ellipsis overflow-hidden text-left align-bottom p-2 h-9"
                  on:click={(e) => handleSort(e, schemaItem.column)}
                >
                  {formatColumnName(schemaItem.column, $sortDesc, $sortColumn)}
                </th>
              {/if}
            {/each}
          </tr>
        </thead>
        {#if $data}
          <tbody>
            {#each $data as row}
              <tr class="hover:bg-blue-50">
                <td class="pt-2 pl-2 align-top border-b border-gray-100">
                  <div
                    class="text-gray-500 rounded-full py-1 hover:text-primary-700 hover:bg-primary-100"
                    title="Show similar"
                  >
                    <FilterOutline
                      title="filter me"
                      size="sm"
                      on:click={() =>
                        displaySimilar(
                          Number(row[datasetInfo.primary_key.name]),
                        )}
                    />
                  </div>
                </td>
                {#each $schema as schemaItem}
                  {@const myValue = row[schemaItem.column]}
                  {@const item = renderValue(
                    myValue,
                    schemaItem,
                    $selectionDisplay,
                    $filters.joinDatasetInfo,
                  )}
                  {#if schemaItem.column !== datasetInfo.primary_key.name || currentColToggleStates[datasetInfo.primary_key.name]}
                    <td
                      class={`whitespace-normal text-ellipsis overflow-hidden p-2 align-top text-sm border-b border-gray-100 ${
                        myValue == undefined
                          ? "text-gray-300 italic"
                          : "text-gray-800"
                      }`}
                    >
                      <svelte:component this={item.component} {...item.props} />
                    </td>
                  {/if}
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
