<script lang="ts">
  import type { ColumnSummary } from "../shared/types";
  import type { DatasetInfo } from "../backendapi/models/DatasetInfo";
  import ColumnProfile from "./ColumnProfile.svelte";
  import ProjectionOverview from "./ProjectionOverview.svelte";

  export let datasetInfo: DatasetInfo;
  export let datasetColSummaries: ColumnSummary[];

  // probably better to turn datasetColSummaries into a Map then index rather than find cuz that slow
</script>

<div>
  <ProjectionOverview />

  {#each datasetInfo.column_info as col}
    {#if col.type == "text"}
      <ColumnProfile
        displayCol={col}
        colType="text"
        plotCols={datasetInfo.column_info.filter(
          (c) => c.associated_text_col_name === col.name,
        )}
        colSummary={datasetColSummaries.find((c) => c.column_name === col.name)}
      />
    {:else if col.associated_text_col_name == null}
      <!-- only plot metadata without associated text column so those already plotted -->
      <ColumnProfile
        displayCol={col}
        plotCols={datasetInfo.column_info.filter((c) => c.name === col.name)}
        colSummary={datasetColSummaries.find((c) => c.column_name === col.name)}
      />
    {/if}
  {/each}
</div>
