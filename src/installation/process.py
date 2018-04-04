#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# process.py
#
# Copyright © 2013-2017 Antergos
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


""" Format and Installation process module. """

import multiprocessing
import subprocess
import traceback
import logging
import sys
import queue

import pyalpm

import misc.extra as misc

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
        self.pkg = None
        self.down = None

    def create_metalinks_list(self):
        """ Create metalinks list """
        self.pkg = pack.SelectPackages(self.settings, self.callback_queue)
        self.pkg.create_package_list()

        if not self.pkg.packages:
            txt = _("Cannot create package list.")
            raise misc.InstallError(txt)

        # Won't download anything here. It's just to create the metalinks list
        self.down = download.DownloadPackages(
            package_names=self.pkg.packages,
            pacman_conf_file='/etc/pacman.conf',
            pacman_cache_dir='/var/cache/pacman/pkg',
            settings=self.settings,
            callback_queue=self.callback_queue)

        # Create metalinks list
        self.down.create_metalinks_list()

        if not self.down.metalinks:
            txt = _("Cannot create download package list (metalinks).")
            raise misc.InstallError(txt)

    def prepare_lembrame(self):
        if self.settings.get("feature_lembrame"):
            logging.debug("Preparing Lembrame files")
            from lembrame.lembrame import Lembrame

            self.queue_event('pulse', 'start')
            self.queue_event('info', _("Downloading Lembrame file with your synced configuration"))

            lembrame = Lembrame(self.settings)
            lembrame_download_status = lembrame.download_file()

            if lembrame_download_status:
                self.queue_event('info', _("Decrypting your Lembrame file"))
                logging.debug("Setting up Lembrame configurations")
                lembrame.setup()
            self.queue_event('info', _("Initializing package downloading"))
            self.queue_event('pulse', 'stop')

    def run(self):
        """ Calculates download package list and then calls run_format and
        run_install. Takes care of the exceptions, too. """

        try:
            # Start Lembrame download package if activated. We'll need the package list to
            # overwrite the one used by the installer by default
            self.prepare_lembrame()

            # Before formatting, let's try to calculate package download list
            # this way, if something fails (a missing package, mostly) we have
            # not formatted anything yet.
            self.create_metalinks_list()

            self.queue_event(
                'info', _("Getting your disk(s) ready for Antergos..."))
            with misc.raised_privileges() as __:
                self.install_screen.run_format()

            path = "/tmp/.cnchi_partitioning_completed"
            with open(path, 'w') as part_file:
                part_file.write("# File created by Cnchi to force\n")
                part_file.write("# users to reboot before retry\n")
                part_file.write("# formatting their hard disk(s)\n")

            self.queue_event('info', _("Installation will start now!"))
            with misc.raised_privileges() as __:
                self.install_screen.run_install(
                    self.pkg.packages, self.down.metalinks)
        except subprocess.CalledProcessError as process_error:
            txt = "Error running command {0}: {1}".format(
                process_error.cmd,
                process_error.output)
            logging.error(txt)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            for line in trace:
                logging.error(line.rstrip())
            txt = _("Error running command {0}: {1}").format(
                process_error.cmd,
                process_error.output)
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
            trace = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            for line in trace:
                logging.error(line.rstrip())
            self.queue_fatal_event(install_error)

    def queue_fatal_event(self, txt):
        """ Enqueues a fatal event and exits process """
        self.queue_event('error', txt)
        sys.exit(0)

    def queue_event(self, event_type, event_text=""):
        """ Enqueue an event """
        if self.callback_queue is not None:
            try:
                self.callback_queue.put_nowait((event_type, event_text))
            except queue.Full:
                pass
        else:
            print("{0}: {1}".format(event_type, event_text))
