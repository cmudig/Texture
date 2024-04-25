import sentence_transformers
import numpy as np


def calculate_embeddings(col: np.ndarray, model_name: str, useTensor=True):
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
