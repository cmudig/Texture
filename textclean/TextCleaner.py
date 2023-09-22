import pandas as pd
import string
from textclean.model_metrics import extract_col_model_metadata


class TextCleaner:
    """
    TextCleaner main class

    df: the dataframe with raw data
    text_columns: the columns in the dataframe that contain text for processing
    model_names: models to use for embedding. Can by any models on https://www.sbert.net/docs/pretrained_models.html
    """

    def __init__(self, df, text_columns, model_names):
        self.df = df
        self.text_columns = text_columns
        self.model_names = model_names

    def process(self):
        return extract_all_metadata(self.df, self.text_columns, self.model_names)

    # def transform_and_save(self, path="transformed_data.csv"):
    #     data = self.process()
    #     data.to_csv(path, index=False)


def extract_all_metadata(
    df: pd.DataFrame, column_names: list[str], model_names: list[str]
):
    for colname in column_names:
        if is_string_series(df[colname]):
            print("extracting metadata for", colname)
            heuristic_metadata = extract_col_heuristic_metadata(df[colname])
            model_meta = extract_col_model_metadata(df[colname], model_names)
            df = df.join(heuristic_metadata)
            df = df.join(model_meta)

    df = join_text_columns(df, column_names)
    row_model_meta = extract_col_model_metadata(df["joint"], model_names)
    df = df.join(row_model_meta)

    return df


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


def join_text_columns(df: pd.DataFrame, text_columns: list[str]):
    # TODO: this will create column even if all text columns are null, should prob not

    df["joint"] = df[text_columns].apply(
        lambda x: " ".join(
            [f"{col}: {clean_value(val)}" for col, val in zip(text_columns, x)]
        ),
        axis=1,
    )

    return df
