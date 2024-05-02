<script lang="ts">
  /**
   * SubstringHighlight.svelte
   * Given a value string and an array of highlights, will highlight every
   * intance of the highlights in the value string by matching substrings.
   */
  export let value: any;
  export let highlights: any[];

  console.log("substring highlight");

  type AnnotatedSpan = {
    span: string;
    included: boolean;
  };

  function annotateSpans(
    _value: string,
    _highlights: string[],
  ): AnnotatedSpan[] {
    if (_highlights.length > 0) {
      // ' gets escaped as '' in SQL, so we need to unescape it
      _highlights = _highlights.map((v) => v.replaceAll("''", "'"));
    }
    let annotatedSpans: AnnotatedSpan[] = [];
    let lastIndex = 0;

    // Function to add a new span
    const addSpan = (endIndex: number, included: boolean) => {
      if (lastIndex !== endIndex) {
        annotatedSpans.push({
          span: _value.substring(lastIndex, endIndex),
          included: included,
        });
        lastIndex = endIndex;
      }
    };

    for (let i = 0; i < _value.length; ) {
      let foundHighlight = false;

      // Check each highlight
      for (const highlight of _highlights) {
        if (_value.startsWith(highlight, i)) {
          // Add non-highlighted part
          addSpan(i, false);

          // Add highlighted part
          addSpan(i + highlight.length, true);

          // Move the index
          i += highlight.length;
          foundHighlight = true;
          break;
        }
      }

      // If no highlight found, move to the next character
      if (!foundHighlight) {
        i++;
      }
    }

    // Add any remaining part of the string
    addSpan(value.length, false);

    return annotatedSpans;
  }

  $: annotatedSpans = annotateSpans(value, highlights);
</script>

<!-- TODO: use different colors for different highlights? -->
<span class="whitespace-pre-wrap">
  {#each annotatedSpans as s}
    {#if s.included}
      <span class="bg-highlight-300">{s.span}</span>
    {:else}
      {s.span}
    {/if}
  {/each}
</span>
