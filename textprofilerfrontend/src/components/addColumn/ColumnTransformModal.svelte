<script lang="ts">
  import {
    databaseConnection,
    datasetInfo,
    filteredIndices,
    filteredCount,
  } from "../../stores";
  import { Modal, Spinner, Select, Button } from "flowbite-svelte";
  import { TaskFormat } from "../../backendapi";
  import {
    RocketSolid,
    WandMagicSparklesOutline,
    CodeOutline,
    CheckSolid,
  } from "flowbite-svelte-icons";
  import TransformPreview from "./TransformPreview.svelte";
  import { QueryStatus } from "../../shared/types";
  import { formatInt } from "../../shared/format";
  import SchemaEditor from "./SchemaEditor.svelte";
  import LLMExtract from "./LLMTransform/LLMExtract.svelte";
  import CodeExtract from "./CodeTransform/CodeExtract.svelte";

  // props
  export let panelOpen: boolean;
  export let finishedCommitHandler: () => void;

  $: textCols = $datasetInfo?.columns.filter((col) => col.type === "text");
  $: allColNames = $datasetInfo?.columns.map((col) => col.name);
  $: idColName = $datasetInfo?.primary_key.name;

  // locals
  let targetColName: string;
  let transformType: "llm" | "code" = "code";

  // example data
  let example_idxs = [0, 1, 2];
  let preview_idxs = [3, 4, 5, 6, 7];

  filteredIndices.subscribe((newIndices) => {
    example_idxs =
      newIndices && newIndices.length > 0 ? newIndices.slice(0, 3) : [0, 1, 2];

    preview_idxs =
      newIndices && newIndices.length > 3
        ? newIndices.slice(3, 8)
        : [3, 4, 5, 6, 7];

    fetchColData();
  });

  // schema
  let responseSchema: TaskFormat = {
    name: "",
    type: TaskFormat.type.STRING,
    num_replies: TaskFormat.num_replies.SINGLE,
  };
  let schemaResultStatus: QueryStatus = QueryStatus.NOT_STARTED;

  // specify transform
  let userPrompt: string;
  let columnExampleData: any[];
  let exampleResult: any[];
  let userTransformCode: string;

  // preview transform
  let readyToGenPreview = false;
  let columnPreviewData: any[];
  let finalPreviewStatus: QueryStatus = QueryStatus.NOT_STARTED;
  let previewProcessingError;
  let finalPreview: any[];

  // apply to final result
  let commitResultStatus: QueryStatus = QueryStatus.NOT_STARTED;
  let commitError;

  async function init(_textCols) {
    targetColName = _textCols?.[0].name;
    fetchColData();
  }

  function fetchColData() {
    if (targetColName && idColName) {
      databaseConnection
        .getValues($datasetInfo.name, idColName, targetColName, example_idxs)
        .then((r) => {
          columnExampleData = r;
        });

      databaseConnection
        .getValues($datasetInfo.name, idColName, targetColName, preview_idxs)
        .then((r) => {
          columnPreviewData = r;
        });
    }
  }

  async function generatePreview() {
    console.log(`Generating ${transformType} preview`);
    finalPreviewStatus = QueryStatus.PENDING;
    let r;

    if (transformType === "llm") {
      r = await databaseConnection.api.getLlmTransformResult({
        userPrompt,
        taskFormat: responseSchema,
        columnData: columnPreviewData.map((cd) => cd[targetColName]),
        exampleData: columnExampleData.map((cd) => cd[targetColName]),
        exampleResponse: exampleResult.map((item) => ({
          [responseSchema.name]: item,
        })),
      });
    } else {
      r = await databaseConnection.api.getCodeTransformResult({
        codeString: userTransformCode,
        taskFormat: responseSchema,
        columnData: columnPreviewData.map((cd) => cd[targetColName]),
      });
    }

    finalPreviewStatus = QueryStatus.COMPLETED;

    if (r.success) {
      previewProcessingError = undefined;
      finalPreview = r.result;
      console.log("Final Preview: ", finalPreview);
    } else {
      console.error("Error in code transform: ", r.result?.error);
      previewProcessingError = r.result?.error;
    }
  }

  async function deriveEntireColumn() {
    console.log(`Applying ${transformType} transform to entire column.`);
    commitResultStatus = QueryStatus.PENDING;
    let r;

    if (transformType === "llm") {
      r = await databaseConnection.api.commitLlmTransformResult({
        userPrompt,
        taskFormat: responseSchema,
        columnName: targetColName,
        tableName: $datasetInfo.name,
        exampleData: columnExampleData.map((cd) => cd[targetColName]),
        exampleResponse: exampleResult.map((item) => ({
          [responseSchema.name]: item,
        })),
        applyToIndices: $filteredIndices,
      });
    } else {
      r = await databaseConnection.api.commitCodeTransformResult({
        codeString: userTransformCode,
        taskFormat: responseSchema,
        columnName: targetColName,
        tableName: $datasetInfo.name,
        applyToIndices: $filteredIndices,
      });
    }

    commitResultStatus = QueryStatus.COMPLETED;
    if (r.success) {
      commitError = undefined;
      finishedCommitHandler();
    } else {
      commitError = r.result?.error;
    }
  }

  $: initPromise = init(textCols);
  // error handling
  $: namingErrorExists =
    responseSchema?.name && allColNames.includes(responseSchema.name);
</script>

<Modal bind:open={panelOpen} title="Extract new column" size="xl" outsideclose>
  {#await initPromise}
    <div class="p-2">
      <Spinner />
    </div>
  {:then _}
    {#if textCols}
      <div class="flex flex-col gap-8">
        <div class="flex gap-2 items-center">
          From
          <Select
            class="w-64 bg-white"
            size="sm"
            items={textCols.map((k) => ({
              value: k.name,
              name: k.name,
            }))}
            placeholder="Select column"
            bind:value={targetColName}
            on:change={fetchColData}
          />
          <p>applied to current selection ({formatInt($filteredCount)} rows)</p>
        </div>

        <div>
          <div class="flex w-full">
            <Button
              color={transformType === "llm" ? "primary" : "alternative"}
              class="flex items-center gap-2 w-1/2 text-md py-4 rounded-none rounded-tl-lg"
              on:click={() => (transformType = "llm")}
            >
              <WandMagicSparklesOutline size="sm" />
              Extract with LLM
            </Button>

            <Button
              color={transformType === "code" ? "primary" : "alternative"}
              class="flex items-center gap-2 w-1/2 text-md py-4 rounded-none rounded-tr-lg"
              on:click={() => (transformType = "code")}
            >
              <CodeOutline size="sm" />
              Extract with code
            </Button>
          </div>

          <div class="p-4 flex flex-col bg-gray-100 rounded-b-lg">
            <div class="flex gap-2 items-center mb-8">
              <SchemaEditor
                bind:responseSchema
                disabled={schemaResultStatus === QueryStatus.PENDING}
              />
              {#if schemaResultStatus === QueryStatus.PENDING}
                <Spinner />
              {/if}
              {#if namingErrorExists}
                <div class="text-red-500">
                  Column {responseSchema.name} is already in the dataset, try another
                  name!
                </div>
              {/if}
            </div>

            {#if transformType === "llm"}
              <LLMExtract
                {targetColName}
                {idColName}
                setPreviewReady={(v) => (readyToGenPreview = v)}
                bind:userPrompt
                bind:responseSchema
                bind:schemaResultStatus
                bind:columnExampleData
                bind:exampleResult
              />
            {:else}
              <CodeExtract
                {targetColName}
                bind:userTransformCode
                bind:responseSchema
                setPreviewReady={(v) => (readyToGenPreview = v)}
              />
            {/if}
          </div>
        </div>

        {#if readyToGenPreview}
          <Button
            class="w-64"
            on:click={generatePreview}
            disabled={!readyToGenPreview || !responseSchema?.name}
          >
            {#if finalPreviewStatus === QueryStatus.PENDING}
              <Spinner size="4" class="mr-2" />
            {:else}
              <CheckSolid size="sm" class="mr-2" />
            {/if}
            Preview transform
          </Button>

          {#if previewProcessingError}
            <div class="text-red-500">
              Error: {previewProcessingError}
            </div>
          {:else if finalPreviewStatus !== QueryStatus.NOT_STARTED && columnPreviewData}
            <div class="flex flex-col gap-4">
              <div class="text-black text-lg font-semibold">
                Transformation Preview
              </div>

              <TransformPreview
                {idColName}
                {targetColName}
                {responseSchema}
                columnData={columnPreviewData}
                bind:resultData={finalPreview}
                queryStatus={finalPreviewStatus}
                allowEdits={false}
              />

              <div class="flex gap-2 items-center w-full">
                <Button
                  class="w-96"
                  on:click={deriveEntireColumn}
                  disabled={!responseSchema?.name}
                >
                  <RocketSolid size="sm" class="mr-2" />

                  Run transformation (will transform {formatInt($filteredCount)}
                  rows)
                </Button>

                {#if commitError}
                  <div class="text-red-500">
                    Error: {commitError}
                  </div>
                {:else if commitResultStatus === QueryStatus.PENDING}
                  <Spinner />
                {:else if commitResultStatus === QueryStatus.COMPLETED}
                  <div class="text-green-500">Completed query!</div>
                {/if}
              </div>
            </div>
          {/if}
        {/if}
      </div>
    {/if}
  {/await}
</Modal>
