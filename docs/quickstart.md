# Quickstart

This page provides a quickstart guide to using Texture. Texture is a Python library that visualizes text data and structured attributes.

## Install and run

Install texture with pip:

```bash
pip install texture-viz
```

Then you can run in a python script or notebook by providing a pandas dataframe with your text data and attributes.

```python
import texture
texture.run(df)
```

## Texture Configuration

You can optionally pass arguments to the `run` command to configure the interface. Configuration options are:

- `data: pd.DataFrame`: The dataframe to parse and visualize.
- `schema`: a dataset schema describing the columns, types, and tables (calculated automatically if none provided)
- `load_tables: Dict[str, pd.DataFrame]`: A dictionary of tables to load into the schema. The key is the table name and the value is the dataframe.
- `create_new_embedding_func`: A function that takes a string and returns a vector embedding (see example below)

There are several reserved column names in the main table that are used in the interface:

- `id`: A unique identifier for each row.
- `vector`: A column containing embeddings for the text data.
- `umap_x` and `umap_y`: Columns containing 2d projections of the embeddings.

We provide various preprocessing functions to calculate embeddings, projections, and word tables. You can use these functions to preprocess your data before launching the Texture app.

```python
import pandas as pd
import texture
from texture.models import DatasetSchema, Column, DerivedSchema

P = "https://raw.githubusercontent.com/cmudig/Texture/main/examples/vis_papers/"

df_main = pd.read_parquet(P + "1_main.parquet")
df_words = pd.read_parquet(P + "2_words.parquet")
df_authors = pd.read_parquet(P + "3_authors.parquet")
df_keywords = pd.read_parquet(P + "4_keywords.parquet")

load_tables = {
    "main_table": df_main,
    "words_table": df_words,
    "authors_table": df_authors,
    "keywords_table": df_keywords,
}

# Create schema for the dataset that decides how the data will be visualized
schema = DatasetSchema(
    name="main_table",
    columns=[
        Column(name="Title", type="text"),
        Column(name="Abstract", type="text"),
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
        Column(name="Year", type="number"),
        Column(name="Conference", type="categorical"),
        Column(name="PaperType", type="categorical"),
        Column(name="CitationCount_CrossRef", type="number"),
        Column(name="Award", type="categorical"),
    ],
    primary_key=Column(name="id", type="number"),
    origin="uploaded",
    has_embeddings=True,
    has_projection=True,
)

def get_embedding(value: str):
    import sentence_transformers

    model = sentence_transformers.SentenceTransformer("all-mpnet-base-v2")
    e = model.encode(value)

    return e

texture.run(
    schema=schema, load_tables=load_tables, create_new_embedding_func=get_embedding
)
```
