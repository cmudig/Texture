import type { DatasetInfo } from "./types";

export const datasets: { [key: string]: DatasetInfo } = {
  dolly: {
    name: "dolly",
    filename: "dolly15k.parquet",
    textColumns: ["instruction", "context", "response"],
    metaColumns: ["category"], // in the dataset, not derived
  },
  opus: {
    name: "opus",
    filename: "opus100_en_es.parquet",
    textColumns: ["en", "es"],
  },
  squad: {
    name: "squad",
    filename: "squad_validation.parquet",
    textColumns: ["context", "question", "answers[0]"],
    metaColumns: ["title"], // in the dataset, not derived
  },
};

export const heuristicMetaCols = [
  "text_length",
  "num_words",
  "max_word_length",
  "avg_word_length",
  "perc_special_chars",
];

export const modelMetaCols = [
  "dist_from_mean_embed_all-mpnet-base-v2",
  "outlier_score_ECOD_all-mpnet-base-v2",
  "outlier_score_IForest_all-mpnet-base-v2",
  "dist_from_mean_embed_all-MiniLM-L6-v2",
  "outlier_score_ECOD_all-MiniLM-L6-v2",
  "outlier_score_IForest_all-MiniLM-L6-v2",
  "dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
  "outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
  "outlier_score_IForest_distiluse-base-multilingual-cased-v1",
];
