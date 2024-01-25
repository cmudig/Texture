<script lang="ts">
  import type { SelectionRange } from "../shared/types";
  import { formatFloat } from "../shared/format";

  export let colName: string;
  export let filterRange: SelectionRange;

  $: isString = typeof filterRange[0] === "string";

  // number is blue-500
  // string is orange-500
</script>

<div
  class="flex flex-col items-center rounded border-2 p-1 {isString
    ? 'bg-orange-200'
    : 'bg-blue-200'}"
>
  <span
    class="w-full overflow-hidden text-ellipsis whitespace-nowrap text-center"
    >{colName}</span
  >
  <div class="w-full text-center font-light">
    {#if isString}
      {filterRange.join(", ")}
    {:else}
      [{formatFloat(Number(filterRange[0]))}, {formatFloat(
        Number(filterRange[1]),
      )}]
    {/if}
  </div>
</div>
