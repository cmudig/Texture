<script lang="ts">
  import { formatNumber } from "../shared/format";
  import { filteredCount } from "../stores";
  import FilterBar from "./FilterBar.svelte";

  export let datasetSize;
</script>

<div class="grow self-center">
  <FilterBar />
</div>
<div class="text-md self-center">
  {formatNumber($filteredCount)} / {formatNumber(datasetSize)} rows
</div>
