import json
from typing import Optional, List, Any
from logging import Logger
from pypeepa.utils.loggingHandler import loggingHandler


def readJSON(file_name: str, logger: Optional[Logger] = None) -> List[Any]:
    """
    Reads a .json file and returns the result.\n
    @param: `file_name`: Name of the .json file\n
    @param: `loggingHandler`: (Optional)loggingHandler function from pypeepa.utils\n
    @return: Returns the json data in an array or empty array if any error occurs.\n
    """

    read_data = []

    try:
        with open(file_name, "r") as openfile:
            read_data = json.load(openfile)
    except FileNotFoundError:
        fnf_mssg = f"File '{file_name}' not found."
        loggingHandler(logger, fnf_mssg)
    except json.JSONDecodeError as e:
        jde_mssg = f"Error decoding JSON in '{file_name}': {e}"
        loggingHandler(logger, jde_mssg)
    except Exception as e:
        exc_mssg = f"An error occurred while reading '{file_name}': {e}"
        loggingHandler(logger, exc_mssg)

    return read_data
