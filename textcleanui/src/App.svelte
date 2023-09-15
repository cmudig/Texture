<script lang="ts">
  import type { DatabaseConnection } from "./database/loader";
  import * as vg from "@uwdata/vgplot";
  import DistSidebar from "./components/DistSidebar.svelte";
  import InstanceView from "./components/InstanceView.svelte";

  export let dbConnection: DatabaseConnection;

  // export default vg.plot(
  //   vg.line(vg.from("aapl"), { x: "Date", y: "Close" }),
  //   vg.width(680),
  //   vg.height(200)
  // );

  let datasetName = "opus100_en_es";
  // let dRef = dbConnection.loadDataset(datasetName);
</script>

<div class="bg-gradient-to-r from-blue-100 to-blue-700 dark:bg-sky-950 p-5">
  <span
    class="self-center whitespace-nowrap text-2xl font-semibold text-blue-900 dark:text-white"
    >Text Clean</span
  >
</div>

<!-- <div class="flex">
  <div class="w-1/4">
    <DistSidebar />
  </div>
  <div class="w-3/4">
    <InstanceView />
  </div>
</div> -->

<!-- <div>
  {#await dRef}
    <p>loading...</p>
  {:then d}
    <p>Loaded dataset: {datasetName}</p>
    {vg.table({
      from: datasetName,
      columns: ["en", "es"],
      width: { en: 200, es: 200 },
      height: 500,
    })}
  {/await}
</div> -->

<div>
  <p>Loaded dataset: {datasetName}</p>
  <!-- {vg.table({
    from: datasetName,
    columns: ["en", "es"],
    width: { en: 200, es: 200 },
    height: 500,
  })} -->
</div>
