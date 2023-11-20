<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate } from "svelte";
  import { filters } from "../../stores";

  export let datasetName: string;
  export let columnName: string;

  let el: HTMLElement;

  function renderChart() {
    let c = vg.search({
      as: $filters.brush,
      from: datasetName,
      column: columnName,
      type: "contains",
    });

    el.replaceChildren(c);
  }

  afterUpdate(renderChart);
</script>

<div class="summaryChart my-2" bind:this={el} />
