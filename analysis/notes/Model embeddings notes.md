# Model embeddings

Using the sentence transformers library, has list of models here: https://www.sbert.net/docs/pretrained_models.html

### Models

- **all-mpnet-base-v2**: all around model, has highest average performance AND is relatively fast (T5 is very slow, all-mpnet-base-v2 is 56x faster)

### Embedding similarity

- Can use cosine similarity to calculate similarity between embeddings.
- Cosine similarity has range of [-1, 1], where -1 is opposite, 1 is same, and 0 is orthogonal (e.g. no similarity).

### deduplication

- Lilac uses minhash duplication, see https://github.dev/lilacai/lilac/lilac/signals/minhash_dup.py

### PII detection

- Lilac uses https://github.com/microsoft/presidio/
