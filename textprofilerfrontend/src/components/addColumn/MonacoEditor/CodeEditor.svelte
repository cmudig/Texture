<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import type * as Monaco from "monaco-editor/esm/vs/editor/editor.api";

  //   const initialPythonCode = `import pandas as pd

  // def transform(col: pd.Series) -> pd.Series:
  //   # do transformation here and return a series or array
  //   pass
  // `;

  const initialPythonCode = `import pandas as pd

# length (in characters)
def transform(col: pd.Series):
  return col.str.len()
`;

  export let currentCode: string = initialPythonCode;

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

  onDestroy(() => {
    monaco?.editor.getModels().forEach((model) => model.dispose());
    editor?.dispose();
  });
</script>

<div
  class="h-48 w-full border-2 border-gray-300 rounded"
  class:border-primary-500={isFocused}
  bind:this={editorElement}
/>
