<script lang="ts">
  import { databaseConnection, datasetSchema, setSchema } from "../stores";
  import { SearchOutline } from "flowbite-svelte-icons";
  import Toggle from "./layout/Toggle.svelte";
  import { QueryStatus } from "../shared/types";
  import { Spinner } from "flowbite-svelte";

  let currentQuery: string = "";
  let searchStatus: QueryStatus = QueryStatus.NOT_STARTED;

  function runSearch() {
    if (currentQuery) {
      console.log("Starting similarity search", currentQuery);
      searchStatus = QueryStatus.PENDING;
      const prom = databaseConnection.api.runEmbedSearch(
        $datasetSchema.name,
        undefined,
        currentQuery,
      );

      prom.then((res) => {
        console.log("Finished similarity search", res);
        searchStatus = QueryStatus.NOT_STARTED;
        setSchema();
      });
    } else {
      console.error("no search query");
    }
  }
</script>

<Toggle showTopBorder={false}>
  <div slot="title">Similarity Search</div>

  <div slot="body" class="flex flex-col gap-1">
    <div class="flex gap-2 items-start mt-2">
      <textarea
        class="w-full disabled:cursor-not-allowed disabled:opacity-50 focus:border-primary-500 focus:ring-primary-500 dark:focus:border-primary-500 dark:focus:ring-primary-500 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:border-gray-600 text-sm rounded-md bg-gray-50 text-gray-900 border-gray-200 px-2 py-1 grow min-h-8 h-8"
        placeholder="Search..."
        bind:value={currentQuery}
      />

      <button
        class="p-2 rounded-lg bg-gray-100 hover:bg-gray-300 focus:ring-2 focus:ring-primary-500"
        title="Run search"
        on:click={runSearch}
      >
        {#if searchStatus === QueryStatus.PENDING}
          <Spinner size="4" />
        {:else}
          <SearchOutline
            class="text-primary-800  pointer-events-none"
            size="sm"
          />
        {/if}
      </button>
    </div>
  </div>
</Toggle>
