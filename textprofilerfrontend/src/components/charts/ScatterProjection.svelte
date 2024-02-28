<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import { mosaicSelection, clearColumnSelections } from "../../stores";
  import { getDatasetName, getUUID } from "../../shared/utils";
  import { getPlot } from "./chartUtils";

  export let columnName: string;
  export let mainDatasetName: string;
  export let plotNulls = true;

  let el: HTMLElement;
  let plotWrapper;
  let thisSelection = vg.Selection.single();

  let uuid = getUUID();
  $: saveSelectionToCache(thisSelection, columnName);

  function resetSelection(s) {
    s.clauses.forEach((clause) => {
      s.update({
        ...clause,
        value: null,
        predicate: null,
      });
    });
  }

  function saveSelectionToCache(s, name) {
    $clearColumnSelections = [
      ...$clearColumnSelections,
      {
        clearFunc: () => resetSelection(s),
        sourceId: uuid,
        colName: name,
      },
    ];
  }

  async function renderChart(
    mainDsName: string,
    cName: string,
    pltNullsFlag: boolean,
    selection: any,
  ) {
    let datasetName = await getDatasetName(mainDsName, cName, pltNullsFlag);
    let fromClause: any = datasetName;

    plotWrapper = getPlot(
      vg.dot(vg.from(fromClause), {
        x: "umap_x",
        y: "umap_y",
        r: 1.5,
        fill: "#ccc",
        fillOpacity: 0.4,
      }),
      vg.dot(vg.from(fromClause, { filterBy: $mosaicSelection }), {
        x: "umap_x",
        y: "umap_y",
        r: 1.5,
        fill: "steelblue",
      }),
      vg.xAxis(null),
      vg.yAxis(null),
      vg.highlight({ by: selection, opacity: 0.1 }),
      vg.intervalXY({ as: selection }),
      vg.intervalXY({ as: $mosaicSelection }),
      vg.width(400),
      vg.height(280),
    );

    el.replaceChildren(plotWrapper.element);
  }

  afterUpdate(() => {
    renderChart(mainDatasetName, columnName, plotNulls, thisSelection);
  });

  onDestroy(() => {
    if (plotWrapper) {
      plotWrapper.marks.forEach((mark) => vg.coordinator().disconnect(mark));

      $clearColumnSelections = $clearColumnSelections.filter(
        (s) => s.sourceId !== uuid,
      );
    }
  });
</script>

<div bind:this={el} />
