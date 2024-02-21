<script lang="ts">
  import { databaseConnection } from "../../stores";
  import { Modal, Spinner, Select, Textarea, Button } from "flowbite-svelte";
  import type { DatasetInfo } from "../../backendapi";
  import {
    CheckSolid,
    TrashBinOutline,
    RocketSolid,
  } from "flowbite-svelte-icons";
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
  let responseFormat; // { "name": "email_addresses", "type": "string", "num_replies": "multiple" }
  let previewResult;
  let columnData: any[];
  let sampleResultStatus: LLMQueryStatus = LLMQueryStatus.NOT_STARTED;
  let finalResultStatus: LLMQueryStatus = LLMQueryStatus.NOT_STARTED;
  let userPrompt: string;

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
    if (columnData) {
      sampleResultStatus = LLMQueryStatus.PENDING;
      let _responseFormat =
        await databaseConnection.api.getLlmResponseFormat(userPrompt);
      responseFormat = _responseFormat.result;

      console.log("response format is: ", responseFormat);

      const stringFormat = `{ "${responseFormat.name ?? "colName"}": { "type": "${responseFormat.type ?? "string"}", "num_replies": "${responseFormat.num_replies ?? "single"}" } }`;

      databaseConnection.api
        .getLlmTransformResult({
          userPrompt,
          taskFormat: stringFormat,
          columnData: columnData.map((cd) => cd[targetColName]),
        })
        .then((r) => {
          let parsedResult = r.result;
          previewResult = parsedResult.map(
            (item) => item[responseFormat.name] ?? "",
          );
          console.log("preview result is: ", previewResult);
          sampleResultStatus = LLMQueryStatus.COMPLETED;
        });
    } else {
      console.error("No column data to transform!");
    }
  }

  async function applyToEntireColumn() {
    console.log("Applying to entire column");

    // FUTURE: use curated dataset examples
    // const data = {
    //   exampleData: columnData.map((cd) => cd[targetColName]),
    //   exampleResponse: previewResult,
    // };
    // console.log(data);

    const stringFormat = `{ "${responseFormat.name ?? "colName"}": { "type": "${responseFormat.type ?? "string"}", "num_replies": "${responseFormat.num_replies ?? "single"}" } }`;

    finalResultStatus = LLMQueryStatus.PENDING;
    databaseConnection.api
      .commitLlmTransformResult({
        userPrompt,
        taskFormat: stringFormat,
        columnName: targetColName,
        tableName: datasetInfo.name,
        newColumnName: responseFormat.name,
      })
      .then((r) => {
        finalResultStatus = LLMQueryStatus.COMPLETED;
        console.log("commit result finished with: ", r);
      });
  }

  function deleteResult(index) {
    columnData.splice(index, 1);
    previewResult.splice(index, 1);

    columnData = columnData; // trigger reactivity
    previewResult = previewResult; // trigger reactivity
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
            {#if sampleResultStatus === LLMQueryStatus.PENDING}
              <Spinner size="4" class="mr-2" />
            {:else}
              <CheckSolid size="sm" class="mr-2" />
            {/if}
            Generate sample response
          </Button>
        </div>
      </div>
      {#if sampleResultStatus !== LLMQueryStatus.NOT_STARTED && columnData}
        <div class="">
          <div class="flex font-semibold">
            <div
              class="w-1/2 whitespace-normal break-words p-2 bg-gray-50 border-l border-y border-gray-200"
            >
              {targetColName}
            </div>
            <div
              class="grow whitespace-normal break-words p-2 border-l border-y border-gray-200 text-black bg-gray-50"
            >
              {#if responseFormat}
                {`${responseFormat.name} (${responseFormat?.type}${responseFormat.num_replies === "single" ? "" : "[]"})`}
              {:else}
                <Spinner />
              {/if}
            </div>
            <div class="w-8 border-l border-gray-200" />
          </div>

          {#each columnData as cd, index}
            <div class="flex">
              <div
                class="w-1/2 whitespace-normal break-words align-top p-2 overflow-auto max-h-32 border-b border-l border-gray-200"
              >
                {cd[targetColName]}
              </div>
              <div
                class="grow whitespace-normal break-words border-l border-b border-gray-200 bg-green-50 text-black align-top p-2 overflow-auto max-h-32"
              >
                {#if sampleResultStatus === LLMQueryStatus.COMPLETED}
                  <Textarea
                    rows="3"
                    bind:value={previewResult[index]}
                    class="bg-white/50"
                  />
                {:else}
                  <TextPlaceholder />
                {/if}
              </div>

              <div class="w-8 border-l border-gray-200">
                <button
                  class="hover:bg-gray-100 text-gray-500 p-1 rounded m-1"
                  on:click={() => deleteResult(index)}
                >
                  <TrashBinOutline size="sm" />
                </button>
              </div>
            </div>
          {/each}
        </div>
        <div class="flex gap-2 items-center">
          {#if finalResultStatus === LLMQueryStatus.PENDING}
            <Spinner />
          {:else if finalResultStatus === LLMQueryStatus.COMPLETED}
            <div class="text-green-500">Completed query!</div>
          {/if}

          <Button
            class="w-64 ml-auto"
            on:click={applyToEntireColumn}
            disabled={!userPrompt}
          >
            <RocketSolid size="sm" class="mr-2" />

            Apply to entire column
          </Button>
        </div>
      {/if}
    {/if}
  {/await}
</Modal>
