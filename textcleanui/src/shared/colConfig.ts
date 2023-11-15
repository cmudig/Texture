import type { DatasetInfo } from "./types";

// TODO: in the future this will be stored server side and fetched

export const datasets: { [key: string]: DatasetInfo } = {
  dolly: {
    name: "dolly",
    filename: "dolly15k.parquet",
    metadata: {
      text_columns: [
        { name: "instruction", type: "text" },
        { name: "context", type: "text" },
        { name: "response", type: "text" },
      ],
      other_columns: [{ name: "category", type: "categorical" }],
      text_meta_columns: {
        instruction: [
          { name: "instruction_text_length", type: "number" },
          { name: "instruction_num_words", type: "number" },
          { name: "instruction_max_word_length", type: "number" },
          { name: "instruction_avg_word_length", type: "number" },
          { name: "instruction_perc_special_chars", type: "number" },
          {
            name: "instruction_dist_from_mean_embed_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "instruction_outlier_score_ECOD_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "instruction_outlier_score_IForest_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "instruction_dist_from_mean_embed_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "instruction_outlier_score_ECOD_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "instruction_outlier_score_IForest_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "instruction_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "instruction_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "instruction_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
        ],
        context: [
          { name: "context_text_length", type: "number" },
          { name: "context_num_words", type: "number" },
          { name: "context_max_word_length", type: "number" },
          { name: "context_avg_word_length", type: "number" },
          { name: "context_perc_special_chars", type: "number" },
          {
            name: "context_dist_from_mean_embed_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "context_outlier_score_ECOD_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "context_outlier_score_IForest_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "context_dist_from_mean_embed_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "context_outlier_score_ECOD_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "context_outlier_score_IForest_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "context_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "context_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "context_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
        ],
        response: [
          { name: "response_text_length", type: "number" },
          { name: "response_num_words", type: "number" },
          { name: "response_max_word_length", type: "number" },
          { name: "response_avg_word_length", type: "number" },
          { name: "response_perc_special_chars", type: "number" },
          {
            name: "response_dist_from_mean_embed_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "response_outlier_score_ECOD_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "response_outlier_score_IForest_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "response_dist_from_mean_embed_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "response_outlier_score_ECOD_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "response_outlier_score_IForest_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "response_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "response_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "response_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
        ],
      },
    },
  },
  opus: {
    name: "opus",
    filename: "opus100_en_es.parquet",
    metadata: {
      text_columns: [
        { name: "en", type: "text" },
        { name: "es", type: "text" },
      ],
      other_columns: [],
      text_meta_columns: {
        en: [
          { name: "en_text_length", type: "number" },
          { name: "en_num_words", type: "number" },
          { name: "en_max_word_length", type: "number" },
          { name: "en_avg_word_length", type: "number" },
          { name: "en_perc_special_chars", type: "number" },
          { name: "en_dist_from_mean_embed_all-mpnet-base-v2", type: "number" },
          { name: "en_outlier_score_ECOD_all-mpnet-base-v2", type: "number" },
          {
            name: "en_outlier_score_IForest_all-mpnet-base-v2",
            type: "number",
          },
          { name: "en_dist_from_mean_embed_all-MiniLM-L6-v2", type: "number" },
          { name: "en_outlier_score_ECOD_all-MiniLM-L6-v2", type: "number" },
          { name: "en_outlier_score_IForest_all-MiniLM-L6-v2", type: "number" },
          {
            name: "en_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "en_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "en_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
        ],
        es: [
          { name: "es_text_length", type: "number" },
          { name: "es_num_words", type: "number" },
          { name: "es_max_word_length", type: "number" },
          { name: "es_avg_word_length", type: "number" },
          { name: "es_perc_special_chars", type: "number" },
          { name: "es_dist_from_mean_embed_all-mpnet-base-v2", type: "number" },
          { name: "es_outlier_score_ECOD_all-mpnet-base-v2", type: "number" },
          {
            name: "es_outlier_score_IForest_all-mpnet-base-v2",
            type: "number",
          },
          { name: "es_dist_from_mean_embed_all-MiniLM-L6-v2", type: "number" },
          { name: "es_outlier_score_ECOD_all-MiniLM-L6-v2", type: "number" },
          { name: "es_outlier_score_IForest_all-MiniLM-L6-v2", type: "number" },
          {
            name: "es_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "es_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "es_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
        ],
      },
    },
  },
  squad: {
    name: "squad",
    filename: "squad_validation.parquet",
    metadata: {
      text_columns: [
        { name: "context", type: "text" },
        { name: "question", type: "text" },
        { name: "answers[0]", type: "text" },
      ],
      other_columns: [{ name: "title", type: "categorical" }],
      text_meta_columns: {
        context: [
          { name: "context_text_length", type: "number" },
          { name: "context_num_words", type: "number" },
          { name: "context_max_word_length", type: "number" },
          { name: "context_avg_word_length", type: "number" },
          { name: "context_perc_special_chars", type: "number" },
          {
            name: "context_dist_from_mean_embed_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "context_outlier_score_ECOD_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "context_outlier_score_IForest_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "context_dist_from_mean_embed_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "context_outlier_score_ECOD_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "context_outlier_score_IForest_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "context_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "context_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "context_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
        ],
        question: [
          { name: "question_text_length", type: "number" },
          { name: "question_num_words", type: "number" },
          { name: "question_max_word_length", type: "number" },
          { name: "question_avg_word_length", type: "number" },
          { name: "question_perc_special_chars", type: "number" },
          {
            name: "question_dist_from_mean_embed_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "question_outlier_score_ECOD_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "question_outlier_score_IForest_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "question_dist_from_mean_embed_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "question_outlier_score_ECOD_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "question_outlier_score_IForest_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "question_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "question_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "question_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
        ],
        "answers[0]": [
          { name: "answers[0]_text_length", type: "number" },
          { name: "answers[0]_num_words", type: "number" },
          { name: "answers[0]_max_word_length", type: "number" },
          { name: "answers[0]_avg_word_length", type: "number" },
          { name: "answers[0]_perc_special_chars", type: "number" },
          {
            name: "answers[0]_dist_from_mean_embed_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "answers[0]_outlier_score_ECOD_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "answers[0]_outlier_score_IForest_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "answers[0]_dist_from_mean_embed_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "answers[0]_outlier_score_ECOD_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "answers[0]_outlier_score_IForest_all-MiniLM-L6-v2",
            type: "number",
          },
          {
            name: "answers[0]_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "answers[0]_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
          {
            name: "answers[0]_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            type: "number",
          },
        ],
      },
    },
  },
  vast2021: {
    name: "vast2021",
    filename: "vast2021.parquet",
    metadata: {
      text_columns: [{ name: "message", type: "text" }],
      other_columns: [
        { name: "type", type: "categorical" },
        { name: "date(yyyyMMddHHmmss)", type: "number" },
        { name: "author", type: "categorical" },
        { name: "latitude", type: "number" },
        { name: "longitude", type: "number" },
        { name: "location", type: "categorical" },
        { name: "date", type: "date" },
      ],
      text_meta_columns: {
        message: [
          { name: "message_text_length", type: "number" },
          { name: "message_num_words", type: "number" },
          { name: "message_max_word_length", type: "number" },
          { name: "message_avg_word_length", type: "number" },
          { name: "message_perc_special_chars", type: "number" },
          {
            name: "message_dist_from_mean_embed_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "message_outlier_score_ECOD_all-mpnet-base-v2",
            type: "number",
          },
          {
            name: "message_outlier_score_IForest_all-mpnet-base-v2",
            type: "number",
          },
        ],
      },
    },
  },
};
