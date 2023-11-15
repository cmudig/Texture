<script lang="ts">
  import type { DataType } from "../shared/types";

  export let type: DataType;

  function getIcon(type: DataType) {
    switch (type) {
      case "text":
        return "T";
      case "number":
        return "#";
      case "date":
        return "D";
      case "categorical":
        return "C";
    }
  }
</script>

<p class="text-gray-400 font-serif font-medium">
  {getIcon(type)}
</p>
