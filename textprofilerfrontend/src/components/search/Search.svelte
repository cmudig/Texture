<script lang="ts">
  import { Input } from "flowbite-svelte";
  import { SearchOutline } from "flowbite-svelte-icons";
  import { filters } from "../../stores";
  import { writable, type Writable } from "svelte/store";
  import { isSelection } from "@uwdata/mosaic-core";
  import {
    regexp_matches,
    contains,
    prefix,
    suffix,
    literal,
    or,
  } from "@uwdata/mosaic-sql";

  const FUNCTIONS = { contains, prefix, suffix, regexp: regexp_matches };

  export let columnNames: string[] | undefined;
  export let type = "contains";
  let currentQuery: Writable<string> = writable();

  function publishUpdate() {
    if (isSelection($filters.brush) && columnNames?.length) {
      // adds predicates to provided selection; if a cross filter then these will be OR'd

      let pred = null;

      if ($currentQuery) {
        pred =
          columnNames.length > 1
            ? or(
                columnNames.map((col) =>
                  FUNCTIONS[type](col, literal($currentQuery)),
                ),
              )
            : FUNCTIONS[type](columnNames[0], literal($currentQuery));
      }

      let updateInfo = {
        source: undefined,
        schema: { type },
        value: $currentQuery,
        predicate: pred,
      };

      $filters.brush.update(updateInfo);
    }
  }
</script>

<div class="relative w-full max-w-80">
  <div
    class="flex absolute inset-y-0 start-0 items-center ps-3 pointer-events-none"
  >
    <SearchOutline class="w-4 h-4" />
  </div>
  <Input
    class="ps-10"
    placeholder="Search over text columns..."
    bind:value={$currentQuery}
    on:change={() => publishUpdate()}
  />
</div>
