// Front end only types

export type FilterWrapper = {
  brush: any;
  datasetName: string;
};

export type SelectionMap = {
  [key: string]: SelectionRange;
};

export type SelectionRange = number[] | string[];

// this is format from `summarize tablename` in duckdb
export type ColumnSummary = {
  column_name: string;
  column_type: string;
  min: string;
  max: string;
  approx_unique: string;
  avg?: string;
  std?: string;
  q25?: string;
  q50?: string;
  q75?: string;
  count: number;
  null_percentage: string;
};
