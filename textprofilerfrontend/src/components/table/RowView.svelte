<script lang="ts">
  import { AngleRightOutline, AngleDownOutline } from "flowbite-svelte-icons";
  import { formatValue } from "../../shared/format";
  import { type SelectionMap, isStringArray } from "../../shared/types";
  import Highlight from "./Highlight.svelte";
  import Regular from "./Regular.svelte";
  import type { JoinInfo } from "../../backendapi";
  import { filters, selectionDisplay } from "../../stores";

  export let id: number;
  export let textData: Array<[string, unknown]>;
  export let metadata: Array<[string, unknown]>;
  export let highlight = false;

  function renderValue(
    value: any,
    colName: string,
    selections: SelectionMap,
    joinInfo?: JoinInfo,
  ) {
    let highlights: string[] = [];

    if (
      joinInfo?.joinColumn.associated_text_col_name === colName &&
      joinInfo?.joinColumn.name in selections &&
      isStringArray(selections[joinInfo.joinColumn.name])
    ) {
      highlights = [
        ...highlights,
        ...(selections[joinInfo.joinColumn.name] as string[]),
      ];
    }
    if (colName in selections && isStringArray(selections[colName])) {
      highlights = [...highlights, ...(selections[colName] as string[])];
    }

    if (highlights.length) {
      return {
        component: Highlight,
        props: {
          value: value,
          highlights,
        },
      };
    }

    return {
      component: Regular,
      props: { value: formatValue(value) },
    };
  }

  let toggle = false;
</script>

<div
  class={`rounded border bg-white ${highlight ? "border-dashed border-primary-500" : "border-solid border-gray-300"}`}
>
  <div class="flex items-center border-b border-gray-300 p-2 gap-1">
    <button
      class="hover:bg-gray-100 text-gray-500 p-1 rounded"
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

  <div
    class={`flex  ${toggle ? "max-h-96 overflow-auto " : "max-h-48 overflow-hidden"}`}
  >
    <div class={`grow px-2 pt-2 pb-4 text-gray-800 flex flex-col gap-1`}>
      {#each textData as [textColName, textColData] (textColName)}
        {@const renderComponent = renderValue(
          textColData,
          textColName,
          $selectionDisplay,
          $filters.joinDatasetInfo,
        )}
        <div>
          <div class="border-b border-gray-300 italic">{textColName}</div>

          <div>
            <svelte:component
              this={renderComponent.component}
              {...renderComponent.props}
            />
          </div>
        </div>
      {/each}
    </div>

    {#if metadata.length}
      <div class="shrink bg-gray-50 min-w-80 h-full">
        {#each metadata as [itemKey, itemValue] (itemKey)}
          {@const renderComponent = renderValue(
            itemValue,
            itemKey,
            $selectionDisplay,
            $filters.joinDatasetInfo,
          )}
          <div class="flex border-b border-gray-200 px-2">
            <div
              class="whitespace-normal text-ellipsis overflow-hidden text-sm w-1/3 font-semibold italic"
              title={itemKey}
            >
              {itemKey}
            </div>
            <div
              class={`whitespace-normal break-words text-sm w-2/3 ${itemValue == undefined ? "text-gray-300 italic" : "text-gray-800"}`}
            >
              <svelte:component
                this={renderComponent.component}
                {...renderComponent.props}
              />
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>
