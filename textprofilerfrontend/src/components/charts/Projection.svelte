<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import { filters, clearColumnSelections } from "../../stores";
  import type { JoinInfo } from "../../backendapi";
  import { getDatasetName, getUUID } from "../../shared/utils";
  import { getPlot } from "./chartUtils";

  export let columnName: string;
  export let mainDatasetName: string;
  export let joinDatasetInfo: JoinInfo | undefined = undefined;
  export let showBackground = true;
  export let plotNulls = true;

  let el: HTMLElement;
  let plotWrapper;
  let thisSelection = vg.Selection.single();
  // let xs = vg.Selection.intersect();
  // let ys = vg.Selection.intersect();
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
    joinDsInfo?: JoinInfo,
  ) {

    let datasetName = await getDatasetName(mainDsName, cName, pltNullsFlag);
    let fromClause: any = datasetName;

    if (joinDsInfo) {
      fromClause = vg.fromJoinDistinct({
        table: datasetName,
        rightTable: joinDsInfo.joinDatasetName,
        joinKey: joinDsInfo.joinKey,
      });
    }

    if (showBackground) {
      plotWrapper = getPlot(
        // vg.frame(),
        vg.dot(vg.from(fromClause), {
          x: "x",
          y: "y",
          r: 1,
          fill: "#ccc",
          fillOpacity: 0.4,
          // clip: true,
        }),
        vg.dot(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: "x",
          y: "y",
          r: 1,
          fill: "steelblue",
          // clip: true,
        }),
        vg.xAxis(null),
        vg.yAxis(null),
        // vg.margins({"top":20,"bottom":20,"left":20,"right":20}),
        vg.highlight({ by: selection, opacity: 0.1 }),
        vg.intervalXY({ as: selection }),
        vg.intervalXY({ as: $filters.brush }),
        // vg.panZoom({ x: xs, y: ys }),
        vg.width(400),
        vg.height(280),
      );
    } else {
      plotWrapper = getPlot(
        vg.barX(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: "x",
          y: "y",
          r: 1,
          fill: "steelblue",
          clip: true,
        }),
        vg.xAxis(null),
        vg.yAxis(null),
        // vg.margins({"top":20,"bottom":20,"left":20,"right":20}),
        vg.intervalXY({ as: selection }),
        vg.highlight({ by: selection, opacity: 0.1 }),
        vg.intervalXY({ as: $filters.brush }),
        // vg.panZoom({ x: xs, y: ys }),
        vg.width(400),
        vg.height(280),
      );
    }

    el.replaceChildren(plotWrapper.element);
  }

  afterUpdate(() => {
    renderChart(
      mainDatasetName,
      columnName,
      plotNulls,
      thisSelection,
      joinDatasetInfo,
    );
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
  