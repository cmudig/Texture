<script lang="ts">
  import type { DatasetInfo } from "../shared/types";
  import * as vg from "@uwdata/vgplot";
  import { onMount } from "svelte";

  export let datasetInfo: DatasetInfo;
  export let brush: any;

  let el: HTMLElement;

  function renderChart() {
    vg.table({
      element: el,
      from: datasetInfo.name,
      height: 1200,
      width: "100%",
      filterBy: brush,
      // TODO in the future, add toggle to render datasetInfo.metadata.other_columns as well
      columns: datasetInfo.metadata.text_columns,
    });
  }

  onMount(renderChart);
</script>

<div class="border-2 border-slate-50">
  <div bind:this={el} />
</div>
