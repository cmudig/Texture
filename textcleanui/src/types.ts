export type SliceResult = {
  slice: string;
  base_size: number;
  comp_size: number;
  metric: string;
  base_perf: number | null;
  comp_perf: number | null;
  p_value_corrected: number | null;
  significance: string;
};

export type Metric = {
  name: string;
  max_better: boolean;
};

export type ModelInfo = {
  base_model: string;
  compare_model: string;
  base_performance_overall: number;
  comparison_performance_overall: number;
};

export type DataInput = {
  name: string;
  data: ResultSet;
};

export type ResultSet = {
  metrics: Metric[];
  models: string[];
  results: CompareResult[];
};

export type CompareResult = {
  base_m: string;
  comp_m: string;
  results: SliceResult[];
};
