import { format as isoformat } from "isoformat";

export function formatNumber(value: any, locale = "en"): string {
  if (value === undefined || value === null) return "null";
  if (value === 0) return "0";

  return value.toLocaleString(locale);
}

export function formatLocaleAuto(value: any, locale = "en") {
  if (value === undefined || value === null) return "null";
  if (typeof value === "number") return formatNumber(value, locale);
  if (value instanceof Date) return formatDate(value);
  return `${value}`;
}

export function formatDate(date: any): string {
  return isoformat(date, "Invalid Date");
}
