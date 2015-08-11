#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  process.py
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Format and Installation process module. """

import multiprocessing
import subprocess
import traceback
import logging

import misc.misc as misc
import pyalpm

class Process(multiprocessing.Process):
    """ Format and Installation process thread class """

    def __init__(self, install_screen, callback_queue):
        """ Initialize process class """
        multiprocessing.Process.__init__(self)

        self.callback_queue = callback_queue
        self.install_screen = install_screen

    def run(self):
        """ Calls run_format and run_install and takes care of exceptions """
        try:
            with misc.raised_privileges():
                self.install_screen.run_format()
                self.install_screen.run_install()
        except subprocess.CalledProcessError as process_error:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logging.error(_("Error running command %s"), process_error.cmd)
            logging.error(_("Output: %s"), process_error.output)
            for line in trace:
                logging.error(line)
            self.queue_fatal_event(process_error.output)
        except (misc.InstallError,
                pyalpm.error,
                KeyboardInterrupt,
                TypeError,
                AttributeError,
                OSError,
                IOError) as install_error:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logging.error(install_error)
            for line in trace:
                logging.error(line)
            self.queue_fatal_event(install_error)

    def queue_fatal_event(self, txt):
        """ Queues the fatal event and exits process """
        self.queue_event('error', txt)
        sys.exit(0)

    def queue_event(self, event_type, event_text=""):
        if self.callback_queue is not None:
            try:
                self.callback_queue.put_nowait((event_type, event_text))
            except queue.Full:
                pass
        else:
            print("{0}: {1}".format(event_type, event_text))
