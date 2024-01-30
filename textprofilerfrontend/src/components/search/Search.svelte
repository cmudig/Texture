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

  $: console.log("searching over cols: ", columnNames);

  let mySearchClient: SearchClient;
  let previousClient: SearchClient;
  let ready = false;
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
    });

    if (previousClient) {
      console.log("disconnecting previous client");
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
    currentQuery = mySearchClient.currentQuery;
  }
</script>

{#if ready}
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
