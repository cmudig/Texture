import pandas as pd


def process_new_file(df: pd.DataFrame):
    """
    Process a new file and load it into the database
    """
    print("processing df")
    print("shape:", df.shape)
    print("columns: ", df.columns)
