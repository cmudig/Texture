import { v4 as uuidv4 } from "uuid";

export function formatNumber(value: number | undefined) {
  if (value != undefined) {
    return value.toLocaleString("en-US", { maximumFractionDigits: 1 });
  }
  return value;
}

export function getUUID() {
  return uuidv4();
}
