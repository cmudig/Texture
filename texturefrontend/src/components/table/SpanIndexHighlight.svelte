<script lang="ts">
  export let value: any;
  export let highlights: any[]; // {id, span_start, span_end, word}

  function processText(value: string, highlights) {
    let result = "";
    let lastIndex = 0;

    // sort might not be necessary if sorted in query
    highlights.sort((a, b) => a.span_start - b.span_start);

    highlights.forEach(({ span_start, span_end, word }) => {
      result += value.substring(lastIndex, span_start);
      result += `<span class="bg-highlight-300">${word}</span>`;
      lastIndex = span_end;
    });

    result += value.substring(lastIndex);

    return result;
  }

  $: processedText = processText(String(value), highlights);
</script>

<span>{@html processedText}</span>
