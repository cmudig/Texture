<script lang="ts">
  import { afterUpdate } from "svelte";
  import type { DatasetInfo, TableOption } from "../shared/types";
  import * as vg from "@uwdata/vgplot";
  import { brush } from "../stores";

  export let datasetInfo: DatasetInfo;
  export let tableOption: TableOption = "text";

  let el: HTMLElement;
  let plot_cols: string[];

  function getPlotColumns(
    option: "all" | "text",
    dsInfo: DatasetInfo
  ): string[] {
    let text_col_names: string[] = dsInfo.metadata.text_columns.map(
      (c) => c.name
    );

    if (option === "all") {
      let other_cols = dsInfo.metadata.other_columns.map((c) => c.name);
      return text_col_names.concat(other_cols);
    }

    return text_col_names;
  }

  function renderChart(cols: string[]) {
    console.log("[Render] Instance view");
    let c = vg.table({
      // element: el, // doesnt work on updates?
      from: datasetInfo.name,
      height: 1200,
      width: "100%",
      filterBy: $brush,
      columns: cols,
    });

    if (el) {
      el.replaceChildren(c);
    }
  }

  $: {
    plot_cols = getPlotColumns(tableOption, datasetInfo);
  }

  afterUpdate(() => {
    // have to manually call after update to make sure element is rendered and plot_cols is updated
    renderChart(plot_cols);
  });
</script>

<div id="instanceTable" class="border-2 border-slate-50">
  <div bind:this={el} />
</div>
