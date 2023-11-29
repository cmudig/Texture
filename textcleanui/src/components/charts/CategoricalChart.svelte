<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate } from "svelte";
  import { filters, showBackgroundDist } from "../../stores";

  export let columnName: string;

  let el: HTMLElement;

  /* BUG: on component destory, the brush is not  preserved rn. 
  Right now still filters chart but cannot change when new component created
  Either need to (1) reset brush on destory (suboptimal) or 
  (2) preserve brush by binding to parent where toggle happens or smth
  */
  const selectCat = vg.Selection.single();

  function renderChart() {
    let c;

    if ($showBackgroundDist) {
      c = vg.plot(
        // including this breaks the click interation and doesnt cut off text?
        // vg.axisY({
        //   textOverflow: "ellipsis",
        //   lineWidth: 50,
        // }),
        vg.barX(vg.from($filters.datasetName), {
          x: vg.count(),
          y: columnName,
          order: columnName,
          fill: "#ccc",
          fillOpacity: 0.4,
          sort: { y: "-x", limit: 10 },
        }),
        vg.barX(vg.from($filters.datasetName, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: columnName,
          order: columnName,
          fill: "steelblue",
          sort: { y: "-x", limit: 10 },
        }),
        vg.highlight({ by: selectCat }),
        vg.toggleY({ as: selectCat }),
        vg.toggleY({ as: $filters.brush }),
        vg.text(vg.from($filters.datasetName, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: columnName,
          order: columnName,
          sort: { y: "-x", limit: 10 },
          text: vg.count(),
          dx: 5,
          textAnchor: "start",
        }),
        vg.yLabel(null),
        vg.marginLeft(80),
        vg.width(400)
      );
    } else {
      c = vg.plot(
        vg.barX(vg.from($filters.datasetName, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: columnName,
          order: columnName,
          fill: "steelblue",
          sort: { y: "-x", limit: 10 },
        }),
        vg.highlight({ by: selectCat }),
        vg.toggleY({ as: selectCat }),
        vg.toggleY({ as: $filters.brush }),
        vg.text(vg.from($filters.datasetName, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: columnName,
          order: columnName,
          sort: { y: "-x", limit: 10 },
          text: vg.count(),
          dx: 5,
          textAnchor: "start",
        }),
        vg.yLabel(null),
        vg.marginLeft(80),
        vg.width(400)
      );
    }

    el.replaceChildren(c);
  }

  afterUpdate(renderChart);
</script>

<div class="summaryChart" bind:this={el} />
