<script lang="ts">
  import { getUUID } from "../shared/utils";
  import { Tooltip } from "flowbite-svelte";
  import { formatValue } from "../shared/format";

  export let cardinality: number;

  let id = getUUID(); // should be unique for each instance
</script>

<div id="cardinality-display-{id}" class="font-mono text-xs text-gray-400">
  |{formatValue(cardinality, { type: "number" })}|
</div>
<Tooltip
  class="z-10"
  triggeredBy="#cardinality-display-{id}"
  type="dark"
  placement="bottom"
>
  {formatValue(cardinality, { type: "number" })} distinct values
</Tooltip>
