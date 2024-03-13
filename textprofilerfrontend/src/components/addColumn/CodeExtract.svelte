<script lang="ts">
  import { Button } from "flowbite-svelte";

  import CodeEditor from "./MonacoEditor/CodeEditor.svelte";
  import { sampleTransforms } from "./sampleCodeTransforms";

  export let setPreviewReady: (status: boolean) => void;
  export let userTransformCode: string | undefined = undefined;

  // TODO in future only set this once ready?
  setPreviewReady(true);
</script>

<div class="flex gap-2 items-center">
  Transform templates:
  {#each Object.keys(sampleTransforms) as transformName}
    <Button
      on:click={() => {
        console.log("Setting code to: ", sampleTransforms[transformName]);
        userTransformCode = sampleTransforms[transformName];
      }}
      color="alternative"
      size="xs"
      class="text-gray-500"
    >
      {transformName}
    </Button>
  {/each}
</div>

<CodeEditor bind:currentCode={userTransformCode} />
