from pypeepa.fileInteraction.readJSON import readJSON  # check
from pypeepa.utils.loggingHandler import loggingHandler  # check
from pypeepa.fileInteraction.createDirectory import createDirectory
from pypeepa.userInteraction.askYNQuestion import askYNQuestion
from typing import Optional, Iterable, Any
from logging import Logger
import json
import os


class ProgressSaver:
    """
    Saves any kind of state in an array.\n
    @init\n
        @param: `app_name`: Name of the file where the progress states will be saved in.\n
    @func: `saveToJSON`: Append the progress state to an array containing previous states and save to `app_name`.save.json\n
        @param: `new_data`: Data to save.\n
        @param: `name`: (Optional)If the save state has any name, it will be used for logging.\n
        @param: `logger` (Optional)A logger object to enable logging.\n
    @func `resetSavedData`: Resets the progress\n
        @param: `logger` (Optional)A logger object to enable logging.\n
    @func `askToContinue`: Ask the user if they want to continue from before or not.\n
        @param: `logger` (Optional)A logger object to enable logging.\n
    """

    def __init__(self, app_name) -> None:
        self.save_directory = f"saves"
        self.save_file_name = os.path.join(self.save_directory, f"{app_name}.save.json")
        self.saved_data: Iterable[Any] = readJSON(self.save_file_name)

    def saveToJSON(
        self, new_data: Any, name: Optional[str] = None, logger: Optional[Logger] = None
    ):
        self.saved_data.append(new_data)
        createDirectory(self.save_directory)  # Create directory if it doesnt exist
        with open(self.save_file_name, "w+") as completed_output:
            loggingHandler(
                logger, f"Saving file: -> {name}" if name else "Saving file!"
            )
            json.dump(self.saved_data, completed_output)

    def resetSavedData(self, logger: Optional[Logger] = None):
        self.saved_data = []
        with open(self.save_file_name, "w+") as completed_output:
            loggingHandler(logger, f"Clearing saved progress!")
            json.dump(self.saved_data, completed_output)

    def askToContinue(self, logger: Optional[Logger] = None):
        if len(self.saved_data) > 0:
            continue_from_before = askYNQuestion("Continue from before?(y/n)")
            if not continue_from_before:
                self.resetSavedData(logger)
