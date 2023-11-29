<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate } from "svelte";
  import { filters } from "../../stores";

  export let columnName: string;

  let el: HTMLElement;

  function renderChart() {
    // TODO: the suggestions here are not distinct for some reason? They are supposed to be...
    let c = vg.search({
      as: $filters.brush,
      from: $filters.datasetName,
      column: columnName,
      type: "contains",
    });

    el.replaceChildren(c);
  }

  afterUpdate(renderChart);
</script>

<div class="summaryChart my-2" bind:this={el} />
