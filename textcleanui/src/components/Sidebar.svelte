<script lang="ts">
  import type { DatasetInfo } from "../shared/types";
  import ChartGroup from "./ChartGroup.svelte";

  export let datasetInfo: DatasetInfo;
  export let brush: any;
</script>

<div class="border-2 border-slate-50">
  {#each datasetInfo.metadata.text_columns as colName}
    <div>
      <h2 class="font-bold">{colName}</h2>
      <div class="ml-4">
        <ChartGroup
          colNames={datasetInfo.metadata.text_meta_columns[colName]}
          datasetName={datasetInfo.name}
          {brush}
        />
      </div>
    </div>
  {/each}
</div>
