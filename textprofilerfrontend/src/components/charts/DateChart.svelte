<script lang="ts">
  import * as vg from "@uwdata/vgplot";
  import { afterUpdate } from "svelte";
  import { filters } from "../../stores";
  import type { JoinInfo } from "../../backendapi";

  export let columnName: string;
  export let mainDatasetName: string;
  export let joinDatasetInfo: JoinInfo | undefined = undefined;

  let el: HTMLElement;

  // FUTURE: if vg.bin() works for dates might be nice here so less crowded line...
  function renderChart(
    datasetName: string,
    cName: string,
    joinDsInfo?: JoinInfo
  ) {
    let fromClause: any = datasetName;

    if (joinDsInfo) {
      fromClause = vg.fromJoinDistinct({
        table: datasetName,
        rightTable: joinDsInfo.joinDatasetName,
        joinKey: joinDsInfo.joinKey,
      });
    }

    let c = vg.plot(
      vg.lineY(vg.from(fromClause, { filterBy: $filters.brush }), {
        x: cName,
        y: vg.count(),
        stroke: "steelblue",
        curve: "monotone-x",
      }),
      vg.intervalX({ as: $filters.brush }),
      vg.xDomain(vg.Fixed),
      vg.marginLeft(55),
      vg.width(400),
      vg.height(150)
    );

    el.replaceChildren(c);
  }

  afterUpdate(() => renderChart(mainDatasetName, columnName, joinDatasetInfo));
</script>

<div bind:this={el} />
