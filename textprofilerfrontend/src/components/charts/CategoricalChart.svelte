<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import {
    mosaicSelection,
    clearColumnSelections,
    derivedViewNames,
    databaseConnection,
  } from "../../stores";
  import { getDatasetName, getUUID, getCacheKey } from "../../shared/utils";
  import { getPlot } from "./chartUtils";

  export let columnName: string;
  export let mainDatasetName: string;
  export let showBackground = true;
  export let plotNulls = true;
  export let limit = 10;
  export let excludeList: string[] | undefined = undefined;
  export let isDerivedTable = false;

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

    if (isDerivedTable) {
      $derivedViewNames.set(
        getCacheKey({ table: mainDsName, col: cName }),
        datasetName,
      );
    }

    colCount = await databaseConnection.getColCount(
      mainDatasetName,
      columnName,
    );

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
        vg.barX(vg.from(fromClause, { filterBy: $mosaicSelection }), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: "steelblue",
          sort: { y: "-x", limit },
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
          dx: -3,
          textAnchor: "end",
          textOverflow: "ellipsis",
          fill: "white",
        }),
        vg.margins({ left: 80, bottom: 0, top: 0, right: 0 }),
        vg.width(400),
        vg.axis(null),
        vg.axisY({ textOverflow: "ellipsis", lineWidth: 7, label: null }),
      );
    } else {
      plotWrapper = getPlot(
        vg.barX(vg.from(fromClause, { filterBy: $mosaicSelection }), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: "steelblue",
          sort: { y: "-x", limit },
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
          dx: -3,
          textAnchor: "end",
          textOverflow: "ellipsis",
          fill: "white",
        }),
        vg.margins({ left: 80, bottom: 0, top: 0, right: 0 }),
        vg.width(400),
        vg.axis(null),
        vg.axisY({ textOverflow: "ellipsis", lineWidth: 7, label: null }),
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
      +{remainingRows} values. Click to load more.
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
