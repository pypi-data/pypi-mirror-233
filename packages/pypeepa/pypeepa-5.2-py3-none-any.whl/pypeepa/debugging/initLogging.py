import logging
import os
from pypeepa.fileInteraction.createDirectory import createDirectory


def initLogging(app_name, level="INFO"):
    """
    Initialise Logging in your app
    @params: `app_name`:Name of your app\n\n
    @params: `level`:
        `DEBUG`: logging.DEBUG,\n
        `INFO`:(Default)logging.INFO,\n
        `WARNING`: logging.WARNING,\n
        `WARN`: logging.WARNING,\n
        `ERROR`: logging.ERROR,\n
        `CRITICAL`: logging.CRITICAL,\n
        `FATAL`: logging.CRITICAL,\n
    @return: Returns a logger object that you can use wherever you need to log.
    """

    level_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
        "FATAL": logging.CRITICAL,
    }

    if level not in level_mapping:
        raise ValueError("Invalid log level specified")

    level_in_int = level_mapping[level]

    # Initialize logging
    log_directory = f"logs"
    save_file_name = os.path.join(log_directory, f"ExceptionLogs-{app_name}.log")
    createDirectory(log_directory)
    logging.basicConfig(
        filename=save_file_name,
        format="%(asctime)s %(message)s",
    )

    logger = logging.getLogger()
    logger.setLevel(level_in_int)
    logger.info(f"------------------{app_name} initialised!------------------")

    return logger
