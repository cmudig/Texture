<script lang="ts">
  import { databaseConnection, datasetSchema, setSchema } from "../stores";

  import { SearchOutline } from "flowbite-svelte-icons";
  import Toggle from "./Toggle.svelte";
  import Histogram from "./charts/Histogram.svelte";

  let currentQuery: string = "";

  function runSearch() {
    if (currentQuery) {
      console.log("Starting similarity search", currentQuery);
      const prom = databaseConnection.api.runEmbedSearch(
        $datasetSchema.name,
        undefined,
        currentQuery,
      );

      prom.then((res) => {
        console.log("Finished similarity search", res);
        setSchema();
      });
    } else {
      console.error("no search query");
    }
  }
</script>

<Toggle>
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
        <SearchOutline
          class="text-primary-800  pointer-events-none"
          size="sm"
        />
      </button>
    </div>

    <!-- {#if $datasetSchema.search_result}
      <div class="italic">
        {#if $datasetSchema.search_result.extra?.["search_id"] != undefined}
          Similarity to id: {$datasetSchema.search_result.extra?.["search_id"]}
        {/if}
        {#if $datasetSchema.search_result.extra?.["search_query"] != undefined}
          Similarity to query: {$datasetSchema.search_result.extra?.[
            "search_query"
          ]}
        {/if}
      </div>
      <Histogram
        mainDatasetName={$datasetSchema.search_result.derivedSchema
          ?.table_name ?? $datasetSchema.name}
        columnName={$datasetSchema.search_result.name}
        showBackground={false}
      />
    {:else}
      no search
    {/if} -->
  </div>
</Toggle>
