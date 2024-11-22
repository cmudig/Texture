<script lang="ts">
  import { Select, Label } from "flowbite-svelte";
  import type { DatasetSchema } from "../../backendapi";

  import { showBackgroundDistMap, showSegmentValues } from "../../stores";
  import SaveTableToFile from "../SaveTableToFile.svelte";

  export let datasets: Record<string, DatasetSchema>;
  export let currentDatasetName: string;
  export let updateData: () => void;
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
    <h3 class="text-base">Dataset</h3>

    <div class="flex gap-2 items-center">
      <Select
        size="sm"
        items={Object.values(datasets).map((k) => ({
          value: k.name,
          name: k.origin === "example" ? `${k.name} (example)` : k.name,
        }))}
        placeholder="Select dataset"
        bind:value={currentDatasetName}
        on:change={updateData}
      />

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
        class="hover:bg-gray-100 bg-gray-50 rounded border px-2 border-gray-200"
        on:click={() => setBackgroundDist(true)}
      >
        On
      </button>
      <button
        class="hover:bg-gray-100 bg-gray-50 rounded border px-2 border-gray-200"
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
