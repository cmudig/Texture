<script lang="ts">
  import { Input } from "flowbite-svelte";
  import { SearchOutline } from "flowbite-svelte-icons";
  import * as vg from "@uwdata/vgplot";
  import { filters } from "../../stores";
  import { SearchClient } from "./SearchClient";
  import { onDestroy } from "svelte";
  import { writable, type Writable } from "svelte/store";

  export let columnNames: string[] | undefined; // columns to search over
  export let mainDatasetName: string | undefined;
  //   export let as: any; // selection

  let mySearchClient: SearchClient;
  let previousClient: SearchClient;
  let ready = false;
  //   let inputValue: Writable<string>; //= writable();
  let currentQuery: Writable<string>;

  onDestroy(() => {
    vg.coordinator().disconnect(mySearchClient);
  });

  $: if (columnNames && mainDatasetName) {
    mySearchClient = new SearchClient({
      selection: $filters.brush,
      columns: columnNames,
      from: mainDatasetName,
      filterBy: $filters.brush,
      //   inputValue,
    });

    if (previousClient) {
      vg.coordinator().disconnect(previousClient);
    }
    previousClient = mySearchClient;

    vg.coordinator()
      .connect(mySearchClient)
      .then(() => {
        ready = true;
      });
  }

  $: if (mySearchClient) {
    ({ currentQuery } = mySearchClient);
  }
</script>

{#if ready}
  debug: {$currentQuery}
  <div class="relative w-full max-w-80">
    <div
      class="flex absolute inset-y-0 start-0 items-center ps-3 pointer-events-none"
    >
      <SearchOutline class="w-4 h-4" />
    </div>
    <Input class="ps-10" placeholder="Search..." bind:value={$currentQuery} />
  </div>
{:else}
  Not ready
{/if}
