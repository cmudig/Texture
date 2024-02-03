<script lang="ts">
  import { AngleRightOutline, AngleDownOutline } from "flowbite-svelte-icons";
  export let id: number;
  export let textData: Array<[string, unknown]>;
  export let metadata: Array<[string, unknown]>;
  export let highlight = false;

  // console.log("Document display, textData: ", textData);
  // console.log("Document display, metadata: ", metadata);

  // function renderValue(
  //   myValue: any,
  //   schemaItem: FieldInfo,
  //   selections: SelectionMap,
  //   joinInfo?: JoinInfo,
  // ) {
  //   let highlights: string[] = [];

  //   if (
  //     joinInfo?.joinColumn.associated_text_col_name == schemaItem.column &&
  //     joinInfo?.joinColumn.name in selections &&
  //     isStringArray(selections[joinInfo.joinColumn.name])
  //   ) {
  //     highlights = [...highlights, ...selections[joinInfo.joinColumn.name]];
  //   }
  //   if (
  //     schemaItem.column in selections &&
  //     isStringArray(selections[schemaItem.column])
  //   ) {
  //     highlights = [...highlights, ...selections[schemaItem.column]];
  //   }

  //   if (highlights.length) {
  //     return {
  //       component: Highlight,
  //       props: {
  //         value: myValue,
  //         highlights,
  //       },
  //     };
  //   }

  //   return {
  //     component: Regular,
  //     props: { value: formatValue(myValue, { type: schemaItem.type }) },
  //   };
  // }

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
    <slot name="optionButtons" />
    <slot name="title" />

    <div class="grow"></div>
    <div class="text-gray-500">{id}</div>
  </div>

  <div class={`flex  ${toggle ? "max-h-none " : "max-h-48 "}`}>
    <div class={` overflow-auto grow p-2 text-gray-800 flex flex-col gap-1`}>
      {#each textData as [textColName, textColData] (textColName)}
        <div>
          <div class="border-b border-gray-300 italic">{textColName}</div>

          <div>{textColData}</div>
        </div>
      {/each}
    </div>

    {#if metadata.length}
      <div class="overflow-auto shrink bg-gray-50 min-w-80">
        {#each metadata as [itemKey, itemValue] (itemKey)}
          <div class="flex border-b border-gray-200 px-2">
            <div
              class="whitespace-normal text-ellipsis overflow-hidden text-sm w-1/3 font-semibold italic"
              title={itemKey}
            >
              {itemKey}
            </div>
            <div class="whitespace-normal overflow-scroll text-sm w-2/3">
              {itemValue}
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>
