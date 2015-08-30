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


""" Format and Installation process module. """

import multiprocessing
import subprocess
import traceback
import logging
import sys
import misc.misc as misc
import pyalpm
from download import download

from installation import select_packages as pack


class Process(multiprocessing.Process):
    """ Format and Installation process thread class """

    def __init__(self, install_screen, settings, callback_queue):
        """ Initialize process class """
        multiprocessing.Process.__init__(self)
        self.settings = settings
        self.callback_queue = callback_queue
        self.install_screen = install_screen

    def create_downloads_list(self, package_list):
        # download_packages = download.DownloadPackages(package_list)
        # download_packages.create_downloads_list()
        pass

    def run(self):
        """ Calls run_format and run_install and takes care of exceptions """

        try:
            # Before formatting, let's try to calculate package download list
            # this way, if something fails (a missing package, mostly) we have
            # not formatted anything yet.
            # TODO: package list is created in install.py. We need to break that
            # file so select_packages() can be run BEFORE formatting (it could be
            # run here in process.py)
            # self.create_downloads_list()

            pkg = pack.SelectPackages(self.settings, self.callback_queue)
            pkg.create_package_list()

            with misc.raised_privileges():
                self.install_screen.run_format()
                self.install_screen.run_install(pkg.packages)
        except subprocess.CalledProcessError as process_error:
            txt = "Error running command {0}: {1}".format(process_error.cmd, process_error.output)
            logging.error(txt)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            for line in trace:
                logging.error(line.rstrip())
            txt = _("Error running command {0}: {1}").format(process_error.cmd, process_error.output)
            self.queue_fatal_event(txt)
        except (misc.InstallError,
                pyalpm.error,
                KeyboardInterrupt,
                TypeError,
                AttributeError,
                OSError,
                IOError) as install_error:
            logging.error(install_error)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            for line in trace:
                logging.error(line.rstrip())
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
