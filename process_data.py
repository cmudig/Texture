import textclean
import pandas as pd

datasets = ["dolly15k", "opus100-en-es", "squad_validation"]

for d in datasets:
    df = pd.read_csv(f"datasets/raw/{d}.csv")
    m = textclean.TextCleaner(df)
    processed_df = m.transform_and_save(f"datasets/processed/{d}.csv")
