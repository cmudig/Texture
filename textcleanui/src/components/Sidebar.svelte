<script lang="ts">
  import type { DatasetInfo } from "../shared/types";
  import ColumnProfile from "./ColumnProfile.svelte";

  export let datasetInfo: DatasetInfo;
  export let brush: any;
</script>

<div class="border-2 border-slate-50">
  {#each datasetInfo.metadata.text_columns as colName}
    <ColumnProfile
      {colName}
      colType={"text"}
      chartColNames={datasetInfo.metadata.text_meta_columns[colName]}
      datasetName={datasetInfo.name}
      {brush}
    />
  {/each}
</div>
