<script lang="ts">
  import type { Column } from "../../shared/types";
  import CategoricalChart from "../charts/CategoricalChart.svelte";
  import { Select } from "flowbite-svelte";

  export let text_column: Column;
  export let cluster_columns: Column[];

  $: col_options = cluster_columns?.map((col) => ({
    value: col.name,
    name: col.name,
  }));
  let selectedClusterCol: string = cluster_columns?.[0]?.name;

  // $: col_options = cluster_columns?.map((col) => col.name);
</script>

<div class="flex flex-col gap-1">
  <p>Exact Duplicates</p>
  <div class="pl-4">
    <CategoricalChart columnName={text_column.name} />
  </div>
</div>

{#if cluster_columns}
  <div class="flex flex-col gap-1">
    <p>Near Duplicates</p>

    <div class="pl-4">
      <div class="max-w-xs">
        <Select
          size="sm"
          items={col_options}
          placeholder="Select clustering"
          bind:value={selectedClusterCol}
        />
      </div>

      <CategoricalChart columnName={selectedClusterCol} plotNulls={false} />

      <!-- {#each col_options as colName}
        <p>{colName}</p>
        <CategoricalChart columnName={colName} plotNulls={false} />
      {/each} -->
    </div>
  </div>
{/if}
