#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  logging_color.py
#
#  Copyright © 2013-2017 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

""" Logger Formatter that uses colors in output """

import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30

class ColoredFormatter(logging.Formatter):
    """ Log formatter class that adds colors to logging messages """

    # These are the sequences need to get colored ouput
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"

    COLORS = {
        'WARNING': YELLOW, 'INFO': WHITE, 'DEBUG': BLUE, 'CRITICAL': YELLOW, 'ERROR': RED}

    def __init__(self, fmt, datefmt, use_color=True):
        msg = self.formatter_message(fmt)
        logging.Formatter.__init__(self, fmt=msg, datefmt=datefmt)
        self.use_color = use_color

    @staticmethod
    def formatter_message(message, use_color=True):
        """ Formats message adding colors """
        if use_color:
            message = message.replace("$RESET", ColoredFormatter.RESET_SEQ)
            message = message.replace("$BOLD", ColoredFormatter.BOLD_SEQ)
        else:
            message = message.replace("$RESET", "").replace("$BOLD", "")
        return message

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in ColoredFormatter.COLORS:
            levelname_color = ColoredFormatter.COLOR_SEQ % (
                30 + ColoredFormatter.COLORS[levelname]) + levelname + ColoredFormatter.RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)
