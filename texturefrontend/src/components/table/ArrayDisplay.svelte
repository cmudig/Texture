<script lang="ts">
  import type { Column } from "../../backendapi";
  import { formatValue } from "../../shared/format";
  import type { SelectionRange } from "../../shared/types";
  import { shouldHighlight } from "../../shared/utils";

  export let name: string;
  export let type: Column.type;
  export let data: { [key: string]: any }[] | undefined;
  export let highlights: undefined | SelectionRange = undefined;
</script>

{#if data}
  <div class="flex gap-1 flex-wrap">
    {#each data as item}
      <div
        class="px-1 bg-gray-100 rounded"
        class:bg-highlight-100={highlights != undefined &&
          shouldHighlight(item[name], highlights, type)}
      >
        {formatValue(item[name], { type })}
      </div>
    {/each}
  </div>
{:else}
  {formatValue(null)}
{/if}
