<script lang="ts">
  import { Button } from "flowbite-svelte";
  import { PlusSolid } from "flowbite-svelte-icons";
  import type { ColumnSummary } from "../shared/types";
  import ColumnProfile from "./ColumnProfile.svelte";
  import ProjectionOverview from "./ProjectionOverview.svelte";
  import { datasetSchema } from "../stores";
  import SimilaritySearch from "./SimilaritySearch.svelte";

  export let datasetColSummaries: Map<string, ColumnSummary>;
  export let showAddColModal: boolean;
  export let allowDeriveNew: boolean;
</script>

<div class="flex flex-col h-full overflow-y-auto">
  {#if allowDeriveNew}
    <div class="flex justify-center py-2">
      <Button on:click={() => (showAddColModal = true)} size="sm">
        <PlusSolid size="sm" class="mr-2" />
        Derive New Column
      </Button>
    </div>
  {/if}

  <SimilaritySearch />

  <ProjectionOverview
    colorCols={$datasetSchema.columns.filter(
      (c) => c.type === "categorical" && !c.derivedSchema,
    )}
  />

  {#each $datasetSchema.columns as col}
    <ColumnProfile
      displayCol={col}
      colSummary={datasetColSummaries.get(col.name)}
    />
  {/each}
</div>
