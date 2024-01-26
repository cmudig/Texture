import { format as isoformat } from "isoformat";

export function formatNumber(value: any, locale = "en", options = {}): string {
  if (value === undefined || value === null) return "null";
  if (value === 0) return "0";

  return value.toLocaleString(locale, options);
}

export function formatFloat(value: any) {
  return formatNumber(value, "en", { maximumFractionDigits: 1 });
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
