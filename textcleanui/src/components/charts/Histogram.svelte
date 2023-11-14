<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { onMount } from "svelte";

  export let datasetName: string;
  export let columnName: string;
  export let brush: any;

  let el: HTMLElement;

  function renderChart() {
    let c = vg.plot(
      vg.rectY(vg.from(datasetName, { filterBy: brush }), {
        x: vg.bin(columnName),
        y: vg.count(),
        fill: "steelblue",
        inset: 0.5,
      }),
      vg.intervalX({ as: brush }),
      vg.xDomain(vg.Fixed),
      vg.marginLeft(55),
      vg.width(400),
      vg.height(150)
    );

    el.replaceChildren(c);
  }

  onMount(renderChart);
</script>

<div bind:this={el} />
