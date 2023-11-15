<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate } from "svelte";
  import { brush } from "../../stores";

  export let datasetName: string;
  export let columnName: string;

  let el: HTMLElement;

  //   let query = `SELECT "${columnName}", count("${columnName}") as count from "${datasetName}" group by "${columnName}" order by count desc limit 10;`;

  const click = vg.Selection.single();

  function renderChart() {
    let c = vg.plot(
      vg.barX(vg.from(datasetName), {
        x: vg.count(),
        y: columnName,
        fill: "#ccc",
        fillOpacity: 0.2,
        sort: { y: "-x" },
      }),
      vg.barX(vg.from(datasetName, { filterBy: $brush }), {
        x: vg.count(),
        y: columnName,
        fill: "steelblue",
        sort: { y: "-x" },
      }),
      vg.toggleY({ as: click }),
      vg.highlight({ by: click }),
      vg.xDomain(vg.Fixed),
      vg.yLabel(null),
      vg.width(400)
      // vg.yDomain(domain),
      // vg.colorDomain(domain),
      // vg.colorRange(colors),
    );

    el.replaceChildren(c);
  }

  afterUpdate(renderChart);
</script>

<div bind:this={el} />
