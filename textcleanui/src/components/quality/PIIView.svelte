<script lang="ts">
  import type { Column } from "../../shared/types";
  import Histogram from "../charts/Histogram.svelte";

  export let pii_col: Column;
</script>

<div class="flex flex-col gap-1">
  <p>Num PII detected</p>
  <div class="pl-4">
    <Histogram columnName={pii_col.name} />
  </div>
</div>
