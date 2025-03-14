<script lang="ts">
  import {
    databaseConnection,
    datasetSchema,
    filteredIndices,
    filteredCount,
    setSchema,
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
  import { sampleTransforms } from "./CodeTransform/sampleCodeTransforms";

  // props
  export let panelOpen: boolean = false;
  export let finishedCommitHandler: () => void;

  $: textCols = $datasetSchema?.columns.filter((col) => col.type === "text");
  $: allColNames = $datasetSchema?.columns.map((col) => col.name);
  $: idColName = $datasetSchema?.primary_key.name;

  // locals
  let targetColName: string;
  let transformType: "llm" | "code" = "code";
  let initPromise: Promise<void>;

  // example data
  // TODO: make this dynamic becuase if the id is not 0 indexed won't work
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
  let exampleResult: any[] | undefined;
  let userTransformCode: string;

  // preview transform
  let readyToGenPreview = false;
  let columnPreviewData: any[];
  let finalPreviewStatus: QueryStatus = QueryStatus.NOT_STARTED;
  let previewProcessingError;
  let finalPreview: any[] | undefined;

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
        .getValues($datasetSchema.name, idColName, targetColName, example_idxs)
        .then((r) => {
          columnExampleData = r;
        });

      databaseConnection
        .getValues($datasetSchema.name, idColName, targetColName, preview_idxs)
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
        exampleResponse: exampleResult?.map((item) => ({
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

    if (transformType === "llm" && exampleResult) {
      r = await databaseConnection.api.commitLlmTransformResult({
        userPrompt,
        taskFormat: responseSchema,
        columnName: targetColName,
        tableName: $datasetSchema.name,
        exampleData: columnExampleData.map((cd) => cd[targetColName]),
        exampleResponse: exampleResult?.map((item) => ({
          [responseSchema.name]: item,
        })),
        applyToIndices: $filteredIndices,
      });
    } else if (transformType === "code") {
      r = await databaseConnection.api.commitCodeTransformResult({
        codeString: userTransformCode,
        taskFormat: responseSchema,
        columnName: targetColName,
        tableName: $datasetSchema.name,
        applyToIndices: $filteredIndices,
      });
    }

    commitResultStatus = QueryStatus.COMPLETED;
    if (r?.success) {
      console.log("finished with success, calling finish handler");
      commitError = undefined;

      // TODO issue #136: hack to force table reload
      window.location.reload();

      finishedCommitHandler();
      await setSchema();
    } else {
      commitError = r?.result?.error;
    }
  }

  // reset state when modal closes
  function handleModalClose() {
    // if pending query then dont clear
    if (commitResultStatus !== QueryStatus.PENDING) {
      responseSchema = {
        name: "",
        type: TaskFormat.type.STRING,
        num_replies: TaskFormat.num_replies.SINGLE,
      };
      schemaResultStatus = QueryStatus.NOT_STARTED;
      userPrompt = "";
      exampleResult = undefined;
      userTransformCode = sampleTransforms["Empty"].code;
      readyToGenPreview = false;
      finalPreviewStatus = QueryStatus.NOT_STARTED;
      previewProcessingError = undefined;
      finalPreview = undefined;
      commitResultStatus = QueryStatus.NOT_STARTED;
      commitError = undefined;
    }
  }

  $: if (panelOpen && !initPromise) {
    initPromise = init(textCols);
  }
  // error handling
  $: namingErrorExists =
    responseSchema?.name && allColNames.includes(responseSchema.name);
</script>

<Modal
  bind:open={panelOpen}
  title="Derive new column"
  size="xl"
  outsideclose
  on:close={handleModalClose}
>
  {#await initPromise}
    <div class="p-2">
      <Spinner /> Waiting for data...
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
              color={transformType === "code" ? "primary" : "alternative"}
              class="flex items-center text-base gap-2 w-1/2 py-4 rounded-none rounded-tl-lg"
              on:click={() => (transformType = "code")}
            >
              <CodeOutline size="sm" />
              Derive with code
            </Button>

            <Button
              color={transformType === "llm" ? "primary" : "alternative"}
              class="flex items-center text-base gap-2 w-1/2 py-4 rounded-none rounded-tr-lg"
              on:click={() => (transformType = "llm")}
            >
              <WandMagicSparklesOutline size="sm" />
              Derive with LLM
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
                  Column {responseSchema.name} already exists, try another name!
                </div>
              {/if}
            </div>

            <div class:hidden={transformType !== "llm"}>
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
            </div>
            <div class:hidden={transformType !== "code"}>
              <CodeExtract
                {targetColName}
                bind:userTransformCode
                bind:responseSchema
                setPreviewReady={(v) => (readyToGenPreview = v)}
              />
            </div>
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
