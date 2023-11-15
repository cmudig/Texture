<script lang="ts">
  import Histogram from "./charts/Histogram.svelte";
  import type { Column } from "../shared/types";

  export let columns: Column[];
  export let brush: any;
  export let datasetName: string;
</script>

<div class="flex flex-col">
  {#each columns as col}
    {#if col.type === "number"}
      <Histogram {datasetName} columnName={col.name} {brush} />
    {:else}
      <div>{col.name}: Unsupported column type ({col.type})</div>
    {/if}
  {/each}
</div>
