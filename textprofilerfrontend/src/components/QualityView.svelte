<script lang="ts">
  import type { DatasetInfo } from "../shared/types";
  import QualityTab from "./QualityTab.svelte";

  export let datasetInfo: DatasetInfo;
</script>

<div>
  {#if datasetInfo.metadata.text_quality_info}
    {#each datasetInfo.metadata.text_quality_info as qualityInfo}
      <QualityTab {qualityInfo} />
    {/each}
  {:else}
    <div class="p-4">No quality metrics for this dataset.</div>
  {/if}
</div>
