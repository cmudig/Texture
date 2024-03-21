<script lang="ts">
  import { Button } from "flowbite-svelte";
  import { PlusSolid } from "flowbite-svelte-icons";
  import { formatNumber } from "../shared/format";
  import { filteredCount } from "../stores";
  import FilterBar from "./FilterBar.svelte";

  export let showAddColModal;
  export let datasetSize;
</script>

<Button class="shrink-0" on:click={() => (showAddColModal = true)} size="sm">
  <PlusSolid size="sm" class="mr-2" />
  Derive Column
</Button>
<div class="grow px-2 self-center">
  <FilterBar />
</div>
<div class="text-md self-center">
  {formatNumber($filteredCount)} / {formatNumber(datasetSize)} rows
</div>
