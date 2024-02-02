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
  export let limit = 10;

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
        // including this breaks the click interation and doesnt cut off text?
        // vg.axisY({
        //   textOverflow: "ellipsis",
        //   lineWidth: 50,
        // }),
        vg.barX(vg.from(fromClause), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: "#ccc",
          fillOpacity: 0.4,
          sort: { y: "-x", limit },
        }),
        vg.barX(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: "steelblue",
          sort: { y: "-x", limit },
        }),
        vg.highlight({ by: selection }),
        vg.toggleY({ as: selection }),
        vg.toggleY({ as: $filters.brush }),
        vg.text(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: cName,
          order: cName,
          sort: { y: "-x", limit },
          text: vg.count(),
          dx: 5,
          textAnchor: "start",
        }),
        vg.yLabel(null),
        vg.marginLeft(80),
        vg.width(400),
      );
    } else {
      plotWrapper = getPlot(
        vg.barX(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: "steelblue",
          sort: { y: "-x", limit },
        }),
        vg.highlight({ by: selection }),
        vg.toggleY({ as: selection }),
        vg.toggleY({ as: $filters.brush }),
        vg.text(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: cName,
          order: cName,
          sort: { y: "-x", limit },
          text: vg.count(),
          dx: 5,
          textAnchor: "start",
        }),
        vg.yLabel(null),
        vg.marginLeft(80),
        vg.width(400),
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

<button on:click={resetSelection}> reset selection</button>

<div class="summaryChart" bind:this={el} />
