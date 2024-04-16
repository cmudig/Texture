from umap import UMAP


def get_projection(vector):
    # alt metric is "cosine"
    return umap.UMAP(metric="euclidean", n_components=2).fit_transform(vector)
