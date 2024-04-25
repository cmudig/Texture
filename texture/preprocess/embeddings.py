import umap
import sentence_transformers
import numpy as np

from texture.preprocess.utils import save_embeddings

# see https://www.sbert.net/docs/pretrained_models.html for all models
# best model overall for english: "all-mpnet-base-v2"
# best semantic similarity across languages: "distiluse-base-multilingual-cased-v1"
# best model for Bitext Mining i.e. translation: "LaBSE"


def calculate_embeddings(
    col: np.ndarray, model_name="all-mpnet-base-v2", useTensor=True
):
    """
    Calcs the embeddings.
    TODO: My understanding is the sentence_transformers library cuts off inputs longer than
    384 words. Need to fix that for longer docs probably by chunking text into longest amount and
    then averaging the resulting embeddings
    """
    model = sentence_transformers.SentenceTransformer(model_name)
    e = model.encode(col, convert_to_tensor=useTensor)
    print("Created embedding of shape", e.shape, "with", model_name)
    return e


def get_projection(vector):
    # alt metric is "cosine"
    # NOTE: for some reason this breaks on intel mac laptop if n_jobs is not 1 so dont change
    return umap.UMAP(metric="euclidean", n_components=2, n_jobs=1).fit_transform(
        vector,
    )


def get_embeddings_and_projection(
    col_matrix: np.ndarray, base_path=None, model_name="all-mpnet-base-v2"
):
    embeddings = calculate_embeddings(col_matrix, model_name)

    if base_path:
        embed_path = base_path / "embeddings.pt"
        save_embeddings(embeddings, embed_path)

    projection = get_projection(embeddings)
    return embeddings, projection
