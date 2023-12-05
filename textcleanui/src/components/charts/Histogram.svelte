<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate } from "svelte";
  import { filters, showBackgroundDist } from "../../stores";

  export let columnName: string;
  export let plotNulls = false;

  let el: HTMLElement;

  async function getDatasetName(
    mainDatasetName: string,
    cName: string,
    pltNullsFlag: boolean,
  ) {
    let viewName = `${mainDatasetName}NoNulls${cName}`;

    if (!pltNullsFlag) {
      await vg
        .coordinator()
        .exec(
          vg.sql`create view if not exists ${vg.column(
            viewName,
          )} as select * from ${vg.column(mainDatasetName)} where ${vg.column(
            cName,
          )} is not null;`,
        );

      return viewName;
    }

    return mainDatasetName;
  }

  async function renderChart(
    mainDsName: string,
    cName: string,
    pltNullsFlag: boolean,
  ) {
    let c;

    let datasetName = await getDatasetName(mainDsName, cName, pltNullsFlag);

    if ($showBackgroundDist) {
      c = vg.plot(
        vg.rectY(vg.from(datasetName), {
          x: vg.bin(columnName),
          y: vg.count(),
          fill: "#ccc",
          fillOpacity: 0.4,
          inset: 0.5,
        }),
        vg.rectY(vg.from(datasetName, { filterBy: $filters.brush }), {
          x: vg.bin(columnName),
          y: vg.count(),
          fill: "steelblue",
          inset: 0.5,
        }),
        vg.intervalX({ as: $filters.brush }),
        vg.xDomain(vg.Fixed),
        vg.marginLeft(55),
        vg.width(400),
        vg.height(150),
      );
    } else {
      c = vg.plot(
        vg.rectY(vg.from(datasetName, { filterBy: $filters.brush }), {
          x: vg.bin(columnName),
          y: vg.count(),
          fill: "steelblue",
          inset: 0.5,
        }),
        vg.intervalX({ as: $filters.brush }),
        vg.xDomain(vg.Fixed),
        vg.marginLeft(55),
        vg.width(400),
        vg.height(150),
      );
    }

    el.replaceChildren(c);
  }

  // This re-renders unnecessarily but is required or else will not re-render on $brush updates
  afterUpdate(() => renderChart($filters.datasetName, columnName, plotNulls));
</script>

<div bind:this={el} />
