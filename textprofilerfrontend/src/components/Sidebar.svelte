<script lang="ts">
  import type { ColumnSummary } from "../shared/types";
  import ColumnProfile from "./ColumnProfile.svelte";
  import ProjectionOverview from "./ProjectionOverview.svelte";
  import { datasetInfo } from "../stores";

  export let datasetColSummaries: Map<string, ColumnSummary>;
</script>

<div>
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
