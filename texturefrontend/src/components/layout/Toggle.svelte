<script lang="ts">
  export let active = true;
  export let showTopBorder = true;
</script>

<div>
  <button
    class={`flex gap-2 min-h-9 w-full items-center px-2 hover:bg-gray-200 ${showTopBorder ? "border-t-2 border-secondary-200" : ""}`}
    on:click={() => {
      active = !active;
    }}
  >
    <slot name="title" />
  </button>

  <div class="w-full px-2 mb-2" class:hidden={!active}>
    <slot name="body" />
  </div>
</div>
