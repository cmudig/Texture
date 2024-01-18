<script lang="ts">
  import { Listgroup, ListgroupItem, Select } from "flowbite-svelte";
  import DataTypeIcon from "../DataTypeIcon.svelte";

  import type { DatasetInfo } from "../../backendapi";
  import { Column } from "../../backendapi";
  export let schema: DatasetInfo;

  $: all_columns = [
    { value: undefined, name: "Not derived" },
    ...schema.column_info
      .filter((c) => c.type === "text")
      .map((col) => ({ value: col.name, name: col.name })),
  ];
</script>

<!-- Schema editor -->
<div class="flex flex-col gap-1">
  <Listgroup active class="">
    <p class="m-4">
      <span>Dataset name:</span>
      <span class="text-black bold">{schema.name}</span>
    </p>
    {#each schema.column_info as col}
      <ListgroupItem class="text-base font-semibold gap-2">
        <DataTypeIcon type={col.type} />

        <span class="text-black bold">{col.name}</span>

        <div class="grow" />

        <Select
          class="w-32"
          placeholder="Select type..."
          size="sm"
          items={Object.values(Column.type).map((v) => ({ value: v, name: v }))}
          bind:value={col.type}
        />

        {#if col.type !== "text"}
          <Select
            class="w-32"
            placeholder="Derived from..."
            size="sm"
            items={all_columns.filter((c) => c.value !== col.name)}
            bind:value={col.associated_text_col_name}
          />
        {:else}
          <div class="w-32" />
        {/if}
      </ListgroupItem>
    {/each}
  </Listgroup>
</div>
