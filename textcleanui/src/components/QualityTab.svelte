<script lang="ts">
  import { slide } from "svelte/transition";
  import type { QualityInfo } from "../shared/types";
  import DuplicatesView from "./quality/DuplicatesView.svelte";

  export let qualityInfo: QualityInfo;

  let active = true;
</script>

<div>
  <button
    class="px-2 flex space-between items-center gap-2 justify-between w-full hover:bg-gray-100 h-9"
    class:bg-gray-50={active}
    on:click={() => {
      active = !active;
    }}
  >
    <p
      class:font-medium={active}
      class="text-left text-ellipsis overflow-hidden max-w-sm"
    >
      {qualityInfo.type}
    </p>

    <div class="grow" />
  </button>
  <div class="w-full">
    {#if active}
      <div transition:slide|local={{ duration: 200 }} class="ml-4 mt-2">
        {#if qualityInfo.type === "duplicates"}
          <DuplicatesView
            text_column={qualityInfo.text_column}
            cluster_columns={qualityInfo.plot_columns ?? []}
          />
        {:else}
          <p>Unkown quality type!</p>
        {/if}
      </div>
    {/if}
  </div>
</div>
