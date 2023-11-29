<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate } from "svelte";
  import { filters, showBackgroundDist } from "../../stores";

  export let columnName: string;

  let el: HTMLElement;

  function renderChart() {
    let c;

    if ($showBackgroundDist) {
      c = vg.plot(
        vg.rectY(vg.from($filters.datasetName), {
          x: vg.bin(columnName),
          y: vg.count(),
          fill: "#ccc",
          fillOpacity: 0.4,
          inset: 0.5,
        }),
        vg.rectY(vg.from($filters.datasetName, { filterBy: $filters.brush }), {
          x: vg.bin(columnName),
          y: vg.count(),
          fill: "steelblue",
          inset: 0.5,
        }),
        vg.intervalX({ as: $filters.brush }),
        vg.xDomain(vg.Fixed),
        vg.marginLeft(55),
        vg.width(400),
        vg.height(150)
      );
    } else {
      c = vg.plot(
        vg.rectY(vg.from($filters.datasetName, { filterBy: $filters.brush }), {
          x: vg.bin(columnName),
          y: vg.count(),
          fill: "steelblue",
          inset: 0.5,
        }),
        vg.intervalX({ as: $filters.brush }),
        vg.xDomain(vg.Fixed),
        vg.marginLeft(55),
        vg.width(400),
        vg.height(150)
      );
    }

    el.replaceChildren(c);
  }

  // This re-renders unnecessarily but is required or else will not re-render on $brush updates
  afterUpdate(renderChart);
</script>

<div bind:this={el} />
