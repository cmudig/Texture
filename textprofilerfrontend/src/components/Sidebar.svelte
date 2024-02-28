<script lang="ts">
  import type { ColumnSummary } from "../shared/types";
  import ColumnProfile from "./ColumnProfile.svelte";
  import ProjectionOverview from "./ProjectionOverview.svelte";
  import { datasetInfo } from "../stores";

  export let datasetColSummaries: ColumnSummary[];

  // probably better to turn datasetColSummaries into a Map then index rather than find cuz that slow
</script>

<div>
  <ProjectionOverview />

  {#each $datasetInfo.columns as col}
    {#if col.type == "text"}
      <ColumnProfile
        displayCol={col}
        colType="text"
        plotCols={$datasetInfo.columns.filter(
          (c) => c.derived_from === col.name,
        )}
        colSummary={datasetColSummaries.find((c) => c.column_name === col.name)}
      />
    {:else if col.derived_from == null}
      <!-- only plot metadata without associated text column so those already plotted -->
      <ColumnProfile
        displayCol={col}
        plotCols={$datasetInfo.columns.filter((c) => c.name === col.name)}
        colSummary={datasetColSummaries.find((c) => c.column_name === col.name)}
      />
    {/if}
  {/each}
</div>
