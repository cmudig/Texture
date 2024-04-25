import pandas as pd


def execute_code_and_apply_function(code_str: str, series: pd.Series) -> pd.Series:
    """
    Execute the code string and apply the function to the series.

    Args:
        code_str (str): The code string. Should define a function called transform.
        series (pd.Series): The series to apply the function to.
    """

    # use the same dict for local and global context so that helper functions can be accessed
    # FUTURE: probably want to use this for imports like context = {"pd": pd}
    context = {}

    exec(code_str, context, context)
    t = context["transform"]
    result = t(series)

    return result
