<script lang="ts">
  import FilterDisplay from "./FilterDisplay.svelte";
  import { selectionDisplay } from "../stores";
</script>

<div class="flex gap-2 flex-wrap">
  {#if Object.keys($selectionDisplay).length === 0}
    <div class="italic">No filters applied</div>
  {:else}
    {#each Object.keys($selectionDisplay) as k}
      <FilterDisplay colName={k} filterRange={$selectionDisplay[k]} />
    {/each}
  {/if}
</div>
