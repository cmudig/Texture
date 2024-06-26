<script lang="ts">
  import { onDestroy, onMount, afterUpdate } from "svelte";
  import type * as Monaco from "monaco-editor/esm/vs/editor/editor.api";

  export let currentCode: string;

  // monaco variables
  let monaco: typeof Monaco;
  let editor: Monaco.editor.IStandaloneCodeEditor;
  let editorElement: HTMLDivElement;
  let model: Monaco.editor.ITextModel;

  // styling
  let isFocused = false;

  onMount(async () => {
    monaco = (await import("./monaco")).default;

    editor = monaco.editor.create(editorElement, {
      theme: "vs",
      minimap: {
        enabled: false,
      },
      language: "python",
      automaticLayout: true,
      scrollbar: {
        vertical: "hidden",
      },
      scrollBeyondLastLine: false,
    });
    model = monaco.editor.createModel(currentCode, "python");
    editor.setModel(model);

    editor.onDidChangeModelContent(() => (currentCode = editor.getValue()));
    editor.onDidFocusEditorWidget(() => (isFocused = true));
    editor.onDidBlurEditorWidget(() => (isFocused = false));
  });

  afterUpdate(() => {
    if (model && model?.getValue() !== currentCode) {
      model.setValue(currentCode);
    }
  });

  onDestroy(() => {
    monaco?.editor.getModels().forEach((model) => model.dispose());
    editor?.dispose();
  });
</script>

<div
  class="h-40 w-full border-2 border-gray-300 rounded"
  class:border-primary-500={isFocused}
  bind:this={editorElement}
/>
