import pandas as pd
from pathlib import Path

from texture.preprocess.utils import save_embeddings
from texture.preprocess.tokenize import get_df_words_w_span
from texture.preprocess.utils import get_data_types
from texture.preprocess.embeddings import get_embeddings_and_projection


####### example run
def run_preprocess_pipeline():
    dataset_name = "example_dataset"
    base_path = Path(dataset_name)
    base_path.mkdir(exist_ok=True)

    df = pd.read_parquet(
        "/Users/wepperso/workspaces/Research/TextureAll/Texture/.texture_cache/raw_data/mateo_data/public_systems.parquet"
    )

    # step 1: infer and correct data types
    data_types = get_data_types(df)
    print("Data types:", data_types)

    # calculate embeddings however you want, for example by just using the first text column
    first_text = next(
        (info["name"] for info in data_types if info["type"] == "text"), None
    )

    if first_text is None:
        raise ValueError("No text column found for embeddings or words!")

    # step 2: get embeddings and project

    embeddings, projection = get_embeddings_and_projection(
        df[first_text].values, base_path
    )

    df["umap_x"] = projection[:, 0]
    df["umap_y"] = projection[:, 1]

    dataset_path = base_path / "data.parquet"
    df.to_parquet(dataset_path)
    print("Saved dataset to ", dataset_path)

    # step 4: calculate words
    words = get_df_words_w_span(df[first_text].values, df.id.values)
    word_path = base_path / f"{first_text}_words.parquet"
    words.to_parquet(word_path)
    print("Saved words to ", word_path)
    print("Done!")
