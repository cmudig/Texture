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
