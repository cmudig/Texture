<script lang="ts">
  import type { SelectionRange } from "../shared/types";
  import { formatNumber } from "../shared/formatters";

  export let colName: string;
  export let filterRange: SelectionRange;

  $: isString = typeof filterRange[0] === "string";

  // number is blue-500
  // string is orange-500
</script>

<div
  class="flex flex-col border-2 rounded p-1 items-center {isString
    ? 'bg-orange-200'
    : 'bg-blue-200'}"
>
  <span
    class="w-full text-center text-ellipsis overflow-hidden whitespace-nowrap"
    >{colName}</span
  >
  <div class="w-full text-center font-light">
    {#if isString}
      {filterRange.join(", ")}
    {:else}
      [{formatNumber(Number(filterRange[0]))}, {formatNumber(
        Number(filterRange[1])
      )}]
    {/if}
  </div>
</div>
