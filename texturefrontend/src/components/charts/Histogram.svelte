<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import { mosaicSelection } from "../../stores";
  import { getPlot } from "./chartUtils";

  export let columnName: string;
  export let mainDatasetName: string;
  export let showBackground = true;

  let el: HTMLElement;
  let plotWrapper;

  async function renderChart(table: string, col: string) {
    // FUTURE: this chart breaks if the col has null values; use a view or selection to filter out nulls or fix bins

    if (showBackground) {
      plotWrapper = getPlot(
        vg.rectY(vg.from(table), {
          x: vg.bin(col),
          y: vg.count(),
          fill: "#ccc",
          fillOpacity: 0.4,
          inset: 0.5,
        }),
        vg.rectY(vg.from(table, { filterBy: $mosaicSelection }), {
          x: vg.bin(col),
          y: vg.count(),
          fill: "steelblue",
          inset: 0.5,
        }),
        vg.intervalX({ as: $mosaicSelection }),
        vg.xDomain(vg.Fixed),
        vg.width(400),
        vg.height(150),
        vg.axisX({ label: null }),
        vg.axisY({ label: null }),
        vg.margins({ top: 10, right: 15, left: 40 }),
      );
    } else {
      plotWrapper = getPlot(
        vg.rectY(vg.from(table, { filterBy: $mosaicSelection }), {
          x: vg.bin(col),
          y: vg.count(),
          fill: "steelblue",
          inset: 0.5,
        }),
        vg.intervalX({ as: $mosaicSelection }),
        vg.xDomain(vg.Fixed),
        vg.width(400),
        vg.height(150),
        vg.axisX({ label: null }),
        vg.axisY({ label: null }),
        vg.margins({ top: 10, right: 15, left: 40 }),
      );
    }

    el.replaceChildren(plotWrapper.element);
  }

  // This re-renders unnecessarily but is required or else will not re-render on $brush updates
  afterUpdate(() => renderChart(mainDatasetName, columnName));

  onDestroy(() => {
    if (plotWrapper) {
      plotWrapper.marks.forEach((mark) => vg.coordinator().disconnect(mark));
    }
  });
</script>

<div bind:this={el} />
