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
  <div class="flex items-center border-b border-gray-300 p-2">
    <div>{docName}</div>
    <div class="grow"></div>
    <div class="text-gray-500">{id}</div>
  </div>

  <div class="flex">
    <!-- tool bar -->
    <div class="flex flex-col gap-1 pt-2 pl-2">
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
    </div>
    <div
      class={`overflow-auto p-2 w-full text-gray-800 ${toggle ? "max-h-96 " : "max-h-48 "}`}
    >
      {document}
    </div>

    {#if metadata.length}
      <div class="bg-gray-50 p-2 min-w-48">
        <table class="table-fixed">
          <tbody>
            {#each metadata as [itemKey, itemValue] (itemKey)}
              <tr>
                <td class="font-semibold italic">{itemKey}</td>
                <td>{itemValue}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</div>
