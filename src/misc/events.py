#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# events.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

""" Events module, used to store events in log and show them to the user """

import inspect
import queue
import logging
import sys

class Events():
    """ Class that will store events, log them and show them to the user """
    def __init__(self, callback_queue):
        self.queue = callback_queue
        self.last_event = {}

    def add(self, event_type, event_text=""):
        """ Queues events to the event list in the GUI thread """

        if event_type == "percent":
            try:
                event_text = float(event_text)
                # Limit percent to two decimals
                event_text = "{0:.2f}".format(event_text)
            except ValueError:
                msg = "{} cannot be converted to a float number".format(event_text)
                logging.warning(msg)

        if event_type in self.last_event:
            if self.last_event[event_type] == event_text:
                # Do not enqueue the same event twice
                return

        self.last_event[event_type] = event_text

        if event_type == "error":
            # Format message to show file, function, and line where the
            # error was issued. We get the previous frame in the stack,
            # otherwise it would be this function
            func = inspect.currentframe().f_back.f_code
            # Dump the message + the name of this function to the log.
            event_text = "{0}: {1} in {2}:{3}".format(
                event_text, func.co_name, func.co_filename, func.co_firstlineno)

        if self.queue is None:
            if event_type == 'error':
                logging.error(event_text)
            elif event_type == 'warning':
                logging.warning(event_text)
            else:
                logging.debug(event_text)
        else:
            try:
                self.queue.put_nowait((event_type, event_text))
            except queue.Full:
                logging.warning("Callback queue is full")

    def add_fatal(self, event_text=""):
        """ Adds an error event to Cnchi event queue and quits """
        self.add('error', event_text)
        self.queue.join()
        sys.exit()
