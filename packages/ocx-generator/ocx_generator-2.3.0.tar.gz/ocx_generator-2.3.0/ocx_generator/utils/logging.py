#  Copyright (c) 2023. OCX Consortium https://3docx.org. See the LICENSE
# System imports
import warnings
import logging
from loguru import logger
from xsdata.utils.click import LogHandler

logger.disable(__name__)

# Log warnings as well
showwarning_ = warnings.showwarning


def showwarning(message, *args, **kwargs):
    logger.warning(message)
    showwarning_(message, *args, **kwargs)


class LoguruHandler(LogHandler):
    """Override the xsData LogHandler class for integration with loguru."""

    @logger.catch
    def emit(self, record: logging.LogRecord):
        if record.levelno > logging.INFO:
            logger.warning(record)
        else:
            logger.error(record)

    def emit_warnings(self):
        pass
