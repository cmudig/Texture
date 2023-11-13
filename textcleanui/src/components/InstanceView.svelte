<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { onMount } from "svelte";

  export let textColumns: string[];
  export let datasetName: string;
  export let brush: any;

  let el: HTMLElement;

  function renderChart() {
    let table: HTMLElement = vg.table({
      from: datasetName,
      height: 1200,
      width: "100%",
      filterBy: brush,
      columns: textColumns,
    });

    el.replaceChildren(table);
  }

  onMount(renderChart);
</script>

<div class="border-2 border-slate-50">
  <div bind:this={el} />
</div>
