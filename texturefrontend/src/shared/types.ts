// Front end only types

export type SelectionMap = {
  [key: string]: SelectionRange;
};

export type SelectionRange = string[] | number[] | boolean[];

// Type guard for number array
export function isNumberArray(
  selectionRange: SelectionRange,
): selectionRange is number[] {
  return selectionRange.length === 0 || typeof selectionRange[0] === "number";
}

// Type guard for string array
export function isStringArray(
  selectionRange: SelectionRange,
): selectionRange is string[] {
  return selectionRange.length === 0 || typeof selectionRange[0] === "string";
}

// Type guard for boolean array
export function isBoolArray(
  selectionRange: SelectionRange,
): selectionRange is boolean[] {
  return selectionRange.length === 0 || typeof selectionRange[0] === "boolean";
}

// this is format from `summarize tablename` in duckdb
export type ColumnSummary = {
  column_name: string;
  column_type: string;
  min: string;
  max: string;
  approx_unique: string; // this value is always wrong from duckdb
  avg?: string;
  std?: string;
  q25?: string;
  q50?: string;
  q75?: string;
  count: number;
  null_percentage: string;
  cardinality: number; // plus extra field
};

export enum QueryStatus {
  NOT_STARTED = 0,
  PENDING = 1,
  COMPLETED = 2,
}
