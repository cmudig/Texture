<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate } from "svelte";
  import { filters } from "../../stores";
  import type { JoinInfo } from "../../backendapi";
  import { getDatasetName } from "../../shared/utils";

  export let columnName: string;
  export let mainDatasetName: string;
  export let joinDatasetInfo: JoinInfo | undefined = undefined;
  export let showBackground = true;
  export let plotNulls = false;

  let el: HTMLElement;

  async function renderChart(
    mainDsName: string,
    cName: string,
    pltNullsFlag: boolean,
    joinDsInfo?: JoinInfo
  ) {
    let c;

    let datasetName = await getDatasetName(mainDsName, cName, pltNullsFlag);

    let fromClause: any = datasetName;

    if (joinDsInfo) {
      fromClause = vg.fromJoinDistinct({
        table: datasetName,
        rightTable: joinDsInfo.joinDatasetName,
        joinKey: joinDsInfo.joinKey,
      });
    }

    if (showBackground) {
      c = vg.plot(
        vg.rectY(vg.from(fromClause), {
          x: vg.bin(columnName),
          y: vg.count(),
          fill: "#ccc",
          fillOpacity: 0.4,
          inset: 0.5,
        }),
        vg.rectY(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: vg.bin(columnName),
          y: vg.count(),
          fill: "steelblue",
          inset: 0.5,
        }),
        vg.intervalX({ as: $filters.brush }),
        vg.xDomain(vg.Fixed),
        vg.marginLeft(55),
        vg.width(400),
        vg.height(150)
      );
    } else {
      c = vg.plot(
        vg.rectY(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: vg.bin(columnName),
          y: vg.count(),
          fill: "steelblue",
          inset: 0.5,
        }),
        vg.intervalX({ as: $filters.brush }),
        vg.xDomain(vg.Fixed),
        vg.marginLeft(55),
        vg.width(400),
        vg.height(150)
      );
    }

    el.replaceChildren(c);
  }

  // This re-renders unnecessarily but is required or else will not re-render on $brush updates
  afterUpdate(() =>
    renderChart(mainDatasetName, columnName, plotNulls, joinDatasetInfo)
  );
</script>

<div bind:this={el} />
