<script lang="ts">
  import type { SelectionRange } from "../shared/types";
  import { formatFloat } from "../shared/format";
  import { CloseSolid } from "flowbite-svelte-icons";

  export let colName: string;
  export let filterRange: SelectionRange;

  $: isString = typeof filterRange[0] === "string";

  // number is blue-500
  // string is orange-500
</script>

<div
  class={`flex gap-1 items-center  bg-white rounded-lg border-2 p-1  ${isString ? "border-orange-300 " : "border-blue-300"}`}
>
  <div>
    {#if isString}
      <span class="font-semibold text-gray-800">{colName}</span>
      <span> == </span>
      <span class="italic">
        {filterRange.map((item) => `"${item}"`).join(", ")}
      </span>
    {:else}
      <span>{formatFloat(Number(filterRange[0]))} {"<="} </span>
      <span class="font-semibold text-gray-800">{colName}</span>

      <span>{"<="} {formatFloat(Number(filterRange[1]))}</span>
    {/if}
  </div>
  <button
    class="bg-gray-300 hover:bg-primary-500 hover:text-white p-2 rounded-full ml-1"
  >
    <CloseSolid class="h-2 w-2" />
  </button>
</div>
