<script lang="ts">
  import { Button } from "flowbite-svelte";
  import { PlusSolid } from "flowbite-svelte-icons";
  import type { ColumnSummary } from "../shared/types";
  import ColumnProfile from "./ColumnProfile.svelte";
  import ProjectionOverview from "./ProjectionOverview.svelte";
  import { datasetInfo } from "../stores";

  export let datasetColSummaries: Map<string, ColumnSummary>;
  export let showAddColModal;
</script>

<div class="flex flex-col">
  <div class="flex justify-center py-2">
    <Button on:click={() => (showAddColModal = true)} size="sm">
      <PlusSolid size="sm" class="mr-2" />
      Derive New Column
    </Button>
  </div>

  <ProjectionOverview />

  {#each $datasetInfo.columns as col}
    <!-- Dont make row entry for text cols -->
    {#if col.type === "categorical" || col.type === "number" || col.type === "date"}
      <ColumnProfile
        displayCol={col}
        colSummary={datasetColSummaries.get(col.name)}
      />
    {/if}
  {/each}
</div>
