<script lang="ts">
  import { CloseButton } from "flowbite-svelte";
  import DocumentDisplay from "./DocumentDisplay.svelte";
  import type { DatasetInfo } from "../backendapi";
  import { databaseConnection } from "../stores";

  export let similarDocID: BigInt;
  export let datasetInfo: DatasetInfo;
  export let clearFunc: () => void;

  async function getData(
    _datasetInfo: DatasetInfo,
    _id: BigInt,
    _textColName: string,
  ) {
    let numID = Number(_id);

    let originalDocArr = await databaseConnection.getDocsByID(_datasetInfo, [
      numID,
    ]);
    let originalDc = originalDocArr[0];

    let vsResponse = await databaseConnection.api.queryEmbedFromId(
      _datasetInfo.name,
      numID,
    );

    let relatedDocIDs = vsResponse.result.map(
      (doc) => doc[_datasetInfo.primary_key.name],
    );

    let relatedDocsFull = await databaseConnection.getDocsByID(
      _datasetInfo,
      relatedDocIDs,
    );

    return {
      originalDoc: structureDoc(originalDc, _textColName, numID),
      relatedDocs: relatedDocsFull.map((doc, idx) =>
        structureDoc(doc, _textColName, relatedDocIDs[idx]),
      ),
    };
  }

  function structureDoc(doc: any, textColKey: string, id: number) {
    return {
      id,
      document: doc[textColKey],
      docName: textColKey,
      metadata: Object.entries(doc).filter(([k, v]) => k !== textColKey),
    };
  }

  // TODO -- TEMP this only renders the first text col, rest is metadata
  $: firstTextColName =
    datasetInfo.column_info.find((col) => col.type === "text")?.name ??
    "None found";

  $: dataPromise = getData(datasetInfo, similarDocID, firstTextColName);
</script>

<div class="flex items-center bg-gray-50 h-10 px-2">
  <h3 class="self-center font-semibold text-lg">Similar View</h3>
  <CloseButton on:click={clearFunc} />
</div>
<div class="max-h-screen overflow-auto">
  {#await dataPromise}
    <div>Loading...</div>
  {:then data}
    <div
      class="p-4 sticky top-0 w-full bg-white border border-dashed border-primary-500"
    >
      <h3 class="font-semibold mb-2">Pinned Document</h3>

      <DocumentDisplay
        id={data.originalDoc.id}
        document={data.originalDoc.document}
        docName={data.originalDoc.docName}
        metadata={data.originalDoc.metadata}
      />
    </div>
    <div class="bg-gray-100 p-4 flex flex-col gap-2">
      {#each data.relatedDocs as relatedDoc}
        <DocumentDisplay
          id={relatedDoc.id}
          document={relatedDoc.document}
          docName={relatedDoc.docName}
          metadata={relatedDoc.metadata}
        />
      {/each}
    </div>
  {:catch error}
    <div>Error: {error.message}</div>
  {/await}
</div>
