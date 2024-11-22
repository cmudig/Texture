<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import { mosaicSelection, clearColumnSelections } from "../../stores";
  import { getUUID } from "../../shared/utils";
  import { getPlot } from "./chartUtils";

  export let columnX: string;
  export let columnY: string;
  export let mainDatasetName: string;
  export let colorColName: string | undefined = undefined;

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

  async function renderChart(
    table: string,
    colX: string,
    colY: string,
    selection: any,
    colorCol: string | undefined,
  ) {
    plotWrapper = getPlot(
      vg.name("projectionView"),
      vg.dot(vg.from(table), {
        x: colX,
        y: colY,
        r: 2,
        fill: "#ccc",
        fillOpacity: 0.4,
      }),
      vg.dot(vg.from(table, { filterBy: $mosaicSelection }), {
        x: colX,
        y: colY,
        r: 2,
        fill: colorCol ?? "steelblue",
      }),
      vg.axis(null),
      vg.highlight({ by: selection, opacity: 0.1 }),
      vg.intervalXY({ as: selection }),
      vg.intervalXY({ as: $mosaicSelection }),
      vg.width(400),
      vg.height(250),
      vg.margins({ top: 10, right: 10, left: 10, bottom: 10 }),
    );

    el.replaceChildren(plotWrapper.element); //, legend.element);
  }

  afterUpdate(() => {
    renderChart(mainDatasetName, columnX, columnY, thisSelection, colorColName);
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
