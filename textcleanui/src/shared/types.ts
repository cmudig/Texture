export type DatasetInfo = {
  name: string;
  filename: string;
  metadata: DatasetMetadata;
};

export type DatasetMetadata = {
  text_columns: Column[];
  other_columns: Column[];
  text_meta_columns: { [key: string]: Column[] };
  text_quality_info?: QualityInfo[];
};

export type QualityInfo = {
  type: string;
  text_column: Column;
  plot_columns?: Column[];
};

export type DataType = "text" | "number" | "date" | "categorical";

export type Column = {
  name: string;
  type: DataType;
};

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
