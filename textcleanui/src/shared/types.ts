export type DatasetInfo = {
  name: string;
  filename: string;
  metadata: DatasetMetadata;
};

export type DatasetMetadata = {
  text_columns: string[];
  other_columns: string[];
  text_meta_columns: { [key: string]: string[] };
};
