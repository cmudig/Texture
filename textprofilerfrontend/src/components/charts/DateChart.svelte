<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import { mosaicSelection } from "../../stores";
  import { getPlot, dateLayout } from "./chartUtils";

  export let columnName: string;
  export let mainDatasetName: string;

  let el: HTMLElement;
  let plotWrapper;

  const layout = dateLayout;

  // FUTURE: if vg.bin() works for dates might be nice here so less crowded line...
  function renderChart(datasetName: string, cName: string) {
    let fromClause: any = datasetName;

    plotWrapper = getPlot(
      vg.lineY(vg.from(fromClause, { filterBy: $mosaicSelection }), {
        x: cName,
        y: vg.count(),
        stroke: layout.color,
        curve: "monotone-x",
      }),
      vg.intervalX({ as: $mosaicSelection }),
      vg.xDomain(vg.Fixed),
      vg.marginLeft(layout.marginLeft),
      vg.width(layout.width),
      vg.height(layout.height),
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
