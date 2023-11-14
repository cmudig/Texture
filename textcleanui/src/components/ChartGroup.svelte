<script lang="ts">
  import Histogram from "./charts/Histogram.svelte";

  export let groupName: string;
  export let colNames: string[];
  export let brush: any;
  export let datasetName: string;
</script>

<div>
  <h3>{groupName} metrics</h3>
  <div class="flex flex-col">
    {#each colNames as col}
      <Histogram {datasetName} columnName={col} {brush} />
    {/each}
  </div>
</div>
