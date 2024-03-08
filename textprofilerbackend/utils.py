from functools import wraps
import time
from textprofilerbackend.models import DataType


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


def process_results(results, colName):
    mapped_results = map_results(results, colName)

    processed_results = []

    for obj in mapped_results:
        if isinstance(obj, list):
            # FUTURE might handle this differently depending on array handling
            if len(obj) > 0:
                processed_results.append(",".join(obj))
            else:
                processed_results.append(None)
        elif isinstance(obj, str):
            processed_results.append(obj if len(obj) > 0 else None)
        elif isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, float):
            processed_results.append(obj)
        else:
            print("Did not parse: ", obj)
            processed_results.append(None)

    return processed_results


def map_results(results, colName):
    mapped = []
    for item in results:
        try:
            mapped.append(item[colName])
        except Exception as e:
            mapped.append(None)

    return mapped


def get_type_from_response(inputType) -> DataType:
    """input type is number, string, or bool from llm response format"""
    if inputType == "number":
        return "number"

    return "categorical"
