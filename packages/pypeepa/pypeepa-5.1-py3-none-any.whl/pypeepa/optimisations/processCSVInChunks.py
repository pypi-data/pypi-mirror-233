import pandas as pd
from typing import Callable, Optional, TypeVar, Any, Dict
from pypeepa.checks.checkIfListIsAllNone import checkIfListIsAllNone
from pypeepa.userInteraction.progressBarIterator import progressBarIterator

ArgsType = TypeVar("ArgsType", bound=Dict)


def processCSVInChunks(
    csv_file: str,
    process_function: Callable[[pd.DataFrame, Any], Optional[pd.DataFrame]],
    pf_args: ArgsType,
    chunk_size: Optional[int] = 10000,
    hide_progress_bar: Optional[bool] = False,
):
    """
    Process any CSV file in chunks instead of whole file at once\n\n
    @param:`csv_file`: Path to the csv file.\n
    @param:`process_function`: The function containing the main processing you want to get done.\n
    @param:`pf_args`: Arguments for the function in a dict eg:-\n
                def deleteRowsInCSV(df,`pf_args`):\n
                    # ...delete rows from csv.\n
                    df=df.drop(`pf_args["delete_rows"]`)\n
                    return df\n
                processCSVInChunks("test.csv", deleteRowsInCSV, `{"delete_rows":range(1,20)}`)\n
    @param:`chunk_size`: (Optional) Size of chunks to work with\n
    @param:`hide_progress_bar`: (Optional) Set to True if you dont want the progress bar that comes with this\n
    @return:
        If the process_function has return values than return the values in a list else return None\n
    """
    # Create a generator to read the CSV file in chunks
    chunk_reader = pd.read_csv(
        csv_file,
        chunksize=chunk_size,
        low_memory=False,
        encoding_errors="ignore",
        on_bad_lines="skip",
    )

    # Process each chunk and concatenate the results
    processed_chunks = []
    # Show progress bar by default
    # Count total number of lines in the csv_file
    total_chunks = int(
        sum(1 for row in open(csv_file, "r", encoding="cp437", errors="ignore"))
        / chunk_size
    )
    for chunk in (
        chunk_reader
        if hide_progress_bar
        else progressBarIterator(chunk_reader, total_chunks, "Processing file -> ")
    ):
        processed_chunk = process_function(chunk, pf_args)
        processed_chunks.append(processed_chunk)

    if checkIfListIsAllNone(processed_chunks):
        return None

    # Concatenate the processed chunks into a single DataFrame
    df = pd.concat(processed_chunks, ignore_index=True)
    return df
