from typing import List, Tuple, Optional
from pandas import read_csv
import numpy
import os
from pypeepa.userInteraction.askSelectOptionQuestion import askSelectOptionQuestion
from pypeepa.userInteraction.printArray import printArray


def askHeaderForMultipleCSV(
    csv_list: List[str], csv_dir: str, label: Optional[str] = "values"
) -> List[Tuple[str, str]]:
    """Ask the user to select headers for many csv files, it will skip repeated sets of headers
    @param:`csv_list`:List of csv file names.
    @param:`csv_dir`:The directory of the csvs.
    @param:`label`:A general label which will be displayed to the user for the specific type of column.
    @return: Returns a list of tuples containing the csv file name and the selected header name
    """
    files_and_header = []
    prev_cols = []
    col_index = None
    for csv_file in csv_list:
        csv_full_path = os.path.join(csv_dir, csv_file)
        current_columns = read_csv(
            csv_full_path, nrows=1, encoding_errors="ignore", encoding="cp437"
        ).columns
        if not numpy.array_equal(numpy.array(prev_cols), numpy.array(current_columns)):
            printArray(current_columns)
            col_index = askSelectOptionQuestion(
                question=f"Enter the index of the column containing the {label}.",
                min=1,
                max=len(current_columns),
            )
            prev_cols = current_columns
        col_name = current_columns[col_index - 1]
        files_and_header.append((csv_full_path, col_name))

    return files_and_header
