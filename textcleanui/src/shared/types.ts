export type DatasetInfo = {
  name: string;
  filename: string;
  metadata: DatasetMetadata;
};

export type DatasetMetadata = {
  text_columns: Column[];
  other_columns: Column[];
  text_meta_columns: { [key: string]: Column[] };
};

export type DataType = "text" | "number" | "date" | "categorical";

export type Column = {
  name: string;
  type: DataType;
};

export type TableOption = "all" | "text";
