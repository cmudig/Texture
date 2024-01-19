<script lang="ts">
  import { getContext } from "svelte";
  import { Button, Modal, Spinner, Dropzone } from "flowbite-svelte";
  import { CheckSolid, CloseSolid } from "flowbite-svelte-icons";

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
  let fileUpload: File | undefined;
  let firstResponse: Promise<DatasetUploadResponse> | undefined;
  let currentlyDragging = false;

  // stage 2 vars
  let parsedSchema: DatasetInfo | undefined;
  let parsedOriginalName: string | undefined;
  let secondResponse: Promise<DatasetVerifyResponse> | undefined;

  function handleFileUpload() {
    if (fileUpload) {
      // Perform file upload logic here
      console.log("Uploading file:", fileUpload.name);
      firstResponse = backendService.uploadDataset({ file: fileUpload });

      firstResponse.then((response) => {
        if (response.success) {
          console.log("File cached successfully (not yet in db)");

          parsedSchema = response.datasetSchema;
          parsedOriginalName = response.datasetSchema?.name;
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
    if (parsedSchema && parsedOriginalName) {
      secondResponse = backendService.verifySchema(
        parsedOriginalName,
        parsedSchema
      );

      secondResponse.then((response) => {
        if (response.success) {
          console.log("File loaded and verified successfully");
          currentStatus = Status.COMPLETED;

          // TODO here need to signal to outside this component that a new dataset successfully uploaded...
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
    fileUpload = undefined;
    firstResponse = undefined;
    parsedSchema = undefined;
    secondResponse = undefined;
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();

    if (event.dataTransfer) {
      if (event.dataTransfer.items && event.dataTransfer.items.length > 0) {
        let firstItem = event.dataTransfer.items[0];
        if (firstItem.kind === "file") {
          const file = firstItem.getAsFile();
          if (file) {
            fileUpload = file;
          }
        }
      } else if (
        event.dataTransfer.files &&
        event.dataTransfer.files.length > 0
      ) {
        fileUpload = event.dataTransfer.files[0];
      }
    }

    currentlyDragging = false;
    handleFileUpload();
  }

  function handleFileClickUpload(event: Event) {
    const files = (event.target as HTMLInputElement)?.files;
    if (files && files.length > 0) {
      fileUpload = files[0];
    }
    handleFileUpload();
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
      <Dropzone
        id="dropzone"
        on:drop={handleDrop}
        on:dragover={(event) => {
          event.preventDefault();
          currentlyDragging = true;
        }}
        on:dragleave={() => {
          currentlyDragging = false;
        }}
        on:change={handleFileClickUpload}
        class={currentlyDragging ? "border-primary-700" : ""}
      >
        <svg
          aria-hidden="true"
          class="mb-3 w-10 h-10 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
        {#if !fileUpload}
          <p
            class="mb-2 text-sm text-gray-500 dark:text-gray-400 font-semibold"
          >
            Click to upload or drag and drop
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            CSV or PARQUET files only
          </p>
        {:else}
          <p>{fileUpload.name}</p>

          {#if firstResponse}
            {#await firstResponse}
              <div class="p-4 flex gap-2 items-center">
                <Spinner size={"6"} />
                <p>Uploading...</p>
              </div>
            {:then response}
              <div class="p-4">
                {#if response.success}
                  <p class="text-green-700">{response.message}</p>
                {:else}
                  <p class="text-red-700"><b>Error:</b> {response.message}</p>
                {/if}
              </div>
            {/await}
          {/if}
        {/if}
      </Dropzone>
    </div>
  {:else if currentStatus === Status.VERIFY_TYPES}
    <div class="flex flex-col gap-4">
      <p class="italic">Edit dataset schema</p>

      <div class="m-2">
        {#if parsedSchema}
          <SchemaEditor bind:schema={parsedSchema} />
        {:else}
          <div>Hmmm something went wrong, please restart dataset upload.</div>
        {/if}
      </div>
      <Button class="w-64 ml-auto mr-2" on:click={handleSchemaVerification}>
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
    <p class="text-green-700">Data successfully uploaded!</p>
  {/if}
</Modal>
