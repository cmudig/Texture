import textclean
import pandas as pd
from pathlib import Path
import torch
import numpy as np

# CONFIG
CACHE_PATH = Path("datasets/processed/embedding_cache")


# METADATA
dataset_info = [
    {
        "name": "vast2021",
        "raw_url": "datasets/raw/vast2021.csv",
        "metadata": {
            "text_columns": [{"name": "message", "type": "text"}],
            "other_columns": [
                {"name": "type", "type": "categorical"},
                {"name": "date(yyyyMMddHHmmss)", "type": "number"},
                {"name": "author", "type": "categorical"},
                {"name": "latitude", "type": "number"},
                {"name": "longitude", "type": "number"},
                {"name": "location", "type": "categorical"},
                {"name": "date", "type": "date"},
            ],
        },
    },
    # ["dolly15k", "opus100-en-es", "squad_validation"]
]

model_names = [
    "all-mpnet-base-v2",  # best performing on leaderboard
    # "all-MiniLM-L6-v2",  # smaller and faster
]


# ~~~~~~~~ Embedding saving and loading ~~~~~~~~


def save_embeddings(embedding, filename):
    path = CACHE_PATH / filename
    torch.save(embedding, path)
    print("Saved embedding to ", path)


def load_embeddings(filename):
    path = CACHE_PATH / filename
    e = torch.load(path)
    print("Loaded embedding from ", path)
    return e


def calculate_or_get_from_cache(
    ds_name: str, col_name: str, model_name: str, column_data: np.ndarray
):
    filename = f"DATA_{ds_name}COL_{col_name}MODEL_{model_name}.pt"

    if (CACHE_PATH / filename).exists():
        print("Found in cache.")
        return load_embeddings(filename)
    else:
        print("Not found in cache. Calculating embeddings...")

        embeddings = textclean.calculate_embeddings(column_data, model_name)
        save_embeddings(embeddings, filename)
        return embeddings


for info_dict in dataset_info:
    ds_name = info_dict["name"]
    ds_path = info_dict["raw_url"]
    ds_text_cols = [x["name"] for x in info_dict["metadata"]["text_columns"]]

    df = pd.read_csv(ds_path)
    # m = textclean.TextCleaner(df)
    # processed_df = m.transform_and_save(f"datasets/processed/{d}.csv")

    for t in ds_text_cols:
        print("Processing column ", t)
        s = df[t]
        embeddings = calculate_or_get_from_cache(ds_name, t, model_names[0], s.values)

        # TODO this should be a param -- dedup
        s = s.drop_duplicates()
        deduped_embed = embeddings[s.index]

        duplicates_df = textclean.detect_duplicates(s, deduped_embed)

        duplicates_df.to_csv(f"datasets/processed/{ds_name}_{t}_duplicates.csv")
