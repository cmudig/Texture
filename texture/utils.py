from functools import wraps
import time
from texture.models import DataType
import pandas as pd


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        print(f"{func.__name__} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


def get_type_from_response(inputType) -> DataType:
    """input type is number, string, or bool from llm response format"""
    if inputType == "number":
        return "number"

    return "categorical"


def flatten(col: pd.Series, idColName="id"):
    """flatten a series with arrays into a dataframe with one entry per row"""
    col = col.explode()
    col = col.reset_index()
    col = col.rename(columns={"index": idColName})

    return col


def is_notebook() -> bool:
    try:
        from IPython.core.getipython import get_ipython

        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except (NameError, ImportError):
        return False  # Probably standard Python interpreter
