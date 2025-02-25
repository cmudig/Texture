<script lang="ts">
  export let minWidth: number | null = null;
  export let maxWidth: number | null = null;
  export let width: number = 100;

  let isHovering = false;

  let lastX: number | null = null;
  let lastY: number | null = null;
  let draggingDirection: string | null = null;

  function onMousedown(e: PointerEvent, direction: string) {
    lastX = e.pageX;
    lastY = e.pageY;
    draggingDirection = direction;
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
  }

  function onMousemove(e: PointerEvent) {
    if (draggingDirection === null) return;
    let xDelta = e.pageX - lastX!;
    let yDelta = e.pageY - lastY!;
    if (draggingDirection == "left") width = (width as number) - xDelta;
    else if (draggingDirection == "right") width = (width as number) + xDelta;

    lastX = e.pageX;
    lastY = e.pageY;
  }

  function onMouseup() {
    lastX = null;
    lastY = null;
    draggingDirection = null;
  }

  let maxWidthStyle: string = "";
  let minWidthStyle: string = "";
  $: minWidthStyle = minWidth === null ? "" : `min-width: ${minWidth}px;`;
  $: maxWidthStyle = maxWidth === null ? "" : `max-width: ${maxWidth}px;`;
  $: widthStyle = `width: ${width}px;`;
</script>

<div
  class="relative border-gray-300 grow-0 shrink-0 border-r-2"
  style="{minWidthStyle} {maxWidthStyle} {widthStyle}"
  class:border-gray-400={isHovering}
>
  <slot />

  <div
    class="absolute inset-y-0 -right-2 top-0 z-10 w-4 h-full cursor-col-resize pointer-events-auto"
    on:pointerdown|preventDefault={(e) => onMousedown(e, "right")}
    on:pointermove|preventDefault={onMousemove}
    on:pointerup|preventDefault={onMouseup}
    on:pointerover|preventDefault={() => (isHovering = true)}
    on:pointerout|preventDefault={() => (isHovering = false)}
  ></div>
</div>
