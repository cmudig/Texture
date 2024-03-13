<script lang="ts">
  import { Button } from "flowbite-svelte";
  import type { TaskFormat } from "../../../backendapi";
  import CodeEditor from "./CodeEditor.svelte";
  import { sampleTransforms } from "./sampleCodeTransforms";

  export let setPreviewReady: (status: boolean) => void;
  export let targetColName: string;
  export let responseSchema: TaskFormat;
  export let userTransformCode: string = sampleTransforms["Empty"].code;

  setPreviewReady(true);
</script>

<div class="flex flex-col gap-2">
  <div class="flex gap-2 items-center overflow-x-auto flex-nowrap">
    Templates:
    {#each Object.keys(sampleTransforms) as transformName}
      <Button
        on:click={() => {
          userTransformCode = sampleTransforms[transformName].code;
          let m = sampleTransforms[transformName].schema;
          responseSchema = { ...m, name: `${targetColName}_${m.name}` };
        }}
        size="xs"
        class="text-white bg-blue-500 hover:bg-blue-600 focus-within:ring-blue-100 shrink-0"
      >
        {transformName}
      </Button>
    {/each}
  </div>

  <CodeEditor bind:currentCode={userTransformCode} />
</div>
