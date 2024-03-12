<script lang="ts">
  import { Select, Input } from "flowbite-svelte";
  import type { TaskFormat } from "../../backendapi";

  export let responseFormat: TaskFormat;
  export let disabled: boolean = false;
</script>

<div class="flex gap-2 items-center">
  Schema
  <Input
    class="w-48"
    placeholder="New column name"
    {disabled}
    bind:value={responseFormat.name}
  />
  <Select
    class="w-48"
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
    bind:value={responseFormat.type}
  />
  <Select
    class="w-48"
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
    bind:value={responseFormat.num_replies}
  />
</div>
