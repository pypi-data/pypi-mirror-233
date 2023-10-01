import concurrent.futures
import time
import psutil
from typing import Optional, Callable, Any, Iterable
from pypeepa.utils.loggingHandler import loggingHandler  # check
import logging
from functools import partial


def concurrentFutures(
    process_function: Callable[[Any], Any],
    divided_tasks: Iterable[Any],
    additional_args: Optional[tuple] = (),
    thread_executor: Optional[bool] = False,  # Default to "process" executor
    max_workers: Optional[int] = 4,
    logger: Optional[logging.Logger] = None,
):
    """
    Wrapper function to run multiple instances of the same function parallely,\n


    @param: `process_function`: The function that contains your processing logic.\n
    @param: `divided_tasks`:  The parameters for the process_function, It contains the divided tasks parameters in an Iterable.\n
    @param: `additional_args`: (Optional) Any additional args you want to pass to process_function\n
    @param: `thread_executor`: (Optional) If True then ThreadPoolExcecutor will be used.\n
    @param: `max_workers`: (Optional) The maximum number of parallel processes/threads.\n
    @param: `logger`: (Optional) You can pass a logging object if you already initialized one.\n


    @return: Returns the results in an array if there are any return values to the process_function
    """
    start = time.time()

    executor_class = (
        concurrent.futures.ProcessPoolExecutor
        if thread_executor == False
        else concurrent.futures.ThreadPoolExecutor
    )

    results = []  # To store results from process_function

    with executor_class(max_workers=max_workers) as executor:
        futures = []
        for task in divided_tasks:
            partial_func = partial(process_function, task, *additional_args)
            future = executor.submit(partial_func)
            futures.append((task, future))

        for task, future in futures:
            try:
                # Start measuring time
                start_time = time.time()

                # Get the result from the future
                result = future.result()
                results.append(result)
                # Print memory usage
                process = psutil.Process()
                memory_usage = process.memory_info().rss / (1024 * 1024)  # in megabytes
                # Calculate time_taken
                time_taken = time.time() - start_time

                loggingHandler(
                    logger=logger,
                    log_mssg="Start: {}, Time taken: {}s, Memory usage:, {}, MB".format(
                        task, time_taken, memory_usage
                    ),
                )
            except Exception as e:
                loggingHandler(
                    logger=logger,
                    log_mssg="Error occurred on task: {} --> Error Report: {}".format(
                        task, e
                    ),
                )

    loggingHandler(
        logger=logger, log_mssg="Total time taken: {}s".format(time.time() - start)
    )

    return results
