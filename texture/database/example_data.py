from texture.models import DatasetInfo

dataset_vis_papers = DatasetInfo(
    name="vis_papers",
    primary_key={"name": "id", "type": "number"},
    origin="example",
    has_embeddings=True,
    has_projection=True,
    columns=[
        {
            "name": "Title",
            "type": "text",
        },
        {
            "name": "Abstract",
            "type": "text",
        },
        {
            "name": "word",
            "type": "categorical",
            "table_name": "vis_papers_words",
            "derived_from": "Abstract",
        },
        # {
        #     "name": "Abstract_num_words",
        #     "type": "number",
        #     "derived_from": "Abstract",
        #     "derived_how": "code",
        # },
        {
            "name": "Year",
            "type": "number",
        },
        {
            "name": "Conference",
            "type": "categorical",
        },
        {
            "name": "author",
            "type": "categorical",
            "table_name": "vis_papers_authors",
            "derived_from": "AuthorNames-Deduped",
        },
        {
            "name": "keyword",
            "type": "categorical",
            "table_name": "vis_papers_keywords",
            "derived_from": "AuthorKeywords",
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
        # {
        #     "name": "id",
        #     "type": "number",
        # },
        # {
        #     "name": "MODEL_sport",
        #     "type": "categorical",
        #     "derived_from": "Abstract",
        #     "derived_how": "model",
        # },
        # {
        #     "name": "AuthorNames-Deduped",
        #     "type": "categorical",
        # },
        # {
        #     "name": "AuthorKeywords",
        #     "type": "categorical",
        # },
        # {
        #     "name": "Abstract_text_length",
        #     "type": "number",
        #     "derived_from": "Abstract",
        # },
        # {
        #     "name": "MODEL_num_participants",
        #     "type": "number",
        #     "derived_from": "Abstract",
        # },
        # {
        #     "name": "MODEL_keywords",
        #     "type": "categorical",
        #     "derived_from": "Abstract",
        # },
        # {
        #     "name": "MODEL_summary",
        #     "type": "text",
        #     "derived_from": "Abstract",
        # },
        # {
        #     "name": "MODEL_has_user_study",
        #     "type": "categorical",
        #     "derived_from": "Abstract",
        # },
        # {
        #     "name": "DOI",
        #     "type": "categorical",
        # },
        # {
        #     "name": "Link",
        #     "type": "categorical",
        # },
        # {
        #     "name": "FirstPage",
        #     "type": "number",
        # },
        # {
        #     "name": "LastPage",
        #     "type": "number",
        # },
        # {
        #     "name": "AuthorNames",
        #     "type": "categorical",
        # },
        # {
        #     "name": "AuthorAffiliation",
        #     "type": "categorical",
        # },
        # {
        #     "name": "InternalReferences",
        #     "type": "categorical",
        # },
        #
        # {
        #     "name": "Abstract_max_word_length",
        #     "type": "number",
        #     "derived_from": "Abstract",
        # },
        # {
        #     "name": "Abstract_avg_word_length",
        #     "type": "number",
        #     "derived_from": "Abstract",
        # },
        # {
        #     "name": "Abstract_perc_special_chars",
        #     "type": "number",
        #     "derived_from": "Abstract",
        # },
    ],
)

dataset_airline_reviews = DatasetInfo(
    name="airline_reviews",
    primary_key={"name": "id", "type": "number"},
    origin="example",
    has_embeddings=True,
    has_projection=True,
    columns=[
        # {"name": "id", "type": "categorical"},
        # {
        #     "name": "tweet_num_characters",
        #     "type": "number",
        #     "derived_from": "tweet",
        #     "derived_how": "code",
        # },
        # {
        #     "name": "twitter_handle",
        #     "type": "categorical",
        #     "derived_from": "tweet",
        #     "derived_how": "code",
        # },
        # {
        #     "name": "is_on_hold",
        #     "type": "categorical",
        #     "derived_from": "tweet",
        #     "derived_how": "model",
        # },
        {
            "name": "word",
            "type": "categorical",
            "table_name": "tweet_words",
            "derived_from": "tweet",
        },
        {"name": "airline", "type": "categorical"},
        {"name": "airline_sentiment", "type": "categorical"},
        {"name": "airline_sentiment_confidence", "type": "number"},
        {"name": "negativereason", "type": "categorical"},
        {"name": "negativereason_confidence", "type": "number"},
        # {"name": "airline_sentiment_gold", "type": "categorical"},  # mostly null
        {"name": "name", "type": "categorical"},
        # {"name": "negativereason_gold", "type": "categorical"}, # mostly null
        {"name": "retweet_count", "type": "number"},
        {"name": "tweet", "type": "text"},
        # {"name": "tweet_coord", "type": "categorical"}, # x, y coords I think
        {"name": "tweet_created", "type": "date"},
        {"name": "tweet_location", "type": "categorical"},
        {"name": "user_timezone", "type": "categorical"},
    ],
)


EXAMPLE_DATASET_INFO = {
    "vis_papers": dataset_vis_papers,
    "airline_reviews": dataset_airline_reviews,
}

EXAMPLE_DATA_PATHS = {
    "vis_papers": {
        "datasets": {
            "vis_papers": "raw_data/vis_papers/vis_papers.parquet",
            "vis_papers_words": "raw_data/vis_papers/vis_papers_words_span.parquet",
            "vis_papers_authors": "raw_data/vis_papers/vis_papers_authors_span.parquet",
            "vis_papers_keywords": "raw_data/vis_papers/vis_papers_keywords_span.parquet",
        },
        "embeddings": {"vis_papers": "raw_data/vis_papers/vis_papers_embeddings.pt"},
    },
    "airline_reviews": {
        "datasets": {
            "airline_reviews": "raw_data/airline_reviews/airlines.parquet",
            "tweet_words": "raw_data/airline_reviews/tweet_words.parquet",
        },
        "embeddings": {"airline_reviews": "raw_data/airline_reviews/embeddings.pt"},
    },
}
