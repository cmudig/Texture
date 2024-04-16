<script lang="ts">
  import { TextPlaceholder } from "flowbite-svelte";

  export let num = 3;
</script>

<div class="flex flex-col">
  {#each Array(num) as _, i}
    <TextPlaceholder size="xl" class="mb-4" />
  {/each}
</div>
