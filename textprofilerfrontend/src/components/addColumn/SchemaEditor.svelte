<script lang="ts">
  import { Select, Input } from "flowbite-svelte";
  import type { TaskFormat } from "../../backendapi";

  export let responseSchema: TaskFormat;
  export let disabled: boolean = false;
</script>

<div class="flex gap-2 items-center">
  <Input
    class="w-48 bg-white"
    placeholder="New column name"
    {disabled}
    bind:value={responseSchema.name}
  />
  <Select
    class="w-48 bg-white"
    {disabled}
    items={[
      {
        value: "bool",
        name: "bool",
      },
      {
        value: "number",
        name: "number",
      },
      {
        value: "string",
        name: "string",
      },
    ]}
    placeholder="Response type..."
    bind:value={responseSchema.type}
  />
  <Select
    class="w-48 bg-white"
    {disabled}
    items={[
      {
        value: "single",
        name: "single",
      },
      {
        value: "multiple",
        name: "multiple",
      },
    ]}
    placeholder="Number responses..."
    bind:value={responseSchema.num_replies}
  />
</div>
