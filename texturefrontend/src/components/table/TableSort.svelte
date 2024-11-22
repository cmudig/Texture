<script lang="ts">
  import { ArrowUpSolid, ArrowDownSolid } from "flowbite-svelte-icons";
  import { Select } from "flowbite-svelte";
  import {
    tableSortColStore,
    tableSortDescStore,
    tableSchemaStore,
  } from "../../stores";

  $: sortColumn = $tableSortColStore;
  $: sortDesc = $tableSortDescStore;
  $: schema = $tableSchemaStore;
</script>

{#if sortColumn != undefined && sortDesc != undefined && schema != undefined}
  <div class="flex gap-1 items-center">
    <Select
      class="max-w-40"
      size="sm"
      items={[
        ...$schema.map((colInfo) => ({
          value: colInfo.column,
          name: colInfo.column,
        })),
      ]}
      bind:value={$sortColumn}
      placeholder="Sort by..."
    />

    <button
      class={`hover:bg-gray-200 text-gray-500 p-1 rounded ${
        !$sortColumn && "cursor-not-allowed !text-gray-300"
      }`}
      on:click={() => ($sortDesc = !$sortDesc)}
      title={"Toggle sort order"}
      disabled={!$sortColumn}
    >
      {#if $sortDesc}
        <ArrowDownSolid size="xs" />
      {:else}
        <ArrowUpSolid size="xs" />
      {/if}
    </button>
  </div>
{/if}
