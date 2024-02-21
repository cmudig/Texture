<script lang="ts">
  import { stopwords } from "../../shared/stopwords";
  import { Textarea, Button } from "flowbite-svelte";

  let isOpen: boolean = false;
  let _excludedWords = $stopwords.join(" ");

  function saveEdits() {
    $stopwords = _excludedWords
      .split(" ")
      .map((word) => word.trim())
      .filter((word) => word !== "");
  }

  function handleToggle() {
    if (isOpen) {
      saveEdits();
    }
    isOpen = !isOpen;
  }
</script>

<div class="flex flex-col gap-2">
  <Button on:click={handleToggle} size="sm">
    {#if isOpen}
      Done
    {:else}
      Edit Stopwords
    {/if}
  </Button>
  {#if isOpen}
    <Textarea
      class="min-h-20"
      bind:value={_excludedWords}
      placeholder="Enter stopwords separated by space."
      rows="15"
      on:change={saveEdits}
    />
  {/if}
</div>
