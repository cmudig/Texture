<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import { mosaicSelection } from "../../stores";
  import { getDatasetName } from "../../shared/utils";
  import { getPlot, histogramLayout } from "./chartUtils";

  export let columnName: string;
  export let mainDatasetName: string;
  export let showBackground = true;
  export let plotNulls = false;

  const layout = histogramLayout;

  let el: HTMLElement;
  let plotWrapper;

  async function renderChart(
    mainDsName: string,
    cName: string,
    pltNullsFlag: boolean,
  ) {
    let datasetName = await getDatasetName(mainDsName, cName, pltNullsFlag);

    let fromClause: any = datasetName;

    if (showBackground) {
      plotWrapper = getPlot(
        vg.rectY(vg.from(fromClause), {
          x: vg.bin(columnName, { steps: layout.steps }),
          y: vg.count(),
          fill: "#ccc",
          fillOpacity: 0.4,
          inset: layout.inset,
        }),
        vg.rectY(vg.from(fromClause, { filterBy: $mosaicSelection }), {
          x: vg.bin(columnName, { steps: layout.steps }),
          y: vg.count(),
          fill: layout.color,
          inset: layout.inset,
        }),
        vg.intervalX({ as: $mosaicSelection }),
        vg.xDomain(vg.Fixed),
        vg.marginLeft(layout.marginLeft),
        vg.width(layout.width),
        vg.height(layout.height),
        vg.axisY({ textOverflow: "ellipsis", lineWidth: layout.axisLineWidth }),
      );
    } else {
      plotWrapper = getPlot(
        vg.rectY(vg.from(fromClause, { filterBy: $mosaicSelection }), {
          x: vg.bin(columnName, { steps: layout.steps }),
          y: vg.count(),
          fill: layout.color,
          inset: layout.inset,
        }),
        vg.intervalX({ as: $mosaicSelection }),
        vg.xDomain(vg.Fixed),
        vg.marginLeft(layout.marginLeft),
        vg.width(layout.width),
        vg.height(layout.height),
        vg.axisY({ textOverflow: "ellipsis", lineWidth: layout.axisLineWidth }),
      );
    }

    el.replaceChildren(plotWrapper.element);
  }

  // This re-renders unnecessarily but is required or else will not re-render on $brush updates
  afterUpdate(() => renderChart(mainDatasetName, columnName, plotNulls));

  onDestroy(() => {
    if (plotWrapper) {
      plotWrapper.marks.forEach((mark) => vg.coordinator().disconnect(mark));
    }
  });
</script>

<div bind:this={el} />
