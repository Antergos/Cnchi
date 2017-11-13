# Set initial value for "_" to appease PyCharm
_ = lambda x: x

# Standard Lib
import argparse
import gettext
import locale
import logging
import logging.handlers
import os
import shutil
import sys
import uuid

# 3rd-Party Libs


try:
    from bugsnag.handlers import BugsnagHandler
    import bugsnag
    BUGSNAG_ERROR = None
except ImportError as err:
    BUGSNAG_ERROR = str(err)
    print("Error importing bugsnag: ", err)

# This Application
from config import ConfigLoader
from logging_utils import ContextFilter
import info
import misc.extra as misc
import show_message as show


try:
    from _cnchi_object import CnchiObject
except ImportError as err:
    logging.exception(err.msg)
    sys.exit(1)
