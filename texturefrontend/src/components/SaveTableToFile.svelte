<script lang="ts">
  import { Button, Spinner } from "flowbite-svelte";
  import { CheckSolid, DownloadSolid } from "flowbite-svelte-icons";
  import { databaseConnection, datasetSchema } from "../stores";
  import { QueryStatus } from "../shared/types";

  let saveStatus: QueryStatus = QueryStatus.NOT_STARTED;

  async function doSave() {
    saveStatus = QueryStatus.PENDING;
    databaseConnection.api.saveDatabaseToFile($datasetSchema.name).then((r) => {
      saveStatus = QueryStatus.COMPLETED;

      setTimeout(() => {
        saveStatus = QueryStatus.NOT_STARTED;
      }, 2000);
    });
  }
</script>

<Button on:click={doSave} size="sm">
  {#if saveStatus === QueryStatus.COMPLETED}
    <CheckSolid size="sm" class="mr-2" />
  {:else if saveStatus === QueryStatus.PENDING}
    <Spinner size="4" class="mr-2" />
  {:else}
    <DownloadSolid size="sm" class="mr-2" />
  {/if}

  Save current dataset to file
</Button>
