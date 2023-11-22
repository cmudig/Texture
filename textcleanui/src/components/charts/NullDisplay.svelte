<script lang="ts">
  export let nullPercentage: number; // number from 0 to 100 with % of column that is NULL

  const normalColor = "rgb(156 163 175)"; // gray-400
  const warningColor = "rgb(251 146 60)"; // orange-600
  const badColor = "rgb(220 38 38)"; // red-600

  function getColor(nullPerc: number) {
    if (nullPerc === 0) {
      return normalColor;
    } else if (nullPerc < 50) {
      return warningColor;
    }
    return badColor;
  }

  $: textColor = getColor(nullPercentage);

  let size = 22;
  let strokeWidth = 3;
  let radius = size / 2 - strokeWidth / 2;
  let circumference = 2 * Math.PI * radius;
  // min nullPercntage at 1 so still draws a small mark for 0% null
  $: offset = circumference * ((100 - Math.max(nullPercentage, 1)) / 100);
</script>

<svg width={size} height={size}>
  <g transform={`rotate(90 ${size / 2} ${size / 2})`}>
    <circle
      cx={size / 2}
      cy={size / 2}
      r={radius}
      fill="none"
      stroke={textColor}
      stroke-width={strokeWidth}
      stroke-dasharray={circumference}
      stroke-dashoffset={offset}
      stroke-linecap="round"
    />
  </g>

  <text
    fill={textColor}
    x="50%"
    y="50%"
    dominant-baseline="central"
    font-size="8"
    text-anchor="middle"
  >
    {nullPercentage.toFixed(0)}
  </text>
</svg>
