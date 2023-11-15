<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { onMount } from "svelte";

  export let datasetName: string;
  export let columnName: string;
  export let brush: any;

  let el: HTMLElement;

  // TODO: easiest thing is to probably create a view of the date as a Q column, bin that and then get the date values
  // on the x axis label

  function renderChart() {
    // let c = vg.plot(
    //   vg.line(vg.from(datasetName, { filterBy: brush }), {
    //     x: vg.bin(columnName),
    //     y: vg.count(),
    //     fill: "steelblue",
    //     // inset: 0.5,
    //   }),
    //   vg.intervalX({ as: brush }),
    //   vg.xDomain(vg.Fixed),
    //   vg.marginLeft(55),
    //   vg.width(400),
    //   vg.height(150)
    // );
    // el.replaceChildren(c);
  }

  onMount(renderChart);
</script>

<div bind:this={el} />
