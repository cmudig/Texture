<script lang="ts">
  import CodeEditor from "./MonacoEditor/CodeEditor.svelte";

  let userTransformCode: string;
</script>

<div>Add extraction function below:</div>

<CodeEditor bind:currentCode={userTransformCode} />
