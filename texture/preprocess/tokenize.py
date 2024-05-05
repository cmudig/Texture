import pandas as pd
from nltk.tokenize import TreebankWordTokenizer as twt
from concurrent.futures import ThreadPoolExecutor

twt_tokenizer = twt()


def get_words_w_span(text):
    if not text:
        return pd.DataFrame(columns=["span_start", "span_end", "word"])

    token_idx = twt_tokenizer.span_tokenize(text)
    _df = pd.DataFrame(token_idx, columns=["span_start", "span_end"])
    _df["word"] = _df.apply(lambda x: text[x.span_start : x.span_end], axis=1)

    return _df


def get_words_w_span_batch(arr: list[str], num_threads=8) -> list[list[str]]:
    with ThreadPoolExecutor(num_threads) as executor:
        return list(executor.map(get_words_w_span, arr))


def get_df_words_w_span(arr: list, id_col: list):
    """
    Calculate the words and their location.

    Args:
        arr (list): List of strings to tokenize.
        id_col (list): List of document ids (must be same size as arr)
    """
    result_list = get_words_w_span_batch(arr)

    for idx, _mydf in zip(id_col, result_list):
        _mydf["id"] = idx

    all_d = pd.concat(result_list, ignore_index=True)
    all_d["word"] = all_d["word"].str.lower()
    return all_d
