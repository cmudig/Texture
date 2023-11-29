from textclean.utils import timer_print
import sentence_transformers
from sklearn.cluster import HDBSCAN
import numpy as np
import pandas as pd
import torch


def get_cluster_id_col(clusters, max_size) -> list[str]:
    """
    Args:
        clusters: list of lists where each list has indicies of rows belonging to that cluster
        max_size: size of original corpus

    Returns:
        cluster_strings: list of strings where each string is the cluster id for that row or None
    """
    cluster_col = [None] * max_size

    for i, cluster_indexes in enumerate(clusters):
        for sentence_idx in cluster_indexes:
            if cluster_col[sentence_idx] is not None:
                print("[WARN] Repeat cluster entry: ", sentence_idx)

            cluster_col[sentence_idx] = i

    return cluster_col


@timer_print
def get_clusters_comm_detection(
    corpus_embeddings: torch.tensor, min_community_size=2, threshold=0.9
) -> list[int]:
    """
    Uses custom community detection algorithm from sentence_transformers library, each sentence ends up in only 1 cluster
    but not all sentences are clustered.

    Args:
        corpus_embeddings: torch tensor embedding matrix of shape (N, D)
        min_community_size: Only consider cluster that have at least a certain number of elements.
        threshold: cosine-similarity larger than threshold are similar (cos has range of -1 to 1)

    Returns:
        clusters: list of len=N with cluster id or None
    """
    print("Starting clustering...")
    clusters = sentence_transformers.util.community_detection(
        corpus_embeddings, min_community_size=min_community_size, threshold=threshold
    )

    print(f"Found {len(clusters)} clusters")

    return get_cluster_id_col(clusters, corpus_embeddings.shape[0])


@timer_print
def get_clusters_hdbscan(corpus_embeddings: torch.tensor, min_size=2) -> list[int]:
    """
    Uses hdbscan to cluster embeddings, each sentence ends up in only 1 cluster or is labeled as noise (undefined cluster)

    Args:
        corpus_embeddings: torch tensor embedding matrix of shape (N, D)
        min_size: Only consider cluster that have at least min_size elements.

    Returns:
       clusters: list of len=N with cluster id or None
    """
    print("Starting clustering...")

    hdb = HDBSCAN(min_cluster_size=min_size, metric="euclidean")
    hdb.fit(corpus_embeddings)
    clusters = hdb.labels_
    print(f"Found {np.unique(clusters).size - 1} clusters")

    # hdbscan labels -1 as noise, so we replace that with None
    clusters = np.where(clusters == -1, None, clusters)

    return clusters


def detect_duplicates(text_col, embeddings):
    clusters_comm = get_clusters_comm_detection(embeddings)
    clusters_hdb = get_clusters_hdbscan(embeddings)

    name = text_col.name

    return pd.DataFrame(
        {
            name: text_col,
            f"{name}_cluster_id_comm": clusters_comm,
            f"{name}_cluster_id_hdb": clusters_hdb,
        }
    )
