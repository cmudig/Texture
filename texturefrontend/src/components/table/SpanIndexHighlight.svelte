<script lang="ts">
  export let value: any;
  export let highlights: any[]; // {id, span_start, span_end}

  // Escape HTML characters
  function escapeHTML(str: string) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // run tagging pipeline
  function runProcess(input_string, highlight_array) {
    const numericHighlights = highlight_array.map((v) => ({
      span_start: Number(v.span_start),
      span_end: Number(v.span_end),
    }));
    const mergedHighlights = mergeHighlights(numericHighlights);
    return tagSpans(String(input_string), mergedHighlights);
  }

  // merge overlapping or duplicate highlights
  function mergeHighlights(
    highlights: { span_start: number; span_end: number }[],
  ): { span_start: number; span_end: number }[] {
    const sortedHighlights = highlights.sort(
      (a, b) => a.span_start - b.span_start || a.span_end - b.span_end,
    );
    const merged: { span_start: number; span_end: number }[] = [];
    for (const { span_start, span_end } of sortedHighlights) {
      // If merged array is empty or current range does not overlap with the last one, add it
      if (
        merged.length === 0 ||
        merged[merged.length - 1].span_end < span_start
      ) {
        merged.push({ span_start, span_end });
      } else {
        // Otherwise, merge the current range with the last one
        merged[merged.length - 1].span_end = Math.max(
          merged[merged.length - 1].span_end,
          span_end,
        );
      }
    }

    return merged;
  }

  // generate tagged spans
  function tagSpans(value: string, highlights) {
    let result = "";
    let lastIndex = 0;

    highlights.forEach(({ span_start, span_end }) => {
      result += escapeHTML(value.substring(lastIndex, span_start));
      const match = escapeHTML(value.substring(span_start, span_end));
      result += `<span class="bg-highlight-300">${match}</span>`;
      lastIndex = span_end;
    });

    result += escapeHTML(value.substring(lastIndex));
    return result;
  }

  $: processedText = runProcess(value, highlights);
</script>

<span class="whitespace-pre-wrap">{@html processedText}</span>
