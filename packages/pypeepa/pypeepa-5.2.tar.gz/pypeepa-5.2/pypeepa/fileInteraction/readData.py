import pandas
import warnings


def readData(file_path: str) -> pandas.DataFrame:
    try:
        warnings.filterwarnings("error", category=pandas.errors.DtypeWarning)
        # Get the data from file
        # TODO convert to stream read
        if file_path.endswith(".csv"):
            read_data = pandas.read_csv(f"""{file_path}""")
        elif file_path.endswith(".xlsx"):
            read_data = pandas.read_excel(f"""{file_path}""")
        elif file_path.endswith(".json"):
            read_data = pandas.read_json(f"""{file_path}""")
        warnings.resetwarnings()
    except pandas.errors.DtypeWarning as pe:
        raise Exception(
            "Error encountered while reading the file: " + pe.args[0]
        ) from pe
    except Exception as exc:
        raise Exception("Error reading the file in " + file_path, exc)
    return read_data


def getColumnHeaders(df: pandas.DataFrame) -> list:
    columns = list(df.columns)
    return columns
