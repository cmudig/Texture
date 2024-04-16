<script lang="ts">
  export let num = 1;
</script>

<div role="status" class="space-y-2.5 animate-pulse max-w-lg">
  {#each Array(num) as _}
    <div class="flex items-center w-full">
      <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-32"></div>
      <div
        class="h-2.5 ms-2 bg-gray-300 rounded-full dark:bg-gray-600 w-24"
      ></div>
      <div
        class="h-2.5 ms-2 bg-gray-300 rounded-full dark:bg-gray-600 w-full"
      ></div>
    </div>
    <div class="flex items-center w-full max-w-[480px]">
      <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-full"></div>
      <div
        class="h-2.5 ms-2 bg-gray-300 rounded-full dark:bg-gray-600 w-full"
      ></div>
      <div
        class="h-2.5 ms-2 bg-gray-300 rounded-full dark:bg-gray-600 w-24"
      ></div>
    </div>
  {/each}
</div>
