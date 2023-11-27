<script lang="ts">
  import { getUUID } from "../shared/utils";
  import NullChart from "./charts/NullChart.svelte";
  import { Tooltip } from "flowbite-svelte";

  export let nullPercentage: number;

  let id = getUUID(); // should be unique for each instance
</script>

<div id="null-display-{id}">
  <NullChart {nullPercentage} />
</div>
<Tooltip
  class="z-10"
  triggeredBy="#null-display-{id}"
  type="dark"
  placement="bottom"
>
  {nullPercentage}% null values
</Tooltip>
