import pandas as pd
import texture
from texture.models import DatasetSchema, Column, DerivedSchema


def get_embedding(value: str):
    import sentence_transformers

    model = sentence_transformers.SentenceTransformer("all-mpnet-base-v2")
    e = model.encode(value)

    return e


def launch():
    df_main = pd.read_parquet("./data/1_main.parquet")
    df_words = pd.read_parquet("./data/2_words.parquet")
    df_authors = pd.read_parquet("./data/3_authors.parquet")
    df_keywords = pd.read_parquet("./data/4_keywords.parquet")

    load_tables = {
        "main_table": df_main,
        "words_table": df_words,
        "authors_table": df_authors,
        "keywords_table": df_keywords,
    }

    schema = DatasetSchema(
        name="main_table",
        columns=[
            Column(name="Title", type="text", derivedSchema=None),
            Column(name="Abstract", type="text", derivedSchema=None),
            Column(
                name="word",
                type="categorical",
                derivedSchema=DerivedSchema(
                    is_segment=True,
                    table_name="words_table",
                    derived_from="Abstract",
                    derived_how=None,
                ),
            ),
            Column(
                name="pos",
                type="categorical",
                derivedSchema=DerivedSchema(
                    is_segment=True,
                    table_name="words_table",
                    derived_from="Abstract",
                    derived_how=None,
                ),
            ),
            # hierarchical non-segment
            Column(
                name="author",
                type="categorical",
                derivedSchema=DerivedSchema(
                    is_segment=False,
                    table_name="authors_table",
                    derived_from=None,
                    derived_how=None,
                ),
            ),
            Column(
                name="keyword",
                type="categorical",
                derivedSchema=DerivedSchema(
                    is_segment=False,
                    table_name="keywords_table",
                    derived_from=None,
                    derived_how=None,
                ),
            ),
            Column(name="Year", type="number", derivedSchema=None),
            Column(name="Conference", type="categorical", derivedSchema=None),
            Column(name="PaperType", type="categorical", derivedSchema=None),
            Column(name="CitationCount_CrossRef", type="number", derivedSchema=None),
            Column(name="Award", type="categorical", derivedSchema=None),
        ],
        primary_key=Column(name="id", type="number", derivedSchema=None),
        origin="uploaded",
        has_embeddings=True,
        has_projection=True,
    )

    texture.run(
        schema=schema, load_tables=load_tables, create_new_embedding_func=get_embedding
    )


if __name__ == "__main__":
    launch()
