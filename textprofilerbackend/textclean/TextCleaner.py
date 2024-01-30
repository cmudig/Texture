import pandas as pd
import string
import random

from .model_metrics import extract_col_model_metadata
from .embeddings import calculate_embeddings


class TextCleaner:
    """
    TextCleaner main class

    df: the dataframe with raw data
    text_columns: the columns in the dataframe that contain text for processing
    model_names: models to use for embedding. Can by any models on https://www.sbert.net/docs/pretrained_models.html
    """

    def __init__(self, df, text_columns, model_names, extract_model_meta=True):
        self.df = df
        self.text_columns = text_columns
        self.model_names = model_names
        self.extract_model_meta = extract_model_meta and (len(self.model_names) > 0)

    def process(self):
        return extract_all_metadata(
            self.df, self.text_columns, self.model_names, self.extract_model_meta
        )


def get_textcol_metadata_embeddings(
    col: pd.Series,
    model_names: list[str],
):
    heuristic_metadata = extract_col_heuristic_metadata(col)
    model_meta = None

    if model_names and len(model_names) > 0:
        model_meta = {}
        for model_name in model_names:
            embeddings = calculate_embeddings(col, model_name)
            model_meta[model_name] = embeddings

    return {"heuristic_metadata": heuristic_metadata, "model_embeddings": model_meta}


def extract_all_metadata(
    df: pd.DataFrame,
    text_column_names: list[str],
    model_names: list[str],
    extract_model_meta=True,
):
    original_columns = df.columns
    confirmed_text_columns = []
    text_meta_columns = {}

    for colname in text_column_names:
        if is_string_series(df[colname]):
            print("extracting metadata for", colname)
            confirmed_text_columns.append(colname)
            heuristic_metadata = extract_col_heuristic_metadata(df[colname])
            df = df.join(heuristic_metadata)
            text_meta_columns[colname] = list(heuristic_metadata.columns)

            if extract_model_meta:
                model_meta = extract_col_model_metadata(df[colname], model_names)
                df = df.join(model_meta)
                text_meta_columns[colname].extend(model_meta.columns)

    if extract_model_meta and len(text_column_names) > 1:
        joint_col_name = generate_joint_column_name(original_columns)

        df = join_text_columns(df, text_column_names, col_name=joint_col_name)
        row_model_meta = extract_col_model_metadata(df[joint_col_name], model_names)
        df = df.join(row_model_meta)

        confirmed_text_columns.append(joint_col_name)
        text_meta_columns[joint_col_name] = list(row_model_meta.columns)

    other_columns = [c for c in original_columns if c not in confirmed_text_columns]
    metadata = {
        "text_columns": confirmed_text_columns,
        "other_columns": other_columns,
        "text_meta_columns": text_meta_columns,
    }

    return df, metadata


def is_string_series(s: pd.Series):
    if isinstance(s.dtype, pd.StringDtype):
        # The series was explicitly created as a string series (Pandas>=1.0.0)
        return True
    elif s.dtype == "object":
        # Object series, check each value
        return all(pd.isna(v) or isinstance(v, str) for v in s)
    else:
        return False


def get_max_word_len(s: str):
    return max([len(w) for w in s.split()])


def get_avg_word_len(s: str):
    return sum([len(w) for w in s.split()]) / len(s.split())


def get_special_char_percentage(s: str):
    special_chars = set(string.punctuation)
    num_special_chars = sum(1 for c in s if c in special_chars)
    return num_special_chars / len(s)


def extract_col_heuristic_metadata(col: pd.Series):
    """Extract instance level metadata from a string

    TODO: other potential metadata:
        - 'Language',
        - 'Sentiment',
        - 'Subjectivity',
        - 'Reading Ease',
        - 'Lexical Density'
    """

    col_name = col.name
    nonNullCol = col[~col.isna()]

    m = pd.DataFrame(
        {
            f"{col_name}_text_length": nonNullCol.str.len(),
            f"{col_name}_num_words": nonNullCol.str.split().str.len(),
            f"{col_name}_max_word_length": nonNullCol.apply(get_max_word_len),
            f"{col_name}_avg_word_length": nonNullCol.apply(get_avg_word_len),
            f"{col_name}_perc_special_chars": nonNullCol.apply(
                get_special_char_percentage
            ),
        },
        index=nonNullCol.index,
    )

    return m


def clean_value(x):
    if isinstance(x, str):
        return x
    return ""


def join_text_columns(df: pd.DataFrame, text_columns: list[str], col_name="joint"):
    # TODO: this will create column even if all text columns are null, should prob not
    df[col_name] = df[text_columns].apply(
        lambda x: " ".join(
            [f"{col}: {clean_value(val)}" for col, val in zip(text_columns, x)]
        ),
        axis=1,
    )
    return df


def generate_joint_column_name(all_column_names) -> str:
    joint_column_name = "joint"
    while joint_column_name in all_column_names:
        joint_column_name = "joint" + str(random.randint(0, 10000))
    return joint_column_name
