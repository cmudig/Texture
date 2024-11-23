<script lang="ts">
  import { Label } from "flowbite-svelte";

  import {
    showBackgroundDistMap,
    showSegmentValues,
    datasetSchema,
  } from "../../stores";
  import SaveTableToFile from "../SaveTableToFile.svelte";

  export let allowDeriveNew: boolean;

  function setBackgroundDist(val: boolean) {
    $showBackgroundDistMap = Object.keys($showBackgroundDistMap).reduce(
      (acc, key) => {
        acc[key] = val;
        return acc;
      },
      {},
    );
  }
</script>

<div class="flex flex-col gap-4 p-2">
  <div class="flex flex-col gap-2">
    <div class="flex gap-2 items-center">
      <h3 class="text-base">Dataset: {$datasetSchema.name}</h3>
      <SaveTableToFile />
    </div>
  </div>

  <hr />

  <div class="flex flex-col gap-2">
    <h3 class="text-base">Display Settings</h3>

    <div class="flex gap-2 items-center">
      <input
        type="checkbox"
        class="w-4 h-4 bg-gray-100 border-gray-300 dark:ring-offset-gray-800 focus:ring-2 me-2 dark:bg-gray-700 dark:border-gray-600 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600"
        bind:checked={$showSegmentValues}
      />

      <Label>Show segment values in table</Label>
    </div>

    <div class="flex gap-2 items-center">
      <button
        class="hover:bg-gray-100 bg-gray-50 rounded border px-2 border-gray-200 focus:ring-2 focus:ring-primary-500"
        on:click={() => setBackgroundDist(true)}
      >
        On
      </button>
      <button
        class="hover:bg-gray-100 bg-gray-50 rounded border px-2 border-gray-200 focus:ring-2 focus:ring-primary-500"
        on:click={() => setBackgroundDist(false)}
      >
        Off
      </button>
      <Label>Background distributions</Label>
    </div>
  </div>

  <hr />

  <div class="flex flex-col gap-2">
    <h3 class="text-base">Feature Flags</h3>

    <div class="flex gap-2 items-center">
      <input
        type="checkbox"
        class="w-4 h-4 bg-gray-100 border-gray-300 dark:ring-offset-gray-800 focus:ring-2 me-2 dark:bg-gray-700 dark:border-gray-600 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600"
        bind:checked={allowDeriveNew}
      />

      <Label>Allow derive new</Label>
    </div>
  </div>
</div>
