<script lang="ts">
  import type { DatasetInfo } from "../shared/types";
  import ColumnProfile from "./ColumnProfile.svelte";

  export let datasetInfo: DatasetInfo;
</script>

<div class="border-2 border-slate-50">
  {#each datasetInfo.metadata.text_columns as col}
    <ColumnProfile
      displayCol={col}
      plotCols={datasetInfo.metadata.text_meta_columns[col.name]}
      datasetName={datasetInfo.name}
    />
  {/each}
  {#each datasetInfo.metadata.other_columns as col}
    <ColumnProfile
      displayCol={col}
      plotCols={[col]}
      datasetName={datasetInfo.name}
    />
  {/each}
</div>
