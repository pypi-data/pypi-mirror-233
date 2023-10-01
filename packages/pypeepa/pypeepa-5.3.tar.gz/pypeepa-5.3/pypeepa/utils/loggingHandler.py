from logging import Logger
from typing import Optional


def loggingHandler(logger: Optional[Logger], log_mssg):
    """Handles logging using pythons native logging support and also prints it on the console, can be used instead of print() function.\n
    @param: `logger`:(Optional) Provide a initialised logger object to log the log_mssg.\n
    @param: `log_mssg`: The message you want to print or log.
    """
    if logger != None:
        logger.log(logger.level, log_mssg)
    print(log_mssg)
