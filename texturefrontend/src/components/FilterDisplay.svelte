<script lang="ts">
  import type { SelectionRange } from "../shared/types";
  import { CloseSolid } from "flowbite-svelte-icons";
  import { deleteFilters } from "../stores";
  import { formatValue } from "../shared/format";
  import { isBoolArray, isStringArray } from "../shared/types";

  export let colName: string;
  export let filterRange: SelectionRange;

  // number is blue-500
  // string is orange-500
</script>

<div
  class={`flex gap-1 items-center  bg-white rounded-lg border-2 p-1 border-highlight-500`}
>
  <div>
    {#if isStringArray(filterRange) || isBoolArray(filterRange) || filterRange[0] == undefined}
      <span class="font-semibold text-gray-800">{colName}</span>
      <span> == </span>
      <span class="italic">
        {filterRange
          .map((item) =>
            typeof item === "string"
              ? `"${item.replaceAll("''", "'")}"`
              : `${item}`,
          )
          .join(", ")}
      </span>
    {:else}
      <span
        >{formatValue(filterRange[0], {
          range: filterRange[1] - filterRange[0],
          colName,
        })}
        {"<="}
      </span>
      <span class="font-semibold text-gray-800">{colName}</span>

      <span
        >{"<="}
        {formatValue(filterRange[1], {
          range: filterRange[1] - filterRange[0],
          colName,
        })}</span
      >
    {/if}
  </div>
  <button
    class="bg-gray-300 hover:bg-primary-500 hover:text-white p-2 rounded-full ml-1"
    on:click={() => deleteFilters(colName)}
  >
    <CloseSolid class="h-2 w-2" />
  </button>
</div>
