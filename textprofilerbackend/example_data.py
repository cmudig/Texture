from textprofilerbackend.models import DatasetInfo


dataset_vast2021 = DatasetInfo(
    name="vast2021",
    joinDatasetInfo={
        "joinDatasetName": "vast2021_word",
        "joinKey": "id",
        "joinColumn": {
            "name": "word",
            "type": "text",
            "associated_text_col_name": "message",
        },
    },
    origin="example",
    column_info=[
        {"name": "message", "type": "text"},
        # dataset metadata
        {"name": "type", "type": "categorical"},
        # {"name": "date(yyyyMMddHHmmss)", "type": "number"},
        {"name": "author", "type": "categorical"},
        {"name": "latitude", "type": "number"},
        {"name": "longitude", "type": "number"},
        {"name": "location", "type": "categorical"},
        # derived metadata for message
        {"name": "date", "type": "date"},
        {
            "name": "message_text_length",
            "type": "number",
            "associated_text_col_name": "message",
        },
        {
            "name": "message_num_words",
            "type": "number",
            "associated_text_col_name": "message",
        },
        {
            "name": "message_max_word_length",
            "type": "number",
            "associated_text_col_name": "message",
        },
        {
            "name": "message_avg_word_length",
            "type": "number",
            "associated_text_col_name": "message",
        },
        {
            "name": "message_perc_special_chars",
            "type": "number",
            "associated_text_col_name": "message",
        },
        {
            "name": "message_dist_from_mean_embed_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "message",
        },
        {
            "name": "message_outlier_score_ECOD_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "message",
        },
        {
            "name": "message_outlier_score_IForest_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "message",
        },
        # quality metadata
        # {
        #     "name": "message_cluster_id_comm",
        #     "type": "categorical",
        #     "associated_text_col_name": "message",
        # },
        # {
        #     "name": "message_cluster_id_hdb",
        #     "type": "categorical",
        #     "associated_text_col_name": "message",
        # },
        # {
        #     "name": "message_pii_count",
        #     "type": "number",
        #     "associated_text_col_name": "message",
        # },
    ],
)


dataset_dolly = DatasetInfo(
    name="dolly",
    origin="example",
    column_info=[
        # text columns
        {"name": "instruction", "type": "text"},
        {"name": "context", "type": "text"},
        {"name": "response", "type": "text"},
        # dataset metadata
        {"name": "category", "type": "categorical"},
        # derived metadata
        {
            "name": "instruction_text_length",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_num_words",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_max_word_length",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_avg_word_length",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_perc_special_chars",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_dist_from_mean_embed_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_outlier_score_ECOD_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_outlier_score_IForest_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_dist_from_mean_embed_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_outlier_score_ECOD_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_outlier_score_IForest_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "instruction_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "instruction",
        },
        {
            "name": "context_text_length",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_num_words",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_max_word_length",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_avg_word_length",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_perc_special_chars",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_dist_from_mean_embed_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_ECOD_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_IForest_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_dist_from_mean_embed_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_ECOD_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_IForest_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "response_text_length",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_num_words",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_max_word_length",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_avg_word_length",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_perc_special_chars",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_dist_from_mean_embed_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_outlier_score_ECOD_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_outlier_score_IForest_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_dist_from_mean_embed_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_outlier_score_ECOD_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_outlier_score_IForest_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "response",
        },
        {
            "name": "response_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "response",
        },
    ],
)

dataset_opus = DatasetInfo(
    name="opus",
    origin="example",
    column_info=[
        # text columns
        {"name": "en", "type": "text"},
        {"name": "es", "type": "text"},
        # derived metadata
        {
            "name": "en_text_length",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_num_words",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_max_word_length",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_avg_word_length",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_perc_special_chars",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_dist_from_mean_embed_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_outlier_score_ECOD_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_outlier_score_IForest_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_dist_from_mean_embed_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_outlier_score_ECOD_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_outlier_score_IForest_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "en_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "en",
        },
        {
            "name": "es_text_length",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_num_words",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_max_word_length",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_avg_word_length",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_perc_special_chars",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_dist_from_mean_embed_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_outlier_score_ECOD_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_outlier_score_IForest_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_dist_from_mean_embed_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_outlier_score_ECOD_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_outlier_score_IForest_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "es",
        },
        {
            "name": "es_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "es",
        },
    ],
)

dataset_squad = DatasetInfo(
    name="squad",
    origin="example",
    column_info=[
        # text columns
        {"name": "context", "type": "text"},
        {"name": "question", "type": "text"},
        {"name": "answers[0]", "type": "text"},
        # dataset metadata
        {"name": "title", "type": "categorical"},
        # derived metadata
        {
            "name": "context_text_length",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_num_words",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_max_word_length",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_avg_word_length",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_perc_special_chars",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_dist_from_mean_embed_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_ECOD_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_IForest_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_dist_from_mean_embed_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_ECOD_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_IForest_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "context_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "context",
        },
        {
            "name": "question_text_length",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_num_words",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_max_word_length",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_avg_word_length",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_perc_special_chars",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_dist_from_mean_embed_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_outlier_score_ECOD_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_outlier_score_IForest_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_dist_from_mean_embed_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_outlier_score_ECOD_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_outlier_score_IForest_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "question_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "question",
        },
        {
            "name": "answers[0]_text_length",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_num_words",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_max_word_length",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_avg_word_length",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_perc_special_chars",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_dist_from_mean_embed_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_outlier_score_ECOD_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_outlier_score_IForest_all-mpnet-base-v2",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_dist_from_mean_embed_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_outlier_score_ECOD_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_outlier_score_IForest_all-MiniLM-L6-v2",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_dist_from_mean_embed_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_outlier_score_ECOD_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
        {
            "name": "answers[0]_outlier_score_IForest_distiluse-base-multilingual-cased-v1",
            "type": "number",
            "associated_text_col_name": "answers[0]",
        },
    ],
)

dataset_bbc = DatasetInfo(
    name="bbc",
    origin="example",
    column_info=[
        # text columns
        {"name": "text", "type": "text"},
        # dataset metadata
        {"name": "category", "type": "categorical"},
        # derived metadata
        {
            "name": "lava_value",
            "type": "number",
            "associated_text_col_name": "text",
        },
    ],
)

dataset_vis_papers = DatasetInfo(
    name="vis_papers",
    origin="example",
    column_info=[
        {
            "name": "Abstract",
            "type": "text",
        },
        {
            "name": "Title",
            "type": "categorical",
        },
        {
            "name": "DOI",
            "type": "categorical",
        },
        {
            "name": "Link",
            "type": "categorical",
        },
        {
            "name": "FirstPage",
            "type": "number",
        },
        {
            "name": "LastPage",
            "type": "number",
        },
        {
            "name": "AuthorNames-Deduped",
            "type": "categorical",
        },
        {
            "name": "AuthorNames",
            "type": "categorical",
        },
        {
            "name": "AuthorAffiliation",
            "type": "categorical",
        },
        {
            "name": "InternalReferences",
            "type": "categorical",
        },
        {
            "name": "AuthorKeywords",
            "type": "categorical",
        },
        {
            "name": "id",
            "type": "number",
        },
        {
            "name": "Conference",
            "type": "categorical",
        },
        {
            "name": "Year",
            "type": "number",
        },
        {
            "name": "PaperType",
            "type": "categorical",
        },
        {
            "name": "AminerCitationCount",
            "type": "number",
        },
        {
            "name": "CitationCount_CrossRef",
            "type": "number",
        },
        {
            "name": "PubsCited_CrossRef",
            "type": "number",
        },
        {
            "name": "Award",
            "type": "categorical",
        },
        {
            "name": "Abstract_text_length",
            "type": "number",
            "associated_text_col_name": "Abstract",
        },
        {
            "name": "Abstract_num_words",
            "type": "number",
            "associated_text_col_name": "Abstract",
        },
        {
            "name": "Abstract_max_word_length",
            "type": "number",
            "associated_text_col_name": "Abstract",
        },
        {
            "name": "Abstract_avg_word_length",
            "type": "number",
            "associated_text_col_name": "Abstract",
        },
        {
            "name": "Abstract_perc_special_chars",
            "type": "number",
            "associated_text_col_name": "Abstract",
        },
    ],
)


EXAMPLE_DATASETS = [
    dataset_vast2021,
    dataset_vis_papers,
    dataset_dolly,
    dataset_opus,
    dataset_squad,
    dataset_bbc,
]
