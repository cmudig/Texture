<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import { mosaicSelection, sidebarWidth } from "../../stores";
  import { getPlot } from "./chartUtils";

  export let columnName: string;
  export let mainDatasetName: string;
  $: width = $sidebarWidth - 50;

  let el: HTMLElement;
  let plotWrapper;

  // FUTURE: if vg.bin() works for dates might be nice here so less crowded line...
  function renderChart(table: string, col: string, chartWidth) {
    plotWrapper = getPlot(
      vg.lineY(vg.from(table, { filterBy: $mosaicSelection }), {
        x: col,
        y: vg.count(),
        stroke: "steelblue",
        curve: "monotone-x",
      }),
      vg.intervalX({ as: $mosaicSelection }),
      vg.xDomain(vg.Fixed),
      vg.width(chartWidth),
      vg.height(150),
      vg.axisX({ label: null }),
      vg.axisY({ label: null }),
      vg.margins({ top: 10, right: 15, left: 25 }),
    );

    el.replaceChildren(plotWrapper.element);
  }

  afterUpdate(() => renderChart(mainDatasetName, columnName, width));

  onDestroy(() => {
    if (plotWrapper) {
      plotWrapper.marks.forEach((mark) => vg.coordinator().disconnect(mark));
    }
  });
</script>

<div bind:this={el} />
