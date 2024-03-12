<script lang="ts">
  import CodeEditor from "./MonacoEditor/CodeEditor.svelte";

  export let setPreviewReady: (status: boolean) => void;
  export let userTransformCode: string | undefined = undefined;

  // TODO in future only set this once ready?
  setPreviewReady(true);
</script>

<div>Add extraction function below:</div>

<CodeEditor bind:currentCode={userTransformCode} />
