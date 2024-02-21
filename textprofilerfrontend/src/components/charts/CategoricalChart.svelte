<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import { mosaicSelection, clearColumnSelections } from "../../stores";
  import { getDatasetName, getUUID } from "../../shared/utils";
  import { getPlot, categoricalLayout } from "./chartUtils";
  import { reduce } from "lodash";
  import { databaseConnection } from "../../stores";

  export let columnName: string;
  export let mainDatasetName: string;
  export let showBackground = true;
  export let plotNulls = true;
  export let limit = 10;
  export let excludeList: string[] | undefined = undefined;

  const layout = categoricalLayout;

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
    _excludeList?: string[],
  ) {
    let datasetName = await getDatasetName(
      mainDsName,
      cName,
      pltNullsFlag,
      _excludeList,
    );
    let fromClause: any = datasetName;

    let colCount = await databaseConnection.getColCount(fromClause, cName);
    colCount = Math.min(limit, colCount);
    const height =
      colCount * layout.barHeight +
      (colCount - 1) * (layout.inset + 1) +
      layout.marginTop +
      layout.marginBottom;

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
          inset: layout.inset,
        }),
        vg.barX(vg.from(fromClause, { filterBy: $mosaicSelection }), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: layout.color,
          sort: { y: "-x", limit },
          inset: layout.inset,
        }),
        vg.highlight({ by: selection }),
        vg.toggleY({ as: selection }),
        vg.toggleY({ as: $mosaicSelection }),
        vg.text(vg.from(fromClause, { filterBy: $mosaicSelection }), {
          x: vg.count(),
          y: cName,
          order: cName,
          sort: { y: "-x", limit },
          text: vg.count(),
          dx: 5,
          textAnchor: "start",
          textOverflow: "ellipsis",
          lineWidth: layout.textLineWidth,
        }),
        vg.yLabel(null),
        vg.marginLeft(layout.marginLeft),
        vg.marginRight(layout.marginRight),
        vg.marginTop(layout.marginTop),
        vg.marginBottom(layout.marginBottom),
        vg.width(layout.width),
        vg.height(height),
        vg.axisY({ textOverflow: "ellipsis", lineWidth: layout.axisLineWidth }),
      );
    } else {
      plotWrapper = getPlot(
        vg.barX(vg.from(fromClause, { filterBy: $mosaicSelection }), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: layout.color,
          sort: { y: "-x", limit },
          inset: layout.inset,
        }),
        vg.highlight({ by: selection }),
        vg.toggleY({ as: selection }),
        vg.toggleY({ as: $mosaicSelection }),
        vg.text(vg.from(fromClause, { filterBy: $mosaicSelection }), {
          x: vg.count(),
          y: cName,
          order: cName,
          sort: { y: "-x", limit },
          text: vg.count(),
          dx: 5,
          textAnchor: "start",
          textOverflow: "ellipsis",
          lineWidth: layout.textLineWidth,
        }),
        vg.yLabel(null),
        vg.marginLeft(layout.marginLeft),
        vg.marginRight(layout.marginRight),
        vg.marginTop(layout.marginTop),
        vg.marginBottom(layout.marginBottom),
        vg.width(layout.width),
        vg.height(height),
        vg.axisY({ textOverflow: "ellipsis", lineWidth: layout.axisLineWidth }),
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
      excludeList,
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

<div class="summaryChart" bind:this={el} />
