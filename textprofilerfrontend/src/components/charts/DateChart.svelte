<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate } from "svelte";
  import { filters } from "../../stores";

  export let columnName: string;

  let el: HTMLElement;

  // FUTURE: if vg.bin() works for dates might be nice here so less crowded line...
  function renderChart() {
    let c = vg.plot(
      vg.lineY(vg.from($filters.datasetName, { filterBy: $filters.brush }), {
        x: columnName,
        y: vg.count(),
        stroke: "steelblue",
        curve: "monotone-x",
      }),
      vg.intervalX({ as: $filters.brush }),
      vg.xDomain(vg.Fixed),
      vg.marginLeft(55),
      vg.width(400),
      vg.height(150),
    );

    el.replaceChildren(c);
  }

  afterUpdate(renderChart);
</script>

<div bind:this={el} />
