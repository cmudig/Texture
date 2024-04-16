<script lang="ts">
  import { databaseConnection } from "../../../stores";
  import type { TaskFormat } from "../../../backendapi";

  import { Spinner, Textarea, Button } from "flowbite-svelte";
  import { CheckSolid } from "flowbite-svelte-icons";
  import TransformPreview from "../TransformPreview.svelte";
  import { QueryStatus } from "../../../shared/types";

  const INSTRUCTION = `Describe how you want to transform the column data in a few sentences with as much details as possible.
For example, "Derive 3 - 5 keywords per article"`;

  // PROPS that we only read
  export let targetColName: string;
  export let idColName: string;
  // PROPS that we edit (should use bind)
  export let userPrompt: string;
  export let responseSchema: TaskFormat;
  export let schemaResultStatus: QueryStatus = QueryStatus.NOT_STARTED;
  export let columnExampleData: any[];
  export let exampleResult: any[] | undefined;
  export let setPreviewReady: (status: boolean) => void;

  // need to wait until have prompt with examples
  setPreviewReady(false);

  // LOCALS
  let exampleResultStatus: QueryStatus = QueryStatus.NOT_STARTED;
  let exampleProcessingError;

  // FUNCTIONS
  let schemaEditTimer;
  async function getSchema() {
    schemaResultStatus = QueryStatus.PENDING;

    if (userPrompt) {
      let r = await databaseConnection.api.getLlmResponseFormat(userPrompt);
      responseSchema = r.result as TaskFormat;
      console.log("Schema is: ", responseSchema);
    }
    schemaResultStatus = QueryStatus.COMPLETED;
  }

  async function submitInitialTransformation() {
    exampleResultStatus = QueryStatus.PENDING;
    let r = await databaseConnection.api.getLlmTransformResult({
      userPrompt,
      taskFormat: responseSchema,
      columnData: columnExampleData.map((cd) => cd[targetColName]),
    });

    exampleResultStatus = QueryStatus.COMPLETED;

    if (r.success) {
      exampleProcessingError = undefined;
      exampleResult = r.result as Array<any>;
      setPreviewReady(true);
    } else {
      exampleProcessingError = (r.result as Record<string, unknown>)?.error;
    }
  }

  function deleteResult(index) {
    columnExampleData.splice(index, 1);
    exampleResult?.splice(index, 1);

    columnExampleData = columnExampleData; // trigger reactivity
    exampleResult = exampleResult; // trigger reactivity
  }
</script>

<div class="flex flex-col gap-4">
  <Textarea
    class="min-h-14"
    rows="5"
    placeholder={INSTRUCTION}
    bind:value={userPrompt}
    on:input={() => {
      clearTimeout(schemaEditTimer);
      schemaEditTimer = setTimeout(getSchema, 1000);
    }}
  />

  <Button
    class="w-64 text-white bg-secondary-500 hover:bg-secondary-600 focus-within:ring-secondary-100"
    on:click={submitInitialTransformation}
    disabled={!userPrompt || !responseSchema}
  >
    {#if exampleResultStatus === QueryStatus.PENDING}
      <Spinner size="4" class="mr-2" />
    {:else}
      <CheckSolid size="sm" class="mr-2" />
    {/if}
    Generate example responses
  </Button>

  {#if exampleProcessingError}
    <div class="text-red-500">
      Error: {exampleProcessingError}
    </div>
  {:else if exampleResultStatus !== QueryStatus.NOT_STARTED && columnExampleData}
    <!-- Sample response table -->
    <div class="text-black text-lg font-semibold">Curate Examples</div>

    <TransformPreview
      {idColName}
      {targetColName}
      {responseSchema}
      columnData={columnExampleData}
      bind:resultData={exampleResult}
      queryStatus={exampleResultStatus}
      {deleteResult}
    />
  {/if}
</div>
