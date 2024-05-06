import torch
import pandas as pd
from typing import List
from texture.models import ColumnInputInfo


def get_data_types(_df: pd.DataFrame) -> List[ColumnInputInfo]:
    """
    Get the data types of each column in the DataFrame.
    Maps each column to a semantic type: 'number', 'date', 'text', or 'categorical'
    """
    data_info = []
    for col_name, dtype in _df.dtypes.items():
        inferred_type = None

        if pd.api.types.is_numeric_dtype(dtype):
            inferred_type = "number"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            inferred_type = "date"
        else:
            max_col_len = _df[col_name].str.len().max()
            cardinality = _df[col_name].nunique()

            # heuristic to detect text or categorical
            if (max_col_len > 200) or (cardinality == len(_df)):
                inferred_type = "text"
            else:
                inferred_type = "categorical"

        c = ColumnInputInfo(name=col_name, type=inferred_type)
        data_info.append(c)
    return data_info


def save_embeddings(embedding, path):
    torch.save(embedding, path)
    print("Saved embedding to ", path)


def load_embeddings(path):
    e = torch.load(path)
    print("Loaded embedding from ", path)
    return e
