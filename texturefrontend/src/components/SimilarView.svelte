<script lang="ts">
  import { CloseButton } from "flowbite-svelte";
  import RowView from "./table/RowView.svelte";
  import type { DatasetSchema } from "../backendapi";
  import { databaseConnection, datasetSchema } from "../stores";
  import { formatNumber } from "../shared/format";
  import TablePlaceholder from "./utils/TablePlaceholder.svelte";

  export let similarDocID: number;
  export let clearFunc: () => void;

  async function getData(_datasetSchema: DatasetSchema, _id: number) {
    // set up
    const colTypeMap = _datasetSchema.columns.reduce((acc, col) => {
      acc[col.name] = col.type;
      return acc;
    }, {});
    const pk_name = _datasetSchema.primary_key.name;

    // get original doc
    let originalDocArr = await databaseConnection.getDocsByID(_datasetSchema, [
      _id,
    ]);
    let originalDc = originalDocArr[0];

    let vsResponse = await databaseConnection.api.queryEmbedFromId(
      _datasetSchema.name,
      _id,
    );

    const orderedMap = new Map(
      vsResponse.result.map((doc) => [doc[pk_name], doc["_distance"]]),
    );

    let relatedDocsFull = await databaseConnection.getDocsByID(
      _datasetSchema,
      Array.from(orderedMap.keys()),
    );

    return {
      originalDoc: structureDoc(originalDc, pk_name, _id, colTypeMap),
      relatedDocs: relatedDocsFull.map((doc) =>
        structureDoc(
          doc,
          pk_name,
          doc[pk_name],
          colTypeMap,
          orderedMap.get(doc[pk_name]),
        ),
      ),
    };
  }

  function structureDoc(
    record: any,
    id_name: string,
    id_value: number,
    colTypeMap,
    distance?: number,
  ) {
    const rowArr = Object.entries(record);

    return {
      id: id_value,
      distance,
      textData: rowArr.filter(([k, v]) => colTypeMap[k] === "text"),
      metadata: rowArr.filter(
        ([k, v]) => colTypeMap[k] !== "text" && k !== id_name,
      ),
    };
  }

  $: dataPromise = getData($datasetSchema, similarDocID);
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
