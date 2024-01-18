<script lang="ts">
  import { getContext } from "svelte";
  import { Button, Modal, Spinner } from "flowbite-svelte";
  import { CheckSolid, UploadOutline, CloseSolid } from "flowbite-svelte-icons";

  import type {
    DefaultService,
    DatasetUploadResponse,
    DatasetVerifyResponse,
    DatasetInfo,
  } from "../../backendapi";
  import SchemaEditor from "./SchemaEditor.svelte";

  enum Status {
    INITIAL_UPLOAD = 0,
    VERIFY_TYPES = 1,
    COMPLETED = 2,
  }

  export let panelOpen: boolean;
  export let finishedCount = 0;
  let currentStatus: Status = Status.INITIAL_UPLOAD;

  // stage 1 vars
  let backendService: DefaultService = getContext("backendService");
  let fileUploadList: FileList | undefined;
  let firstResponse: Promise<DatasetUploadResponse> | undefined;

  // stage 2 vars
  let parsedSchema: DatasetInfo | undefined;
  let secondResponse: Promise<DatasetVerifyResponse> | undefined;

  function handleFileUpload() {
    if (fileUploadList && fileUploadList.length > 0) {
      const selectedFile = fileUploadList[0];
      // Perform file upload logic here
      console.log("Uploading file:", selectedFile.name);

      firstResponse = backendService.uploadDataset({ file: selectedFile });

      firstResponse.then((response) => {
        if (response.success) {
          console.log("File uploaded successfully");

          parsedSchema = response.datasetSchema;
          currentStatus = Status.VERIFY_TYPES;
        } else {
          console.error("Error uploading file:", response.message);
        }
      });
    } else {
      console.log("No file selected");
    }
  }

  function handleSchemaVerification() {
    if (parsedSchema) {
      secondResponse = backendService.verifySchema(parsedSchema);

      secondResponse.then((response) => {
        if (response.success) {
          console.log("Schema verified successfully");
          currentStatus = Status.COMPLETED;

          // TODO also need to signal outside this component that a new dataset successfully uploaded...
          finishedCount += 1;
        } else {
          console.error("Error verifying schema:", response.message);
        }
      });
    } else {
      console.error("No schema to verify");
    }
  }

  function handleModalClose() {
    currentStatus = Status.INITIAL_UPLOAD;
    fileUploadList = undefined;
    firstResponse = undefined;
    parsedSchema = undefined;
    secondResponse = undefined;
  }
</script>

<Modal
  bind:open={panelOpen}
  on:close={handleModalClose}
  title="Add dataset"
  outsideclose
>
  {#if currentStatus === Status.INITIAL_UPLOAD}
    <div class="flex flex-col gap-2">
      <p class="mb-4">Upload csv or parquet file with your data</p>

      <div class="flex gap-2">
        <!-- TODO: add drag and drop data upload -->
        <input type="file" accept=".csv,.parquet" bind:files={fileUploadList} />

        <Button
          class="w-64"
          disabled={!(fileUploadList && fileUploadList.length > 0)}
          on:click={handleFileUpload}
        >
          <UploadOutline size="sm" class="mr-2" />
          Upload
        </Button>
      </div>

      {#if firstResponse}
        {#await firstResponse}
          <div class="p-4 flex gap-2 items-center">
            <Spinner size={"6"} />
            <p>Uploading...</p>
          </div>
        {:then response}
          {#if response.success}
            <p class="text-green-700">{response.message}</p>
          {:else}
            <p class="text-red-700"><b>Error:</b> {response.message}</p>
          {/if}
        {/await}
      {/if}
    </div>
  {:else if currentStatus === Status.VERIFY_TYPES}
    <div class="flex flex-col gap-4">
      <p class="italic">Edit dataset schema</p>

      {#if parsedSchema}
        <div class="m-2">
          <SchemaEditor bind:schema={parsedSchema} />
        </div>
      {/if}

      <Button class="w-64" on:click={handleSchemaVerification}>
        <CheckSolid size="sm" class="mr-2" />
        Looks good
      </Button>

      {#if secondResponse}
        {#await secondResponse}
          <div class="p-4 flex gap-2 items-center">
            <Spinner size={"6"} />
            <p>Verifying schema...</p>
          </div>
        {:then response}
          {#if response.success}
            <p class="text-green-700">{response.message}</p>
          {:else}
            <p class="text-red-700"><b>Error:</b> {response.message}</p>
          {/if}
        {/await}
      {/if}
    </div>
  {:else if currentStatus === Status.COMPLETED}
    <p class="bold">Data successfully uploaded!</p>

    <Button
      class="w-64"
      on:click={() => {
        panelOpen = false;
      }}
    >
      <CloseSolid size="sm" class="mr-2" />
      Close
    </Button>
  {/if}
</Modal>
