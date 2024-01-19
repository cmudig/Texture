import pandas as pd

from textprofilerbackend.models import Column, DatasetInfo


def process_new_file(df: pd.DataFrame, datasetName: str) -> DatasetInfo:
    """
    Process a new file and load it into the database
    """
    print("processing dataset: ", datasetName)
    print("shape:", df.shape)
    print("columns: ", df.columns)

    # create semantic type dict based on types of each column
    text_cols, other_cols = get_data_types(df)

    text_names = [col.name for col in text_cols]

    # heuristic for mapping derived column to text column
    for c in other_cols:
        for t in text_names:
            if c.name.startswith(t):
                c.associated_text_col_name = t

    dsInfo = DatasetInfo(
        name=datasetName, column_info=text_cols + other_cols, origin="uploaded"
    )

    return dsInfo


def get_data_types(df: pd.DataFrame):
    """
    Get the data types of each column in the DataFrame.
    Maps each column to a semantic type: 'number', 'date', 'text', or 'categorical'
    """
    text_cols = []
    other_cols = []

    for col_name, dtype in df.dtypes.items():
        if pd.api.types.is_numeric_dtype(dtype):
            c = Column(name=col_name, type="number")
            other_cols.append(c)
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            c = Column(name=col_name, type="date")
            other_cols.append(c)
        else:
            max_col_len = df[col_name].str.len().max()
            cardinality = df[col_name].nunique()

            # heuristic to detect text or categorical
            if (max_col_len > 100) or (cardinality > 0.1 * len(df)):
                c = Column(name=col_name, type="text")
                text_cols.append(c)
            else:
                c = Column(name=col_name, type="categorical")
                other_cols.append(c)

    return text_cols, other_cols
