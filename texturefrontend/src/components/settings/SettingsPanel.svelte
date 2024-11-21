<script lang="ts">
  import { Select, Toggle, Label, Button } from "flowbite-svelte";
  import type { DatasetInfo } from "../../backendapi";

  import { datasetInfo, showBackgroundDistMap } from "../../stores";
  import StopwordEditor from "./StopwordEditor.svelte";
  import SaveTableToFile from "../SaveTableToFile.svelte";

  export let datasets: Record<string, DatasetInfo>;
  export let currentDatasetName: string;
  export let updateData: () => void;
  export let currentColToggleStates: Record<string, boolean>;
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

<div class="flex flex-col gap-4 p-3">
  <div class="flex flex-col gap-2 pb-2 border-b-2 border-grey-300">
    <h3>Dataset</h3>

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

  <div class="flex flex-col gap-2 pb-2 border-b-2 border-grey-300">
    <h3>Stopwords</h3>
    <StopwordEditor />
  </div>

  <div class="flex flex-col gap-2">
    <h3>Display Settings</h3>

    <div class="flex gap-2 items-center">
      <input
        type="checkbox"
        class="w-4 h-4 bg-gray-100 border-gray-300 dark:ring-offset-gray-800 focus:ring-2 me-2 dark:bg-gray-700 dark:border-gray-600 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600"
        bind:checked={allowDeriveNew}
      />

      <Label>Allow derive new</Label>
    </div>

    <div>
      <Label>Background distributions</Label>

      <Button on:click={() => setBackgroundDist(true)} size="sm">All on</Button>
      <Button on:click={() => setBackgroundDist(false)} size="sm">
        All off
      </Button>
    </div>

    <div>
      <Label>Display in table</Label>
      <div class="mt-2 flex flex-col gap-1">
        {#each $datasetInfo.columns as col}
          <Toggle bind:checked={currentColToggleStates[col.name]}>
            <span class="overflow-hidden text-ellipsis">
              {col.name}
            </span>
          </Toggle>
        {/each}
      </div>
    </div>
  </div>
</div>
