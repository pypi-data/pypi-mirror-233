# expose packages inside third_party
import os
import sys

import logging

# make airgen_third_party available for import
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__path__[0])), "airgen_third_party")
)


GRID_MODULE_NAME = "AirGen"

# --- setup loggers for grid -------
LOGGING_LEVEL = logging.INFO
airgen_logger = logging.getLogger(GRID_MODULE_NAME)
airgen_logger.setLevel(LOGGING_LEVEL)  # INFO
# Create a handler. You can choose StreamHandler, FileHandler, etc.
log_handler = logging.StreamHandler()
log_handler.setLevel(LOGGING_LEVEL)
# Create a formatter
log_formatter = logging.Formatter(
    "[%(name)s][%(asctime)s][%(levelname)s]-[%(filename)16s:%(lineno)4d] - %(message)s"
)
# Add the formatter to the handler
log_handler.setFormatter(log_formatter)
# Add the handler to the logger
airgen_logger.addHandler(log_handler)

# this is bad practice, we should avoid using this and get rid of this in the future
from .client import *

# from .utils import *
from .types import *

from . import utils
from . import types
from . import client
