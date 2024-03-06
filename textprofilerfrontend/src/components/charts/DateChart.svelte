<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import { mosaicSelection } from "../../stores";
  import { getPlot } from "./chartUtils";

  export let columnName: string;
  export let mainDatasetName: string;

  let el: HTMLElement;
  let plotWrapper;

  // FUTURE: if vg.bin() works for dates might be nice here so less crowded line...
  function renderChart(datasetName: string, cName: string) {
    let fromClause: any = datasetName;

    plotWrapper = getPlot(
      vg.lineY(vg.from(fromClause, { filterBy: $mosaicSelection }), {
        x: cName,
        y: vg.count(),
        stroke: "steelblue",
        curve: "monotone-x",
      }),
      vg.intervalX({ as: $mosaicSelection }),
      vg.xDomain(vg.Fixed),
      vg.width(400),
      vg.height(150),
      vg.axisX({ label: null }),
      vg.axisY({ label: null }),
      vg.margins({ top: 10, right: 15, left: 25 }),
    );

    el.replaceChildren(plotWrapper.element);
  }

  afterUpdate(() => renderChart(mainDatasetName, columnName));

  onDestroy(() => {
    if (plotWrapper) {
      plotWrapper.marks.forEach((mark) => vg.coordinator().disconnect(mark));
    }
  });
</script>

<div bind:this={el} />
