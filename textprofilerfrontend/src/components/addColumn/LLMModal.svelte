<script lang="ts">
  import { databaseConnection } from "../../stores";
  import {
    Modal,
    Spinner,
    Select,
    Textarea,
    Button,
    Input,
  } from "flowbite-svelte";
  import type { DatasetInfo, TaskFormat } from "../../backendapi";
  import { CheckSolid, RocketSolid } from "flowbite-svelte-icons";
  import TransformPreview from "./TransformPreview.svelte";
  import { LLMQueryStatus } from "../../shared/types";

  const INSTRUCTION = `Describe how you want to transform the column data in a few sentences with as much details as possible.
For example, "Extract 3 - 5 keywords per article"`;

  // props
  export let panelOpen: boolean;
  export let datasetInfo: DatasetInfo;
  $: textCols = datasetInfo?.column_info.filter((col) => col.type === "text");
  $: allColNames = datasetInfo?.column_info.map((col) => col.name);
  $: idColName = datasetInfo?.joinDatasetInfo?.joinKey;

  // locals
  let targetColName: string;
  // let userPrompt: string;
  let userPrompt: string = "Does this article mention a user study?";
  // step 1 for schema
  let responseFormat: TaskFormat;
  let schemaResultStatus: LLMQueryStatus = LLMQueryStatus.NOT_STARTED;

  // step 2 for editable examples
  let example_idxs = [0, 1, 2];
  let columnExampleData: any[];
  let exampleResultStatus: LLMQueryStatus = LLMQueryStatus.NOT_STARTED;
  let exampleResult: any[];

  // step 3 for transform preview
  let preview_idxs = [3, 4, 5, 6, 7];
  let columnPreviewData: any[];
  let finalPreviewStatus: LLMQueryStatus = LLMQueryStatus.NOT_STARTED;
  let finalPreview: any[];

  // step 4 apply to entire column
  let commitResultStatus: LLMQueryStatus = LLMQueryStatus.NOT_STARTED;

  async function init(_textCols) {
    targetColName = _textCols?.[0].name;
    fetchColData();
  }

  function handleModalClose() {}

  function fetchColData() {
    if (targetColName && idColName) {
      databaseConnection
        .getValues(datasetInfo.name, idColName, targetColName, example_idxs)
        .then((r) => {
          columnExampleData = r;
        });

      databaseConnection
        .getValues(datasetInfo.name, idColName, targetColName, preview_idxs)
        .then((r) => {
          columnPreviewData = r;
        });
    }
  }

  let schemaEditTimer;
  async function getSchema() {
    schemaResultStatus = LLMQueryStatus.PENDING;
    console.log("Getting schema...");

    // TODO this maybe doesnt need to be LLM call, but kinda fun
    if (userPrompt) {
      let _responseFormat =
        await databaseConnection.api.getLlmResponseFormat(userPrompt);
      responseFormat = _responseFormat.result as TaskFormat;

      console.log("Schema is: ", responseFormat);
    }
    schemaResultStatus = LLMQueryStatus.COMPLETED;
  }

  async function submitInitialTransformation() {
    if (columnExampleData && responseFormat) {
      exampleResultStatus = LLMQueryStatus.PENDING;
      databaseConnection.api
        .getLlmTransformResult({
          userPrompt,
          taskFormat: responseFormat,
          columnData: columnExampleData.map((cd) => cd[targetColName]),
        })
        .then((r) => {
          let parsedResult = r.result;
          exampleResult = parsedResult.map(
            (item) => item[responseFormat.name] ?? "",
          );
          console.log("exampleResult is: ", exampleResult);
          exampleResultStatus = LLMQueryStatus.COMPLETED;
        });
    } else {
      console.error("Missing columnExampleData or responseFormat!");
    }
  }

  async function previewTransformation() {
    if (columnPreviewData && responseFormat) {
      finalPreviewStatus = LLMQueryStatus.PENDING;
      databaseConnection.api
        .getLlmTransformResult({
          userPrompt,
          taskFormat: responseFormat,
          columnData: columnPreviewData.map((cd) => cd[targetColName]),
          exampleData: columnExampleData.map((cd) => cd[targetColName]),
          exampleResponse: exampleResult.map((item) => ({
            [responseFormat.name]: item,
          })),
        })
        .then((r) => {
          let parsedResult = r.result;
          finalPreview = parsedResult.map(
            (item) => item[responseFormat.name] ?? "",
          );
          console.log("previewResult is: ", finalPreview);
          finalPreviewStatus = LLMQueryStatus.COMPLETED;
        });
    } else {
      console.error("Missing columnPreviewData or responseFormat!");
    }
  }

  async function applyToEntireColumn() {
    console.log("Applying to entire column");

    const data = {
      exampleData: columnExampleData.map((cd) => cd[targetColName]),
      exampleResponse: exampleResult,
    };
    console.log(data);

    // finalResultStatus = LLMQueryStatus.PENDING;
    // databaseConnection.api
    //   .commitLlmTransformResult({
    //     userPrompt,
    //     taskFormat: responseFormat,
    //     columnName: targetColName,
    //     tableName: datasetInfo.name,
    //     newColumnName: responseFormat.name,
    //   })
    //   .then((r) => {
    //     commitResultStatus = LLMQueryStatus.COMPLETED;
    //     console.log("commit result finished with: ", r);
    //   });
    commitResultStatus = LLMQueryStatus.COMPLETED;
  }

  function deleteResult(index) {
    columnExampleData.splice(index, 1);
    exampleResult.splice(index, 1);

    columnExampleData = columnExampleData; // trigger reactivity
    exampleResult = exampleResult; // trigger reactivity
  }

  $: initPromise = init(textCols);

  // error handling
  $: namingErrorExists =
    responseFormat?.name &&
    (allColNames.includes(responseFormat.name) ||
      allColNames.includes("MODEL_" + responseFormat.name));
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
      <div class="flex flex-col gap-4">
        <div class="text-black text-lg font-semibold">
          Extraction Prompt & Schema
        </div>
        <div class="flex gap-2 items-center">
          Extract from
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
        </div>

        <Textarea
          class="min-h-20"
          rows="5"
          placeholder={INSTRUCTION}
          bind:value={userPrompt}
          on:input={() => {
            clearTimeout(schemaEditTimer);
            schemaEditTimer = setTimeout(getSchema, 1000);
          }}
        />

        <div class="flex flex-wrap gap-2 items-center">
          <!-- Schema editor -->
          {#if responseFormat}
            <div class="flex gap-2 items-center">
              Schema
              <Input
                class="w-48"
                disabled={schemaResultStatus === LLMQueryStatus.PENDING}
                bind:value={responseFormat.name}
              />
              <Select
                class="w-48"
                disabled={schemaResultStatus === LLMQueryStatus.PENDING}
                items={[
                  {
                    value: "bool",
                    name: "bool",
                  },
                  {
                    value: "number",
                    name: "number",
                  },
                  {
                    value: "string",
                    name: "string",
                  },
                ]}
                placeholder="Response type..."
                bind:value={responseFormat.type}
              />
              <Select
                class="w-48"
                disabled={schemaResultStatus === LLMQueryStatus.PENDING}
                items={[
                  {
                    value: "single",
                    name: "single",
                  },
                  {
                    value: "multiple",
                    name: "multiple",
                  },
                ]}
                placeholder="Number responses..."
                bind:value={responseFormat.num_replies}
              />
            </div>
            <!-- {:else if userPrompt}
            <Button class="w-64 bg-gray-500" on:click={getSchema}>
              Generate initial schema
            </Button> -->
          {/if}
          {#if schemaResultStatus === LLMQueryStatus.PENDING}
            <Spinner />
          {/if}

          <Button
            class="w-64 ml-auto"
            on:click={submitInitialTransformation}
            disabled={!userPrompt || namingErrorExists || !responseFormat}
          >
            {#if exampleResultStatus === LLMQueryStatus.PENDING}
              <Spinner size="4" class="mr-2" />
            {:else}
              <CheckSolid size="sm" class="mr-2" />
            {/if}
            Get example responses
          </Button>
        </div>
        {#if namingErrorExists}
          <div class="text-red-500">
            Column {responseFormat.name} is already in the dataset, try another name!
          </div>
        {/if}

        {#if exampleResultStatus !== LLMQueryStatus.NOT_STARTED && columnExampleData}
          <!-- Sample response table -->
          <div class="text-black text-lg font-semibold">Curate Examples</div>

          <TransformPreview
            {idColName}
            {targetColName}
            {responseFormat}
            columnData={columnExampleData}
            bind:resultData={exampleResult}
            queryStatus={exampleResultStatus}
            {deleteResult}
          />

          <div class="flex gap-2 items-center">
            <Button
              class="w-64 ml-auto"
              on:click={previewTransformation}
              disabled={!userPrompt}
            >
              {#if finalPreviewStatus === LLMQueryStatus.PENDING}
                <Spinner size="4" class="mr-2" />
              {:else}
                <CheckSolid size="sm" class="mr-2" />
              {/if}
              Preview Transform
            </Button>
          </div>
        {/if}

        {#if finalPreviewStatus !== LLMQueryStatus.NOT_STARTED && columnPreviewData}
          <div class="text-black text-lg font-semibold">
            Preview transformation
          </div>

          <TransformPreview
            {idColName}
            {targetColName}
            {responseFormat}
            columnData={columnPreviewData}
            bind:resultData={finalPreview}
            queryStatus={finalPreviewStatus}
            allowEdits={false}
          />

          <div class="flex gap-2 items-center">
            {#if commitResultStatus === LLMQueryStatus.PENDING}
              <Spinner />
            {:else if commitResultStatus === LLMQueryStatus.COMPLETED}
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
      </div>
    {/if}
  {/await}
</Modal>
