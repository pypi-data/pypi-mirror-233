import os
import pandas
from typing import Literal


def writeFile(
    data_to_write: pandas.DataFrame,
    file_path: str,
    file_name: str,
    file_type: Literal["csv", "xlsx", "json"],
):
    file = file_path + file_name + "." + file_type
    # Create output directory if it doesnt exist
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        print("\nDirectory created in your documents:", file_path)
    try:
        if file_type == "xlsx":
            # writing to excel file using openpyxl
            with pandas.ExcelWriter(file, engine="openpyxl") as writer:
                data_to_write.to_excel(writer, "spreadsheet1")
        elif file_type == "csv":
            data_to_write.to_csv(file)
        elif file_type == "json":
            json_string = data_to_write.to_json(orient="records")
            with open(file, "w") as json_file:
                json_file.write(json_string)
        else:
            raise Exception("Unsupported file_type. Use 'csv', 'xlsx', or 'json'.")

        print("\nOutput file saved to:", file)

    except Exception as exc:
        raise Exception("\nFailed to save output file!", exc)
