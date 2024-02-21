from functools import wraps
import time


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
    mapped_results = [obj[colName] if colName in obj else None for obj in results]

    processed_results = []

    for obj in mapped_results:
        if isinstance(obj, list):
            if len(obj) > 0:
                processed_results.append(",".join(obj))
            else:
                processed_results.append(None)
        elif isinstance(obj, str):
            processed_results.append(obj if len(obj) > 0 else None)
        elif isinstance(obj, bool):
            processed_results.append(obj)
        else:
            print("Did not parse: ", obj)
            processed_results.append(None)

    return processed_results
