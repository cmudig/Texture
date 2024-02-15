<script lang="ts">
  import { databaseConnection } from "../../stores";
  import { Modal, Spinner, Select, Textarea, Button } from "flowbite-svelte";
  import type { DatasetInfo } from "../../backendapi";
  import { CheckSolid } from "flowbite-svelte-icons";
  import TextPlaceholder from "../utils/TextPlaceholder.svelte";

  enum LLMQueryStatus {
    NOT_STARTED = 0,
    PENDING = 1,
    COMPLETED = 2,
  }

  const INSTRUCTION = `Describe how you want to transform the column data in a few sentences with as much details as possible.
For example, "Extract 3 - 5 keywords per article"`;

  // props
  export let panelOpen: boolean;
  export let datasetInfo: DatasetInfo;
  $: textCols = datasetInfo?.column_info.filter((col) => col.type === "text");

  // locals
  let targetColName: string;
  let responseFormat;
  let previewResult;
  let columnData: any[];
  let resultStatus: LLMQueryStatus = LLMQueryStatus.NOT_STARTED;
  let userPrompt: string;
  // let userPrompt: string = "Extract all urls from the passage, if any";

  async function init(_textCols) {
    targetColName = _textCols?.[0].name;
    fetchColData();
  }

  function handleModalClose() {}

  function fetchColData() {
    // console.log("Getting column data for column: ", targetColName);
    if (targetColName) {
      databaseConnection
        .getValues(datasetInfo.name, targetColName, 5)
        .then((r) => {
          columnData = r;
          // console.log("column data is: ", columnData);
        });
    }
  }

  async function submitInitialTransformation() {
    resultStatus = LLMQueryStatus.PENDING;
    let _responseFormat =
      await databaseConnection.api.getLlmResponseFormat(userPrompt);
    responseFormat = _responseFormat.result;

    console.log("response format is: ", responseFormat);

    databaseConnection.api
      .getLlmTransformResult({
        userPrompt,
        taskFormat: JSON.stringify(responseFormat),
        columnData: columnData.map((cd) => cd[targetColName]),
        tableName: null,
        newColumnName: null,
      })
      .then((r) => {
        previewResult = r.result;
        console.log("preview result is: ", previewResult);
        resultStatus = LLMQueryStatus.COMPLETED;
      });
  }

  $: initPromise = init(textCols);
</script>

<Modal
  bind:open={panelOpen}
  on:close={handleModalClose}
  title="Extract new column"
  size="xl"
  outsideclose
>
  {#await initPromise}
    <div class="p-2">
      <Spinner />
    </div>
  {:then r}
    {#if textCols}
      <div class="flex flex-col gap-2">
        <Textarea
          class="min-h-20"
          rows="5"
          placeholder={INSTRUCTION}
          bind:value={userPrompt}
        />

        <div class="flex gap-2 items-center">
          Transform column
          <Select
            class="w-64"
            size="sm"
            items={textCols.map((k) => ({
              value: k.name,
              name: k.name,
            }))}
            placeholder="Select column"
            bind:value={targetColName}
            on:change={fetchColData}
          />

          <Button
            class="w-64 ml-auto"
            on:click={() => {
              submitInitialTransformation();
            }}
            disabled={!userPrompt}
          >
            {#if resultStatus === LLMQueryStatus.PENDING}
              <Spinner size="4" class="mr-2" />
            {:else}
              <CheckSolid size="sm" class="mr-2" />
            {/if}
            Generate sample response
          </Button>
        </div>
      </div>
      {#if resultStatus !== LLMQueryStatus.NOT_STARTED && columnData}
        <div class="border border-gray-200">
          <div class="flex bg-gray-50 border-b border-gray-200 font-semibold">
            <div class="w-1/2 whitespace-normal break-words p-2">
              {targetColName}
            </div>
            <div
              class="w-1/2 whitespace-normal break-words p-2 border-l border-gray-200 text-black"
            >
              {#if responseFormat}
                {Object.keys(responseFormat)
                  .map(
                    (k) =>
                      `${k} (${responseFormat[k]?.type}${responseFormat[k]?.num_replies === "single" ? "" : "[]"})`,
                  )
                  .join(", ")}
              {:else}
                <Spinner />
              {/if}
            </div>
          </div>

          {#each columnData as cd, index}
            <div class="flex border-b border-gray-200">
              <div
                class="w-1/2 whitespace-normal break-words align-top p-2 overflow-auto max-h-32"
              >
                {cd[targetColName]}
              </div>
              <div
                class="w-1/2 whitespace-normal break-words border-l border-gray-200 bg-green-50 text-black align-top p-2 overflow-auto max-h-32"
              >
                {#if resultStatus === LLMQueryStatus.COMPLETED}
                  {Object.keys(responseFormat)
                    .map((k) => previewResult[index][k])
                    .join(", ")}
                {:else}
                  <TextPlaceholder />
                {/if}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    {/if}
  {/await}
</Modal>
