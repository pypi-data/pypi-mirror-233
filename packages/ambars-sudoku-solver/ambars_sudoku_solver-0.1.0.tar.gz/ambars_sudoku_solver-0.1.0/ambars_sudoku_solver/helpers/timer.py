import time
from typing import Callable


def timer(func: Callable) -> Callable:
    def timer_wrapper(*args, **kwargs):
        start: float = time.perf_counter()
        result: Callable = func(*args, **kwargs)
        stop: float = time.perf_counter()
        print(f"{func.__name__}: {stop - start:.2f}s to excute.")
        return result

    return timer_wrapper
