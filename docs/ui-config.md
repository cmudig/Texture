# UI Configuration

You can pass arguments to the `run` command to configure the Texture interface.

- `data: pd.DataFrame`: The dataframe to parse and visualize.
- `schema: DatasetSchema`: a dataset schema (calculated automatically if none provided)
- `load_tables: Dict[str, pd.DataFrame]`: A dictionary of tables to load.
- `create_new_embedding_func`: A function that takes a string and returns a vector embedding (see example below)

If only `data` is provided, Texture will automatically calculate the schema and load tables. The schema and tables can also be calculated manually by calling the `preprocess` function then passed to `run`:

```python
# automatically calculate schema and tables
texture.run(df)

# OR manually preprocess
schema, load_tables = texture.preprocess(df)
```

## `DatasetSchema`

The schema is a `DatasetSchema` object that describes the columns, types, and tables in the dataset. These column definitions are used to determine how the data will be visualized in the interface. Each schema has the following fields:

- `name`: The name of the dataset.
- `columns`: A list of `Column` objects that describe the columns in the dataset.
- `primary_key`: A `Column` object that describes the primary key of the dataset.
- `has_embeddings`: Whether the dataset has embeddings or not. If so, must contain a column named `"vector"` with embedding arrays
- `has_projection`: Whether the dataset has projections or not. If so, must contain columns named `"umap_x"` and `"umap_y"` with 2d projection coordinates.

## `Column`

`Column` definition contains:

- `name`: The name of the column as it appears in the dataframe
- `type`: The type of the column. Options are `text`, `number`, `categorical`, and `boolean`.
- `derivedSchema`: A `DerivedSchema` object that describes how the column is derived from another table. Options are:
  - `is_segment`: Whether the column is a segment (e.g. word, phrase) or not (e.g. author, keyword).
  - `table_name`: The name of the table the column is in.
  - `derived_from`: The column in the main table that the column is derived from.
  - `derived_how`: How the column is derived from the derived table.

## Example

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
            ),
        ),
        Column(
            name="pos",
            type="categorical",
            derivedSchema=DerivedSchema(
                is_segment=True,
                table_name="words_table",
                derived_from="Abstract",
            ),
        ),
        Column(
            name="author",
            type="categorical",
            derivedSchema=DerivedSchema(
                is_segment=False,
                table_name="authors_table",
            ),
        ),
        Column(
            name="keyword",
            type="categorical",
            derivedSchema=DerivedSchema(
                is_segment=False,
                table_name="keywords_table",
            ),
        ),
        Column(name="Year", type="number"),
        Column(name="Conference", type="categorical"),
        Column(name="PaperType", type="categorical"),
        Column(name="CitationCount_CrossRef", type="number"),
        Column(name="Award", type="categorical"),
    ],
    primary_key=Column(name="id", type="number"),
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

This will launch the Texture UI:

![Texture UI](./images/vis-abstracts.png)
