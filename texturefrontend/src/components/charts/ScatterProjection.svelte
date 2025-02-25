<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import {
    mosaicSelection,
    clearColumnSelections,
    sidebarWidth,
  } from "../../stores";
  import { getUUID } from "../../shared/utils";
  import { getPlot } from "./chartUtils";

  export let columnX: string;
  export let columnY: string;
  export let mainDatasetName: string;
  export let colorColName: string | undefined = undefined;
  export let opacity: number = 0.4;

  $: width = $sidebarWidth - 50;
  let el: HTMLElement;
  let plotWrapper;
  let thisSelection = vg.Selection.single();
  let uuid = getUUID();
  $: saveSelectionToCache(thisSelection, `${columnX}_${columnY}`);

  function resetSelection(s) {
    s.clauses.forEach((clause) => {
      s.update({
        ...clause,
        value: null,
        predicate: null,
      });
    });
  }

  function saveSelectionToCache(selection, name) {
    $clearColumnSelections = [
      ...$clearColumnSelections,
      {
        clearFunc: () => resetSelection(selection),
        sourceId: uuid,
        colName: name,
      },
    ];
  }

  function destroy() {
    if (plotWrapper) {
      console.log("destroying scatter projection");
      plotWrapper.marks.forEach((mark) => vg.coordinator().disconnect(mark));

      $clearColumnSelections = $clearColumnSelections.filter(
        (s) => s.sourceId !== uuid,
      );
    }
  }

  async function renderChart(
    table: string,
    colX: string,
    colY: string,
    selection: any,
    colorCol: string | undefined,
    opacity = 0.4,
    chartWidth: number,
  ) {
    destroy(); // TODO: this in incredibly inefficient, should use a param or something so do not need to re-render
    plotWrapper = getPlot(
      vg.name("projectionView"),
      vg.dot(vg.from(table), {
        x: colX,
        y: colY,
        r: 2,
        fill: "#ccc",
        fillOpacity: 0.2,
      }),
      vg.dot(vg.from(table, { filterBy: $mosaicSelection }), {
        x: colX,
        y: colY,
        r: 2,
        fill: colorCol ?? "steelblue",
        fillOpacity: opacity,
      }),
      vg.axis(null), // TODO: look at axis bc points bleed over
      vg.highlight({ by: selection, opacity: 0.1 }),
      vg.intervalXY({ as: selection }),
      vg.intervalXY({ as: $mosaicSelection }),
      vg.width(chartWidth),
      vg.height(200),
      vg.margins({ top: 10, right: 10, left: 10, bottom: 10 }),
    );

    el.replaceChildren(plotWrapper.element); //, legend.element);
  }

  afterUpdate(() => {
    renderChart(
      mainDatasetName,
      columnX,
      columnY,
      thisSelection,
      colorColName,
      opacity,
      width,
    );
  });

  onDestroy(() => destroy());
</script>

<div bind:this={el} />
