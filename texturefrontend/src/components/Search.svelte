<script lang="ts">
  import { onDestroy } from "svelte";
  import { SearchOutline } from "flowbite-svelte-icons";
  import { mosaicSelection, clearColumnSelections } from "../stores";
  import { isSelection } from "@uwdata/mosaic-core";
  import {
    regexp_matches,
    contains,
    prefix,
    suffix,
    literal,
    eq,
  } from "@uwdata/mosaic-sql";
  import { getUUID } from "../shared/utils";
  import type { Column } from "../backendapi/models/Column";

  const FUNCTIONS = { contains, prefix, suffix, regexp: regexp_matches };

  export let column: Column;
  export let tableName: string;
  export let type = "contains";
  let currentQuery: string | undefined;
  let uuid = getUUID();

  $: saveSelectionToCache(column, uuid);

  function saveSelectionToCache(_col: Column, _uuid) {
    $clearColumnSelections = [
      ...$clearColumnSelections,
      {
        clearFunc: () => (currentQuery = undefined),
        sourceId: _uuid,
        colName: _col.name,
      },
    ];
  }

  function publishUpdate() {
    if (isSelection($mosaicSelection) && column != undefined) {
      let pred = null;
      let cleanedQuery = currentQuery?.replaceAll("'", "''");

      // TODO: support case-insensitive search

      if (cleanedQuery) {
        if (column.type === "text" || column.type === "categorical") {
          pred = FUNCTIONS[type](column.name, literal(cleanedQuery));
        } else if (column.type === "number") {
          pred = eq(column.name, literal(Number(cleanedQuery)));
        } else if (column.type === "date") {
          pred = eq(column.name, literal(cleanedQuery));
        }
      }

      let updateInfo = {
        source: `${column.name}_search_${uuid}`,
        schema: { type },
        value: cleanedQuery,
        predicate: pred,
        clients: new Set().add({ source: { table: tableName } }),
      };

      $mosaicSelection.update(updateInfo);
    }
  }

  onDestroy(() => {
    $clearColumnSelections = $clearColumnSelections.filter(
      (s) => s.sourceId !== uuid,
    );
  });
</script>

<div class="inline flex gap-1 items-center">
  <SearchOutline class="w-3 h-3" />

  <input
    class="w-full disabled:cursor-not-allowed disabled:opacity-50 focus:border-primary-500 focus:ring-primary-500 dark:focus:border-primary-500 dark:focus:ring-primary-500 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:border-gray-600 text-sm rounded-md bg-gray-50 text-gray-900 border-gray-300 px-2 py-0"
    placeholder=""
    type="text"
    bind:value={currentQuery}
    on:input={() => publishUpdate()}
  />
</div>
