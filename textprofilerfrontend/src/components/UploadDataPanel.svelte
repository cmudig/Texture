<script lang="ts">
  import { getContext } from "svelte";
  import type { DefaultService, GenericResponse } from "../backendapi";
  import { Button, Modal, Spinner } from "flowbite-svelte";
  import { UploadOutline } from "flowbite-svelte-icons";

  export let panelOpen: boolean;

  let backendService: DefaultService = getContext("backendService");
  let fileUploadList: FileList | undefined;
  let nextResponse: Promise<GenericResponse> | undefined;

  function handleFileUpload() {
    if (fileUploadList && fileUploadList.length > 0) {
      const selectedFile = fileUploadList[0];
      // Perform file upload logic here
      console.log("Uploading file:", selectedFile.name);

      nextResponse = backendService.uploadDataset({ file: selectedFile });
    } else {
      console.log("No file selected");
    }
  }

  function handleModelClose() {
    fileUploadList = undefined;
    nextResponse = undefined;
  }
</script>

<Modal bind:open={panelOpen} on:close={handleModelClose} title="Add dataset">
  <div class="flex flex-col gap-2">
    <p class="mb-4">Upload csv or parquet file with your data</p>

    <!-- <p>
      {#if fileUploadList}
        Total num files: {fileUploadList.length}

        {#each fileUploadList as file}
          {file.name}
        {/each}
      {:else}
        No files.
      {/if}
    </p> -->

    <div class="flex gap-2">
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

    {#if nextResponse}
      {#await nextResponse}
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
</Modal>
