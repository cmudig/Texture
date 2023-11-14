<script lang="ts">
  import Histogram from "./charts/Histogram.svelte";

  export let colNames: string[];
  export let brush: any;
  export let datasetName: string;
</script>

<div class="flex flex-col">
  {#each colNames as col}
    <Histogram {datasetName} columnName={col} {brush} />
  {/each}
</div>
