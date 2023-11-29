<script lang="ts">
  import type { DatasetInfo, ColumnSummary } from "../shared/types";
  import ColumnProfile from "./ColumnProfile.svelte";

  export let datasetInfo: DatasetInfo;
  export let datasetColSummaries: ColumnSummary[];
</script>

<div>
  {#each datasetInfo.metadata.text_columns as col}
    <ColumnProfile
      displayCol={col}
      plotCols={datasetInfo.metadata.text_meta_columns[col.name]}
      colSummary={datasetColSummaries.find((c) => c.column_name === col.name)}
    />
  {/each}
  {#each datasetInfo.metadata.other_columns as col}
    <ColumnProfile
      displayCol={col}
      plotCols={[col]}
      colSummary={datasetColSummaries.find((c) => c.column_name === col.name)}
    />
  {/each}
</div>
