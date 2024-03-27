<script lang="ts">
  import {
    WandMagicSparklesOutline,
    CodeOutline,
    FileImportOutline,
  } from "flowbite-svelte-icons";

  export let derived_how: "model" | "code" | undefined | null;
</script>

{#if derived_how === "model"}
  <WandMagicSparklesOutline class="inline" size="sm" />
{:else if derived_how === "code"}
  <CodeOutline class="inline" size="sm" />
{:else}
  <FileImportOutline class="inline" size="sm" />
{/if}
