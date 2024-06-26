<script lang="ts">
  import { onDestroy } from "svelte";
  import { Input } from "flowbite-svelte";
  import { SearchOutline } from "flowbite-svelte-icons";
  import { mosaicSelection, clearColumnSelections } from "../stores";
  import { isSelection } from "@uwdata/mosaic-core";
  import {
    regexp_matches,
    contains,
    prefix,
    suffix,
    literal,
    or,
  } from "@uwdata/mosaic-sql";
  import { getUUID } from "../shared/utils";

  const FUNCTIONS = { contains, prefix, suffix, regexp: regexp_matches };

  export let columnNames: string[] | undefined;
  export let tableName: string;
  export let type = "contains";
  let currentQuery: string | undefined;
  let uuid = getUUID();

  $: saveSelectionToCache(columnNames);

  function saveSelectionToCache(_colNames: string[] | undefined) {
    if (_colNames?.length) {
      _colNames.forEach((colName) => {
        $clearColumnSelections = [
          ...$clearColumnSelections,
          {
            clearFunc: () => (currentQuery = undefined),
            sourceId: uuid,
            colName: colName,
          },
        ];
      });
    }
  }

  function publishUpdate() {
    if (isSelection($mosaicSelection) && columnNames?.length) {
      // adds predicates to provided selection; if a cross filter then these will be OR'd

      let pred = null;
      let cleanedQuery = currentQuery?.replaceAll("'", "''");

      if (cleanedQuery) {
        pred =
          columnNames.length > 1
            ? or(
                columnNames.map((col) =>
                  FUNCTIONS[type](col, literal(cleanedQuery)),
                ),
              )
            : FUNCTIONS[type](columnNames[0], literal(cleanedQuery));
      }

      let updateInfo = {
        source: undefined,
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

<div class="relative w-full max-w-96">
  <div
    class="flex absolute inset-y-0 start-0 items-center ps-3 pointer-events-none"
  >
    <SearchOutline class="w-4 h-4" />
  </div>
  <Input
    class="ps-10"
    placeholder="Search over text columns..."
    bind:value={currentQuery}
    on:input={() => publishUpdate()}
  />
</div>
