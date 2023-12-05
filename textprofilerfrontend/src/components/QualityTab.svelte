<script lang="ts">
  import { slide } from "svelte/transition";
  import type { QualityInfo } from "../backendapi/models/QualityInfo";
  import DuplicatesView from "./quality/DuplicatesView.svelte";
  import PIIView from "./quality/PIIView.svelte";

  export let qualityInfo: QualityInfo;

  let active = true;
</script>

<div>
  <button
    class="space-between flex h-9 w-full items-center justify-between gap-2 px-2 hover:bg-gray-100"
    class:bg-gray-50={active}
    on:click={() => {
      active = !active;
    }}
  >
    <p
      class:font-medium={active}
      class="max-w-sm overflow-hidden text-ellipsis text-left"
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
        {:else if qualityInfo.type === "pii"}
          <PIIView pii_col={qualityInfo.plot_columns?.[0]} />
        {:else}
          <p>Unkown quality type!</p>
        {/if}
      </div>
    {/if}
  </div>
</div>
