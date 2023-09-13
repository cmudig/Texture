import pandas as pd
import string


class TextCleaner:
    def __init__(self, df):
        self.df = df

    def process(self):
        return extract_all_metadata(self.df)

    def transform_and_save(self, path="transformed_data.csv"):
        data = self.process()
        data.to_csv(path, index=False)


def extract_all_metadata(df: pd.DataFrame):
    for colname in df.columns:
        if is_string_series(df[colname]):
            print("extracting metadata for ", colname)
            metadata = extract_column_metadata(df[colname])
            df = df.join(metadata)

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


def get_special_char_percentage(s: str):
    special_chars = set(string.punctuation)
    num_special_chars = sum(1 for c in s if c in special_chars)
    return num_special_chars / len(s)


def get_word_data(s: str):
    """Extract instance level metadata from a string

    TODO: other potential metadata: 'Language', 'Sentiment', 'Subjectivity', 'Reading Ease', 'Lexical Density'
    """

    if isinstance(s, str):
        split_arr = s.split()
        return pd.Series(
            {
                "text_length": len(s),
                "num_words": len(split_arr),
                "max_word_length": max([len(w) for w in split_arr]),
                "avg_word_length": sum([len(w) for w in split_arr]) / len(s.split()),
                "perc_special_chars": get_special_char_percentage(s),
            }
        )

    return pd.Series(
        {
            "text_length": None,
            "num_words": None,
            "max_word_length": None,
            "avg_word_length": None,
            "perc_special_chars": None,
        }
    )


def extract_column_metadata(col: pd.Series):
    col_name = col.name
    m = col.apply(get_word_data)
    m = m.rename(columns={c: f"{col_name}_{c}" for c in m.columns})

    return m
