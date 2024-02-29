<script lang="ts">
  import { CloseButton } from "flowbite-svelte";
  import RowView from "./table/RowView.svelte";
  import type { DatasetInfo } from "../backendapi";
  import { databaseConnection, datasetInfo } from "../stores";
  import { formatNumber } from "../shared/format";
  import TablePlaceholder from "./utils/TablePlaceholder.svelte";

  export let similarDocID: number;
  export let clearFunc: () => void;

  async function getData(_datasetInfo: DatasetInfo, _id: number) {
    let originalDocArr = await databaseConnection.getDocsByID(_datasetInfo, [
      _id,
    ]);
    let originalDc = originalDocArr[0];

    let vsResponse = await databaseConnection.api.queryEmbedFromId(
      _datasetInfo.name,
      _id,
    );

    let relatedDocIDs = vsResponse.result.map(
      (doc) => doc[_datasetInfo.primary_key.name],
    );

    const idDistMap = vsResponse.result.reduce((acc, doc) => {
      // distance returned will be in col "_distance"
      acc[doc[_datasetInfo.primary_key.name]] = doc["_distance"];
      return acc;
    }, {});

    let relatedDocsFull = await databaseConnection.getDocsByID(
      _datasetInfo,
      relatedDocIDs,
    );

    return {
      originalDoc: structureDoc(originalDc, _datasetInfo, _id),
      relatedDocs: relatedDocsFull.map((doc, idx) =>
        structureDoc(
          doc,
          _datasetInfo,
          relatedDocIDs[idx],
          idDistMap[relatedDocIDs[idx]],
        ),
      ),
    };
  }

  function structureDoc(
    record: any,
    _datasetInfo: DatasetInfo,
    id: number,
    distance?: number,
  ) {
    const rowArr = Object.entries(record);
    const colTypeMap = $datasetInfo.columns.reduce((acc, col) => {
      acc[col.name] = col.type;
      return acc;
    }, {});

    return {
      id,
      distance,
      textData: rowArr.filter(([k, v]) => colTypeMap[k] === "text"),
      metadata: rowArr.filter(
        ([k, v]) =>
          colTypeMap[k] !== "text" && k !== $datasetInfo.primary_key.name,
      ),
    };
  }

  $: dataPromise = getData($datasetInfo, similarDocID);
</script>

<div class="max-h-screen overflow-auto bg-gray-100 h-full">
  {#await dataPromise}
    <div class="p-4">
      <TablePlaceholder />
    </div>
  {:then data}
    <div
      class="p-4 sticky top-0 w-full bg-white border border-dashed border-primary-500"
    >
      <div class="flex items-center mb-2">
        <h3 class="self-center font-semibold text-lg">
          View similar documents
        </h3>
        <CloseButton on:click={clearFunc} />
      </div>

      <RowView
        id={data.originalDoc.id}
        textData={data.originalDoc.textData}
        metadata={data.originalDoc.metadata}
        originalMetadata={data.originalDoc.metadata}
      >
        <div slot="title" class="font-semibold">Original Record</div>
      </RowView>
    </div>
    <div class="bg-gray-100 p-4 flex flex-col gap-2">
      {#each data.relatedDocs as relatedDoc}
        <RowView
          id={relatedDoc.id}
          textData={relatedDoc.textData}
          metadata={relatedDoc.metadata}
          originalMetadata={data.originalDoc.metadata}
        >
          <div slot="title" class="italic text-gray-500">
            Distance: {formatNumber(relatedDoc.distance)}
          </div>
        </RowView>
      {/each}
    </div>
  {:catch error}
    <div>Error: {error.message}</div>
  {/await}
</div>
