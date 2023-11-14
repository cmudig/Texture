<script lang="ts">
  import { heuristicMetaCols, modelMetaCols } from "../shared/colConfig";
  import ChartGroup from "./ChartGroup.svelte";

  export let textColumns: string[];
  export let datasetName: string;
  export let brush: any;
</script>

<div class="border-2 border-slate-50">
  <div>
    <h2 class="font-bold">Joint</h2>
    <div class="ml-4">
      <ChartGroup
        groupName={"Model"}
        colNames={modelMetaCols.map((m) => `joint_${m}`)}
        {datasetName}
        {brush}
      />
    </div>
  </div>

  {#each textColumns as colName}
    <div>
      <h2 class="font-bold">{colName}</h2>
      <div class="ml-4">
        <ChartGroup
          groupName={"Model"}
          colNames={modelMetaCols.map((m) => `${colName}_${m}`)}
          {datasetName}
          {brush}
        />
        <ChartGroup
          groupName={"Heuristic"}
          colNames={heuristicMetaCols.map((m) => `${colName}_${m}`)}
          {datasetName}
          {brush}
        />
      </div>
    </div>
  {/each}
</div>
