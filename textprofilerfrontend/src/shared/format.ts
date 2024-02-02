import { format as isoformat } from "isoformat";

type NumberOptions = {
  range?: any;
  locale?: string;
  [key: string]: any;
};

export function formatNumber(value: any, options: NumberOptions = {}): string {
  const { range, locale = "en-US" } = options;

  if (value == undefined || Number.isNaN(value)) return "null";
  // cast for BigInt etc
  value = Number(value);
  if (value === 0) return "0";

  if (Math.abs(value) >= 1) {
    if (Math.abs(range) > 10) {
      return value.toLocaleString(locale, {
        maximumFractionDigits: 0,
        ...options,
      });
    }

    return value.toLocaleString(locale, {
      maximumFractionDigits: 1,
      ...options,
    });
  }

  return value.toLocaleString(locale, {
    maximumSignificantDigits: 2,
    ...options,
  });
}

export function formatDate(date: any): string {
  return isoformat(date, "Invalid Date");
}

type FormatOptions = {
  type?: string;
  locale?: string;
  [key: string]: any;
};

export function formatValue(value: any, options: FormatOptions = {}) {
  const { type, ...otherOptions } = options;

  if (value === undefined || value === null) return "null";
  if (type === "number" || typeof value === "number")
    return formatNumber(value, otherOptions);
  if (type === "date" || value instanceof Date) return formatDate(value);

  return `${value}`;
}
