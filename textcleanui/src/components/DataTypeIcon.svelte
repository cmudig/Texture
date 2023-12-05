<script lang="ts">
  import type { DataType } from "../shared/types";
  import { Tooltip } from "flowbite-svelte";
  import { getUUID } from "../shared/utils";

  export let type: DataType;

  function getIcon(type: DataType) {
    switch (type) {
      case "text":
        return "T";
      case "number":
        return "#";
      case "date":
        return "D";
      case "categorical":
        return "C";
    }
  }

  let id = getUUID();
</script>

<p id="data-icon-{id}" class="font-serif font-medium text-gray-400">
  {getIcon(type)}
</p>

<Tooltip
  type="dark"
  placement="bottom"
  class="z-10"
  triggeredBy="#data-icon-{id}"
>
  {type}
</Tooltip>
