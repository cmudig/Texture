<script lang="ts">
  import { TrashBinOutline } from "flowbite-svelte-icons";
  import { Spinner, Textarea } from "flowbite-svelte";
  import TextPlaceholder from "../utils/TextPlaceholder.svelte";
  import { QueryStatus } from "../../shared/types";
  import type { TaskFormat } from "../../backendapi";

  export let idColName: string | undefined;
  export let targetColName: string;
  export let responseSchema: TaskFormat;
  export let columnData: any[];
  export let resultData: any[];
  export let queryStatus: QueryStatus;
  export let deleteResult: ((index: number) => void) | undefined = undefined;
  export let allowEdits = true;
</script>

<div>
  <div class="flex w-full font-semibold">
    <div
      class="w-12 shrink-0 whitespace-normal break-words p-2 bg-gray-50 border-l border-y border-gray-200"
    >
      {idColName ?? ""}
    </div>
    <div
      class="w-1/2 shrink-0 whitespace-normal break-words p-2 bg-gray-50 border-l border-y border-gray-200"
    >
      {targetColName}
    </div>
    <div
      class="grow whitespace-normal break-words p-2 border-l border-y border-gray-200 text-black bg-gray-50"
    >
      {#if responseSchema}
        {`${responseSchema.name} (${responseSchema?.type}${responseSchema.num_replies === "single" ? "" : "[]"})`}
      {:else}
        <Spinner />
      {/if}
    </div>
    <div class="w-8 shrink-0 border-l border-gray-200" />
  </div>

  {#each columnData as cd, index}
    <div class="flex w-full">
      <div
        class="w-12 text-sm shrink-0 whitespace-normal break-words align-top p-2 overflow-auto border-b border-l border-gray-200 bg-white"
      >
        {idColName ? cd[idColName] : ""}
      </div>
      <div
        class="w-1/2 shrink-0 whitespace-normal break-words align-top p-2 overflow-auto max-h-32 border-b border-l border-gray-200 bg-white"
      >
        {cd[targetColName]}
      </div>
      <div
        class="grow whitespace-normal break-words border-l border-b border-gray-200 bg-green-50 text-black align-top p-2 overflow-auto max-h-32"
      >
        {#if queryStatus === QueryStatus.COMPLETED}
          {#if allowEdits}
            <Textarea
              rows="3"
              bind:value={resultData[index]}
              class="bg-white/50"
            />
          {:else}
            <div>
              {responseSchema.num_replies === "multiple"
                ? "[" + resultData[index] + "]"
                : resultData[index]}
            </div>
          {/if}
        {:else}
          <TextPlaceholder />
        {/if}
      </div>

      <div class="w-8 shrink-0 border-l border-gray-200">
        {#if deleteResult}
          <button
            class="hover:bg-gray-100 text-gray-500 p-1 rounded m-1"
            on:click={() => {
              // redundant check cuz typescript gets mad
              if (deleteResult) deleteResult(index);
            }}
          >
            <TrashBinOutline size="sm" />
          </button>
        {/if}
      </div>
    </div>
  {/each}
</div>
