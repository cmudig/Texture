<script lang="ts">
  //   import { datasetSchema } from "../stores";

  import { SearchOutline } from "flowbite-svelte-icons";
  import Toggle from "./Toggle.svelte";

  let currentQuery: string = "";
</script>

<Toggle>
  <div slot="title">Similarity Search</div>

  <div slot="body">
    <div class="flex gap-2 items-start mt-2">
      <textarea
        class="w-full disabled:cursor-not-allowed disabled:opacity-50 focus:border-primary-500 focus:ring-primary-500 dark:focus:border-primary-500 dark:focus:ring-primary-500 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:border-gray-600 text-sm rounded-md bg-gray-50 text-gray-900 border-gray-200 px-2 py-1 grow min-h-8 h-8"
        placeholder="Search..."
        bind:value={currentQuery}
      />

      <button
        class="p-2 rounded-lg bg-gray-100 hover:bg-gray-300 focus:ring-2 focus:ring-primary-500"
        title="Run search"
        on:click={() => {
          console.log("abotta search");
        }}
      >
        <SearchOutline
          class="text-primary-800  pointer-events-none"
          size="sm"
        />
      </button>
    </div>
    <div>TODO show chart here if search result...</div>
  </div>
</Toggle>
