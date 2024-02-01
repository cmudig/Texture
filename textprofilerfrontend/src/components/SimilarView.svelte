<script lang="ts">
  import { getContext } from "svelte";
  import { CloseButton } from "flowbite-svelte";
  import DocumentDisplay from "./DocumentDisplay.svelte";
  import type { DefaultService, DatasetInfo } from "../backendapi";

  export let similarDocID: BigInt;
  export let datasetInfo: DatasetInfo;
  export let clearFunc: () => void;

  let backendService: DefaultService = getContext("backendService");

  function getDocument(id: BigInt) {}
</script>

<div class="flex items-center bg-gray-50 h-10 px-2">
  <h3 class="self-center font-semibold text-lg">Similar View</h3>
  <CloseButton on:click={clearFunc} />
</div>
<div class="max-h-screen overflow-auto">
  <div
    class="p-4 sticky top-0 w-full bg-white border border-dashed border-primary-500"
  >
    <h3 class="font-semibold mb-2">Pinned Document</h3>

    <DocumentDisplay
      id={similarDocID}
      document={"hello world ".repeat(100)}
      docName={"myDocName"}
      metadata={[
        { class: "none" },
        { year: 14474 },
        { other: "heakflsj fsjkl  fajskl ajsfkl" },
      ]}
      highlight={false}
    />
  </div>
  <div class="bg-gray-100 p-4 flex flex-col gap-2">
    {#each [1n, 2n] as item (item)}
      <DocumentDisplay
        id={item}
        document={"hello world ".repeat(Number(item) * 100)}
        docName={"myDocName"}
        metadata={[
          { class: "none" },
          { year: 14474 },
          { other: "heakflsj fsjkl  fajskl ajsfkl" },
        ]}
      />
    {/each}
  </div>
</div>
