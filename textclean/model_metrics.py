import numpy as np
import pandas as pd
import sentence_transformers
from pyod.models.ecod import ECOD
from pyod.models.iforest import IForest


def calculate_embeddings(col: np.ndarray, model_name: str):
    """
    Calcs the embeddings.
    TODO: My understanding is the sentence_transformers library cuts off inputs longer than
    384 words. Need to fix that for longer docs probably by chunking text into longest amount and
    then averaging the resulting embeddings
    """
    model = sentence_transformers.SentenceTransformer(model_name)
    e = model.encode(col)
    print("Created embedding of shape", e.shape, "with", model_name)
    return e


def get_mean_embeddings_dist(embeddings: np.ndarray):
    avg_embed = embeddings.mean(axis=0)
    distances = sentence_transformers.util.cos_sim(avg_embed, embeddings)
    return distances.flatten()


def get_outlier_scores(data, detector_name="ECOD"):
    if detector_name == "ECOD":
        detector = ECOD()
    else:
        detector = IForest()
    detector.fit(data)
    return detector.decision_scores_


def extract_col_model_metadata(col: pd.Series, model_names: list[str]):
    """
    Returns a dataframe with model based metadata extracted.

    NOTE: the returned dataframe will filter out the null values in the column. It may not have
    the same size, but will maintain the col index for joins
    """
    col_name = col.name
    nonNullCol = col[~col.isna()]

    results = {}

    for model_name in model_names:
        print("calculating embeddings for", col_name, "with", model_name)
        embeddings = calculate_embeddings(nonNullCol.values, model_name)

        results[
            f"{col_name}_dist_from_mean_embed_{model_name}"
        ] = get_mean_embeddings_dist(embeddings)

        for detector_name in ["ECOD", "IForest"]:
            results[
                f"{col_name}_outlier_score_{detector_name}_{model_name}"
            ] = get_outlier_scores(embeddings, detector_name)

    return pd.DataFrame(results, index=nonNullCol.index)
