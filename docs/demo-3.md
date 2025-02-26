# Demo: LLM output comparison

In this demo, we compare the outputs of various LLM models. This data is originally from the [LLMComparator](https://github.com/PAIR-code/llm-comparator) paper and system.

![Texture UI](./images/llmcomparator.png)

```python
import pandas as pd
import texture
from texture.models import DatasetSchema, Column, DerivedSchema

P = "https://raw.githubusercontent.com/cmudig/Texture/main/examples/llmcomparator/data/"

df_main = pd.read_parquet(P + "1_main.parquet")
df_ratings = pd.read_parquet(P + "2_ratings.parquet")
df_clusters = pd.read_parquet(P + "3_rationale_clusters.parquet")
df_ngrams_A = pd.read_parquet(P + "4_ngrams_A.parquet")
df_ngrams_B = pd.read_parquet(P + "5_ngrams_B.parquet")

load_tables = {
    "main": df_main,
    "ratings": df_ratings,
    "clusters": df_clusters,
    "ngramsA_table": df_ngrams_A,
    "ngramsB_table": df_ngrams_B,
}

schema = DatasetSchema(
    name="main",
    columns=[
        # INPUTS
        Column(name="input_text", type="text"),
        Column(name="A_output_text", type="text"),
        Column(name="B_output_text", type="text"),
        Column(name="rationales", type="text"),
        Column(
            name="ngram_A",
            type="categorical",
            derivedSchema=DerivedSchema(
                is_segment=True,
                table_name="ngramsA_table",
                derived_from="A_output_text",
            ),
        ),
        Column(
            name="ngram_B",
            type="categorical",
            derivedSchema=DerivedSchema(
                is_segment=True,
                table_name="ngramsB_table",
                derived_from="B_output_text",
            ),
        ),
        # RATIONALES and ratings
        Column(name="winner", type="categorical"),
        Column(name="score", type="number"),
        Column(name="winner_degree", type="categorical"),
        Column(
            name="individual_ratings",
            type="categorical",
            derivedSchema=DerivedSchema(
                is_segment=False,
                table_name="ratings",
            ),
        ),
        Column(
            name="individual_scores",
            type="number",
            derivedSchema=DerivedSchema(
                is_segment=False,
                table_name="ratings",
            ),
        ),
        Column(
            name="rationale_clusters",
            type="categorical",
            derivedSchema=DerivedSchema(
                is_segment=False,
                table_name="clusters",
            ),
        ),
        # METADATA
        Column(name="tag", type="categorical"),
        Column(name="A_toxic", type="number"),
        Column(name="B_toxic", type="number"),
        Column(name="A_sexual", type="number"),
        Column(name="B_sexual", type="number"),
        Column(name="A_violent", type="number"),
        Column(name="B_violent", type="number"),
        Column(name="A_word_count", type="number"),
        Column(name="B_word_count", type="number"),
        Column(
            name="A_has_bullet_lists",
            type="categorical",
        ),
        Column(
            name="B_has_bullet_lists",
            type="categorical",
        ),
        Column(name="A_has_headings", type="categorical"),
        Column(name="B_has_headings", type="categorical"),
        Column(name="A_has_url", type="categorical"),
        Column(name="B_has_url", type="categorical"),
        Column(name="A_has_sure", type="categorical"),
        Column(name="B_has_sure", type="categorical"),
    ],
    primary_key=Column(name="id", type="number"),
    has_embeddings=False,
    has_projection=False,
)

texture.run(schema=schema, load_tables=load_tables)
```
