<script lang="ts">
  import { afterUpdate } from "svelte";
  import type { DatasetInfo, TableOption } from "../shared/types";
  import * as vg from "@uwdata/vgplot";
  import { filters } from "../stores";

  export let datasetInfo: DatasetInfo;
  export let currentColToggleStates: Record<string, boolean> = {};

  let el: HTMLElement;
  let plot_cols: string[];

  function renderChart(cols: string[]) {
    let c;

    if (cols.length > 0) {
      c = vg.table({
        // element: el, // doesnt work on updates?
        from: datasetInfo.name,
        height: 1200,
        width: "100%",
        filterBy: $filters.brush,
        columns: cols,
      });
    } else {
      c = document.createElement("p");
      c.textContent = "Select at least one column to display in table view.";
    }

    if (el) {
      el.replaceChildren(c);
    }
  }

  $: {
    plot_cols = Object.keys(currentColToggleStates).filter(
      (col) => currentColToggleStates[col]
    );
  }

  afterUpdate(() => {
    // have to manually call after update to make sure element is rendered and plot_cols is updated
    renderChart(plot_cols);
  });
</script>

<div id="instanceTable" class="border-2 border-slate-50">
  <div bind:this={el} />
</div>
