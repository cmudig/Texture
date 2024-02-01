<script lang="ts">
  import { AngleRightOutline, AngleDownOutline } from "flowbite-svelte-icons";
  export let id: number;
  export let document: string;
  export let docName: string;
  export let metadata: Array<[string, unknown]>;
  export let highlight = false;

  let toggle = false;
</script>

<div
  class={`rounded border bg-white ${highlight ? "border-dashed border-primary-500" : "border-solid border-gray-300"}`}
>
  <div class="flex items-center border-b border-gray-300 p-2 gap-1">
    <button
      class="bg-gray-50 hover:bg-gray-100 text-gray-500 p-1 rounded"
      on:click={() => (toggle = !toggle)}
    >
      {#if toggle}
        <AngleDownOutline size="xs" />
      {:else}
        <AngleRightOutline size="xs" />
      {/if}
    </button>
    <div>{docName}</div>
    <div class="grow"></div>
    <div class="text-gray-500">{id}</div>
  </div>

  <div class={`flex  ${toggle ? "max-h-none " : "max-h-48 "}`}>
    <div class={` overflow-auto grow p-2 text-gray-800`}>
      {document}
    </div>

    {#if metadata.length}
      <div class="overflow-auto shrink bg-gray-50 min-w-80">
        {#each metadata as [itemKey, itemValue] (itemKey)}
          <div class="flex border-b border-gray-200 px-2">
            <div
              class="whitespace-normal text-ellipsis overflow-hidden text-sm w-1/2 font-semibold italic"
              title={itemKey}
            >
              {itemKey}
            </div>
            <div class="whitespace-normal overflow-scroll text-sm w-1/2">
              {itemValue}
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>
