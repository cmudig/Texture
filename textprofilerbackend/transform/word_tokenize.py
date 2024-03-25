import nltk
from nltk.tokenize import TreebankWordTokenizer as twt
import tiktoken
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

encoding = tiktoken.get_encoding("cl100k_base")

# NLTK stuff
# def get_word_tokens(arr) -> list:
#     """Split array of strings into word tokens using nltk.
#     Returns: 2d array of strings"""
#     return [nltk.word_tokenize(s) for s in arr]


def get_word_tokens_batch(arr: list[str], num_threads=8) -> list[list[str]]:
    """Split array of strings into word tokens using nltk.
    Returns: 2d array of strings"""
    with ThreadPoolExecutor(num_threads) as executor:
        return list(executor.map(nltk.word_tokenize, arr))


def get_number_encoding_batch(arr: list[str]) -> list[list[int]]:
    """Split array of strings into word tokens using tiktoken.
    Returns: 2d array of numbers"""
    return encoding.encode_batch(arr)


# def get_byte_arr(num_arr: list[int]) -> list:
#     return [encoding.decode_single_token_bytes(token) for token in num_arr]


def encode_as_bytes(s: str) -> list[bytes]:
    """Use tiktoken to get number tokens for string then convert to string bytes.
    Returns a byte string array"""
    return [encoding.decode_single_token_bytes(c) for c in encoding.encode(s)]


def get_byte_encoding_batch(arr: list[str], num_threads=8) -> list[list[bytes]]:
    with ThreadPoolExecutor(num_threads) as executor:
        return list(executor.map(encode_as_bytes, arr))


twt_tokenizer = twt()


def get_words_w_span(text):
    token_idx = twt_tokenizer.span_tokenize(text)
    _df = pd.DataFrame(token_idx, columns=["span_start", "span_end"])
    _df["word"] = _df.apply(lambda x: text[x.span_start : x.span_end], axis=1)

    return _df


def get_words_w_span_batch(arr: list[str], num_threads=8) -> list[list[str]]:
    with ThreadPoolExecutor(num_threads) as executor:
        return list(executor.map(get_words_w_span, arr))


def get_df_words_w_span(arr: list, id_col: list, lower_case=True):
    """
    Calculate the words and their location.

    Args:
        arr (list): List of strings to tokenize.
        id_col (list): List of document ids (must be same size as arr)
    """
    r = get_words_w_span_batch(arr)

    for idx, _mydf in zip(id_col, r):
        _mydf["id"] = idx

    df_all = pd.concat(r, ignore_index=True)

    if lower_case:
        df_all["word"] = df_all["word"].str.lower()

    return df_all
