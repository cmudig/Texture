export function formatNumber(value: number | undefined) {
  if (value != undefined) {
    return value.toLocaleString("en-US", { maximumFractionDigits: 1 });
  }
  return value;
}
