<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import {
    mosaicSelection,
    clearColumnSelections,
    derivedViewNames,
  } from "../../stores";
  import { getDatasetName, getUUID, getCacheKey } from "../../shared/utils";
  import { getPlot } from "./chartUtils";

  export let plotTableName: string;
  export let columnName: string;
  export let limit = 10;
  export let excludeList: string[] | undefined = undefined;

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
    _plotTableName: string,
    cName: string,
    selection: any,
    _excludeList?: string[],
  ) {
    let datasetName = await getDatasetName(
      _plotTableName,
      cName,
      true,
      _excludeList,
    );

    $derivedViewNames.set(
      getCacheKey({ table: _plotTableName, col: cName }),
      datasetName,
    );

    plotWrapper = getPlot(
      vg.barX(vg.from(datasetName, { filterBy: $mosaicSelection }), {
        x: vg.count(),
        y: cName,
        order: cName,
        fill: "steelblue",
        sort: { y: "-x", limit },
      }),
      vg.highlight({ by: selection }),
      vg.toggleY({ as: selection }),
      vg.toggleY({ as: $mosaicSelection }),
      vg.text(vg.from(datasetName, { filterBy: $mosaicSelection }), {
        x: vg.count(),
        y: cName,
        order: cName,
        sort: { y: "-x", limit },
        text: vg.count(),
        dx: 5,
        textAnchor: "start",
        textOverflow: "ellipsis",
        lineWidth: 3,
      }),
      vg.yLabel(null),
      vg.marginLeft(80),
      vg.width(400),
      vg.axisY({ textOverflow: "ellipsis", lineWidth: 7 }),
    );

    el.replaceChildren(plotWrapper.element);
  }

  afterUpdate(() => {
    renderChart(plotTableName, columnName, thisSelection, excludeList);
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
