from texture.runner import run
import pandas as pd
from texture.models import DatasetSchema, Column, DerivedSchema


def dev_run():
    """For launching server from poetry"""
    # N.B frontend dev server hard coded for localhost:8080

    df_main = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "text": [
                "A B",
                "A B",
                "B C",
                "B C",
                "C A",
                "C A",
                "C D",
                "C D",
                "D A",
                "D A",
            ],
            "topic": [
                "topic really really long name cool nice",
                "topic_1",
                "topic_1",
                "topic_1",
                "topic_2",
                "topic_2",
                "topic_2",
                "topic_2",
                "topic_3",
                "topic_3",
            ],
            "quantMeasure": [1, 20, 30, 30, 60, 60, 70, 8, 9, 10],
            "umap_x": [
                0.3745,
                0.9507,
                0.7319,
                0.5987,
                0.1560,
                0.1559,
                0.0581,
                0.8662,
                0.6011,
                0.7081,
            ],
            "umap_y": [
                0.0205,
                0.9699,
                0.8324,
                0.2123,
                0.1818,
                0.1834,
                0.3042,
                0.5248,
                0.4319,
                0.2912,
            ],
            "vector": [
                [0.3745, 0.0205],
                [0.9507, 0.9699],
                [0.7319, 0.8324],
                [0.5987, 0.2123],
                [0.1560, 0.1818],
                [0.1559, 0.1834],
                [0.0581, 0.3042],
                [0.8662, 0.5248],
                [0.6011, 0.4319],
                [0.7081, 0.2912],
            ],
        }
    )

    df_words = pd.DataFrame(
        {
            "id": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10],
            "word": [
                "A",
                "B",
                "A",
                "B",
                "B",
                "C",
                "B",
                "C",
                "C",
                "A",
                "C",
                "A",
                "C",
                "D",
                "C",
                "D",
                "D",
                "A",
                "D",
                "A",
            ],
            "span_start": [0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
            "span_end": [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
        }
    )

    df_author = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6, 6, 7, 7, 7, 8],
            "author": [
                "author_1",
                "author_2",
                "author_3",
                "author_4",
                "author_5",
                "author_6",
                "author_7",
                "author_6",
                "author_7",
                "author_7",
                "author_8",
            ],
            "span_start": [0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 0],
            "span_end": [1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 1],
        }
    )

    load_tables = {
        "main_table": df_main,
        "words_table": df_words,
        "authors_table": df_author,
    }

    schema = DatasetSchema(
        name="main_table",
        columns=[
            Column(name="text", type="text"),
            Column(name="topic", type="categorical"),
            Column(name="quantMeasure", type="number"),
            # hierarchical segment
            Column(
                name="word",
                type="categorical",
                derivedSchema=DerivedSchema(
                    is_segment=True,
                    table_name="words_table",
                    derived_from="text",
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
        ],
        primary_key=Column(name="id", type="number"),
        origin="uploaded",
        has_embeddings=True,
        has_projection=True,
    )

    def get_embedding(value: str):
        return [0.5, 0.5]

    run(schema=schema, load_tables=load_tables, create_new_embedding_func=get_embedding)


if __name__ == "__main__":
    dev_run()
