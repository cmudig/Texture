<script lang="ts">
  import DistSidebar from "./lib/DistSidebar.svelte";
  import InstanceView from "./lib/InstanceView.svelte";
</script>

<div class="bg-gradient-to-r from-blue-100 to-blue-700 dark:bg-sky-950 p-5">
  <span
    class="self-center whitespace-nowrap text-2xl font-semibold text-blue-900 dark:text-white"
    >Text Clean</span
  >
</div>

<div class="flex">
  <div class="w-1/4">
    <DistSidebar />
  </div>
  <div class="w-3/4">
    <InstanceView />
  </div>
</div>
