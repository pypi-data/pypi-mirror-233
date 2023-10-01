from pypeepa.utils.loggingHandler import loggingHandler  # check
from typing import Callable, Any, Optional
from logging import Logger
import time


def measureTimeToRun(func: Callable[[Any], Any], logger: Optional[Logger] = None):
    """
    Times any function wrapped with it and if a logger is provided logs it.
    @param: `func`: the function to time.
    @param: `logger`: The Logger object
    @return:
        The result from the function or the None if no result
    """

    def wrapper(*args, **kwargs):
        tick = time.time()
        result = func(*args, **kwargs)
        loggingHandler(logger, f"Time taken for {func.__name__}: {time.time()-tick}")
        if result != None:
            return result

    return wrapper
