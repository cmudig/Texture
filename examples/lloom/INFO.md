# LLOOM dataset

This data contains outputs produced by the concept induction algorithm and lloom system (see https://hci.stanford.edu/publications/2024/Lam_LLooM_CHI24.pdf).

Details:

- Data is originally from the lloom paper, usage scenario 2 of social media posts
- Topics come from running lloom
- Embeddings are from openAI text-embedding-3-small model (in october / november 2024)

To run, either run the notebook `analysis.ipynb` or run the python script `python analysis.py`. Both will load the data and then launch the Texture server.
