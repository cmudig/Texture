from pathlib import Path
import torch
import time


# ~~~~~~~~ Timer utils ~~~~~~~~


def timer_print(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} ran in {end_time - start_time} seconds")
        return result

    return wrapper
