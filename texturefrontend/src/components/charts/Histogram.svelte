<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import { mosaicSelection, clearColumnSelections } from "../../stores";
  import { getPlot } from "./chartUtils";
  import { getUUID } from "../../shared/utils";

  export let columnName: string;
  export let mainDatasetName: string;
  export let showBackground = true;
  export let shouldBin = true;

  let uuid = getUUID();

  let el: HTMLElement;
  let plotWrapper;

  let thisSelection = vg.Selection.single();
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
    table: string,
    col: string,
    shouldBin: boolean,
    selection,
  ) {
    // FUTURE: this chart breaks if the col has null values; use a view or selection to filter out nulls or fix bins

    let interactors;

    if (shouldBin) {
      interactors = [vg.intervalX({ as: $mosaicSelection })];
    } else {
      interactors = [
        vg.toggleX({ as: selection }),
        vg.highlight({ by: selection }),
        vg.toggleX({ as: $mosaicSelection }),
      ];
    }

    const plotDirectives = [
      vg.rectY(vg.from(table, { filterBy: $mosaicSelection }), {
        x: shouldBin ? vg.bin(col) : col,
        y: vg.count(),
        fill: "steelblue",
        inset: 0.5,
      }),
      ...interactors,
      vg.xDomain(vg.Fixed),
      vg.width(400),
      vg.height(150),
      vg.axisX({ label: null }),
      vg.axisY({ label: null }),
      vg.margins({ top: 10, right: 15, left: 40 }),
    ];

    if (showBackground) {
      plotDirectives.unshift(
        vg.rectY(vg.from(table), {
          x: shouldBin ? vg.bin(col) : col,
          y: vg.count(),
          fill: "#ccc",
          fillOpacity: 0.4,
          inset: 0.5,
        }),
      );
    }

    plotWrapper = getPlot(...plotDirectives);

    el.replaceChildren(plotWrapper.element);
  }

  // This re-renders unnecessarily but is required or else will not re-render on $brush updates
  afterUpdate(() =>
    renderChart(mainDatasetName, columnName, shouldBin, thisSelection),
  );

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
