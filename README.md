# Text corpus cleaner

Can I use heuristic checks and models to help you clean your text data?

Goal

- Prepare data for downstream modelling task
- Answer: what is even in this text corpus?

Look at benchmark datasets from...

- text to code generation
- translation
- summarization
- chat

## Datasets

1. Databricks dolly -- chatbot dataset
2. squad v2 -- validation set https://huggingface.co/datasets/squad_v2/viewer/squad_v2/validation
3. opus100-en-es-validation -- https://huggingface.co/datasets/opus100/viewer/en-es/validation

Other (larger) 4. open-orca-100k -- from Lilac AI, their sample of 100k points out of 4.2M in total (https://huggingface.co/datasets/lilacai/lilac-OpenOrca-100k)

## Exploration

For each domain

1. what are useful heuristics?
2. Can I find bad data points with heuristics?
3. Can I find bad data points with outlier detection?
4. Can I find bad data poitns with a model?
5. What data points would I want to add?
