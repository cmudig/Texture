<script lang="ts">
  import type { Column } from "../backendapi/models/Column";
  import { Tooltip } from "flowbite-svelte";
  import { getUUID } from "../shared/utils";

  export let type: Column.type;
  export let id: string;

  $: if (!id) id = getUUID();

  function getIcon(type: Column.type) {
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
</script>

<p id="data-icon-{id}" class="font-serif font-medium text-gray-500">
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
