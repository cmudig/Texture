<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import {
    mosaicSelection,
    clearColumnSelections,
    databaseConnection,
  } from "../../stores";
  import { getUUID } from "../../shared/utils";
  import { getPlot } from "./chartUtils";

  export let columnName: string;
  export let mainDatasetName: string;
  export let showBackground = true;
  export let limit = 10;
  export let colorColName: string | undefined = undefined;

  let el: HTMLElement;
  let plotWrapper;
  let thisSelection = vg.Selection.single();
  let uuid = getUUID();
  let colCount: number;
  $: saveSelectionToCache(thisSelection, columnName);

  $: remainingRows = colCount - limit;

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
    selection: any,
    colorColName?: string,
  ) {
    // TODO -- I think this is uncessary and perhaps not even working?
    colCount = await databaseConnection.getColCount(
      mainDatasetName,
      columnName,
    );

    const plotDirectives = [
      vg.barX(vg.from(table, { filterBy: $mosaicSelection }), {
        x: vg.count(),
        y: col,
        fill: colorColName ?? "steelblue",
        sort: { y: "-x", limit },
      }),
      vg.highlight({ by: selection }),
      vg.toggleY({ as: selection }),
      vg.toggleY({ as: $mosaicSelection }),
      vg.text(vg.from(table, { filterBy: $mosaicSelection }), {
        x: 0,
        y: col,
        sort: { y: "-x", limit },
        text: vg.count(),
        dx: -3,
        textAnchor: "end",
        textOverflow: "ellipsis",
        fill: "black",
      }),
      vg.margins({ left: 250, bottom: 0, top: 0, right: 0 }),
      vg.width(400),
      vg.axis(null),
      vg.axisY({
        textOverflow: "ellipsis",
        lineWidth: 15,
        label: null,
        textAnchor: "start",
        dx: -220,
        fontSize: 14,
        tickSize: 0,
      }),
    ];

    if (showBackground) {
      plotDirectives.unshift(
        vg.barX(vg.from(table), {
          x: vg.count(),
          y: col,
          fill: "#ccc",
          fillOpacity: 0.4,
          sort: { y: "-x", limit },
        }),
      );
    }

    plotWrapper = getPlot(...plotDirectives);
    el.replaceChildren(plotWrapper.element);
  }

  afterUpdate(() => {
    renderChart(mainDatasetName, columnName, thisSelection, colorColName);
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

<div class="max-h-96 overflow-auto">
  <div bind:this={el} />
</div>
<div class="mt-1 flex justify-center gap-1">
  {#if remainingRows > 0}
    <button
      class="hover:bg-gray-100 text-gray-500 text-xs px-2 py-1 rounded"
      on:click={() => {
        limit += 10;
      }}
    >
      <!-- +{formatInt(remainingRows)} values. Click to load more. -->
      Load more
    </button>
  {/if}

  {#if limit != 10}
    <button
      class="hover:bg-gray-100 text-gray-500 text-xs px-2 py-1 rounded"
      on:click={() => {
        limit = 10;
      }}
    >
      Reset
    </button>
  {/if}
</div>
