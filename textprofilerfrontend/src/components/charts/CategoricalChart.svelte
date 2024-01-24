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
  export let plotNulls = true;
  export let limit = 10;

  let el: HTMLElement;

  /* BUG: on component destory, the brush is not  preserved rn. 
  Right now still filters chart but cannot change when new component created
  Either need to (1) reset brush on destory (suboptimal) or 
  (2) preserve brush by binding to parent where toggle happens or smth
  */

  async function renderChart(
    mainDsName: string,
    cName: string,
    pltNullsFlag: boolean,
    joinDsInfo?: JoinInfo,
  ) {
    let c;

    const selectCat = vg.Selection.single();

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
        vg.barX(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: "steelblue",
          sort: { y: "-x", limit },
        }),
        vg.highlight({ by: selectCat }),
        vg.toggleY({ as: selectCat }),
        vg.toggleY({ as: $filters.brush }),
        vg.text(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: cName,
          order: cName,
          sort: { y: "-x", limit },
          text: vg.count(),
          dx: 5,
          textAnchor: "start",
        }),
        vg.yLabel(null),
        vg.marginLeft(80),
        vg.width(400),
      );
    } else {
      c = vg.plot(
        vg.barX(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: cName,
          order: cName,
          fill: "steelblue",
          sort: { y: "-x", limit },
        }),
        vg.highlight({ by: selectCat }),
        vg.toggleY({ as: selectCat }),
        vg.toggleY({ as: $filters.brush }),
        vg.text(vg.from(fromClause, { filterBy: $filters.brush }), {
          x: vg.count(),
          y: cName,
          order: cName,
          sort: { y: "-x", limit },
          text: vg.count(),
          dx: 5,
          textAnchor: "start",
        }),
        vg.yLabel(null),
        vg.marginLeft(80),
        vg.width(400),
      );
    }

    el.replaceChildren(c);
  }

  afterUpdate(() => {
    renderChart(mainDatasetName, columnName, plotNulls, joinDatasetInfo);
  });
</script>

<div class="summaryChart" bind:this={el} />
