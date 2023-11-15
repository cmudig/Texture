<script lang="ts">
  import Histogram from "./charts/Histogram.svelte";
  import DateChart from "./charts/DateChart.svelte";
  import CategoricalChart from "./charts/CategoricalChart.svelte";
  import type { Column } from "../shared/types";

  export let columns: Column[];
  export let datasetName: string;
</script>

<!-- TODO: can use svelte components or something to render the correct chart type -->

<div class="flex flex-col">
  {#each columns as col}
    {#if col.type === "number"}
      <Histogram {datasetName} columnName={col.name} />
    {:else if col.type === "categorical"}
      <CategoricalChart {datasetName} columnName={col.name} />
    {:else if col.type === "date"}
      <!-- <DateChart {datasetName} columnName={col.name} /> -->
      TODO: Date chart...
    {:else}
      <div>{col.name}: Unsupported column type ({col.type})</div>
    {/if}
  {/each}
</div>
