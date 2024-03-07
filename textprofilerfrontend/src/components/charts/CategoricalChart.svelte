<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate, onDestroy } from "svelte";
  import {
    mosaicSelection,
    clearColumnSelections,
    derivedViewNames,
  } from "../../stores";
  import { getDatasetName, getUUID, getCacheKey } from "../../shared/utils";
  import { getPlot, getColCountStore } from "./chartUtils";
  import { formatInt } from "../../shared/format";

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
  $: saveSelectionToCache(thisSelection, columnName);

  $: plotTableNamePromise = calculateDatasetName(
    mainDatasetName,
    columnName,
    plotNulls,
    excludeList,
    isDerivedTable,
  );

  $: colCountStore = getColCountStore(
    plotTableNamePromise,
    columnName,
    showBackground,
    mosaicSelection,
  );

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

  async function calculateDatasetName(
    _mainDatasetName,
    _colName,
    _plotNulls,
    _excludeList,
    _isDerived,
  ): Promise<string> {
    let datasetName = await getDatasetName(
      _mainDatasetName,
      _colName,
      _plotNulls,
      _excludeList,
    );

    if (_isDerived) {
      $derivedViewNames.set(
        getCacheKey({ table: _mainDatasetName, col: _colName }),
        datasetName,
      );
    }

    return datasetName;
  }

  async function renderChart(
    pltNamePromise: Promise<string>,
    cName: string,
    _showBackground: boolean,
    selection: any,
  ) {
    let _tableName: string = await pltNamePromise;
    // console.log("rendering cat chart for ", { table: _tableName, cName });

    if (_showBackground) {
      return getPlot(
        // including this breaks the click interation and doesnt cut off text?
        // vg.axisY({
        //   textOverflow: "ellipsis",
        //   lineWidth: 50,
        // }),
        vg.barX(vg.from(_tableName), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: "#ccc",
          fillOpacity: 0.4,
          sort: { y: "-x", limit },
        }),
        vg.barX(vg.from(_tableName, { filterBy: $mosaicSelection }), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: "steelblue",
          sort: { y: "-x", limit },
        }),
        vg.highlight({ by: selection }),
        vg.toggleY({ as: selection }),
        vg.toggleY({ as: $mosaicSelection }),
        vg.text(vg.from(_tableName, { filterBy: $mosaicSelection }), {
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
    return getPlot(
      vg.barX(vg.from(_tableName, { filterBy: $mosaicSelection }), {
        x: vg.count(),
        y: cName,
        order: cName,
        fill: "steelblue",
        sort: { y: "-x", limit },
      }),
      vg.highlight({ by: selection }),
      vg.toggleY({ as: selection }),
      vg.toggleY({ as: $mosaicSelection }),
      vg.text(vg.from(_tableName, { filterBy: $mosaicSelection }), {
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

  afterUpdate(async () => {
    plotWrapper = await renderChart(
      plotTableNamePromise,
      columnName,
      showBackground,
      thisSelection,
    );
    el.replaceChildren(plotWrapper.element);
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
  {#if $colCountStore - limit > 0}
    <button
      class="hover:bg-gray-100 text-gray-500 text-xs px-2 py-1 rounded"
      on:click={() => {
        limit += 10;
      }}
    >
      +{formatInt($colCountStore - limit)} values. Click to load more.
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
