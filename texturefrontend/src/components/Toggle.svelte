<script lang="ts">
  export let active = true;
</script>

<div>
  <button
    class="space-between flex gap-2 h-9 w-full items-center justify-between px-2 hover:bg-gray-200 border-t-2 border-secondary-200"
    on:click={() => {
      active = !active;
    }}
  >
    <slot name="title" />
  </button>

  <div class="w-full pl-4 pr-2 mb-2" class:hidden={!active}>
    <slot name="body" />
  </div>
</div>
