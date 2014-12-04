#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  download.py
#
#  Copyright © 2013,2014 Antergos
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

""" Module to download packages using Aria2 or urllib """

import os
import logging
import queue

if __name__ == '__main__':
    import sys
    # Insert the parent directory at the front of the path.
    # This is used only when we want to test
    base_dir = os.path.dirname(__file__) or '.'
    parent_dir = os.path.join(base_dir, '..')
    sys.path.insert(0, parent_dir)

import pacman.pac as pac

try:
    import download.metalink as ml
    import download.download_urllib as download_urllib
    import download.download_aria2 as download_aria2
except ImportError as err:
    # when testing download.py
    import metalink as ml
    import download_urllib
    import download_aria2

class DownloadPackages(object):
    """ Class to download packages using Aria2 or urllib
        This class tries to previously download all necessary packages for
        Antergos installation using aria2 or urllib
        Aria2 is known to use too much memory (not Aria2's fault but ours)
        so until it's fixed it it's not advised to use it """

    def __init__(
        self,
        package_names,
        use_aria2=False,
        pacman_conf_file=None,
        pacman_cache_dir=None,
        cache_dir=None,
        callback_queue=None):
        """ Initialize DownloadPackages class. Gets default configuration """

        if pacman_conf_file == None:
            self.pacman_conf_file = "/etc/pacman.conf"
        else:
            self.pacman_conf_file = pacman_conf_file

        if pacman_cache_dir == None:
            self.pacman_cache_dir = "/var/cache/pacman/pkg"
        else:
            self.pacman_cache_dir = pacman_cache_dir

        if cache_dir == None:
            self.cache_dir = ""
        else:
            self.cache_dir = cache_dir

        # Create pacman cache dir if it doesn't exist yet
        if not os.path.exists(pacman_cache_dir):
            os.makedirs(pacman_cache_dir)

        # Stores last issued event for each event type
        # (to prevent repeating events)
        self.last_event = {}

        self.callback_queue = callback_queue

        # Create downloads list from package list
        downloads = self.get_downloads_list(package_names)

        if downloads is None:
            return

        if use_aria2:
            try:
                import download.download_aria2 as download_aria2
            except ImportError as err:
                import download_aria2
            logging.debug(_("Using aria2 to download packages"))
            download = download_aria2.Download(
                pacman_cache_dir,
                cache_dir,
                callback_queue)
        else:
            logging.debug(_("Using urlib to download packages"))
            download = download_urllib.Download(
                pacman_cache_dir,
                cache_dir,
                callback_queue)

        download.start(downloads)

    def get_downloads_list(self, package_names):
        """ Creates a downloads list from the package list """
        self.queue_event('percent', 0)
        self.queue_event('info', _('Creating list of packages to download...'))
        percent = 0
        processed_packages = 0
        total_packages = len(package_names)

        downloads = {}

        pacman = None

        try:
            pacman = pac.Pac(
                conf_path=self.pacman_conf_file,
                callback_queue=self.callback_queue)
        except Exception as err:
            logging.error(_("Can't initialize pyalpm: %s"), err)

        if pacman is None:
            return None

        try:
            for package_name in package_names:
                metalink = ml.create(pacman, package_name, self.pacman_conf_file)
                if metalink == None:
                    logging.error(_("Error creating metalink for package %s"), package_name)
                    continue

                # Get metalink info
                metalink_info = ml.get_info(metalink)

                # Update downloads list with the new info from the processed metalink
                for key in metalink_info:
                    if key not in downloads:
                        downloads[key] = metalink_info[key]

                # Show progress to the user
                processed_packages += 1
                percent = round(float(processed_packages / total_packages), 2)
                self.queue_event('percent', percent)
        except Exception as err:
            logging.error(_("Can't create download set: %s"), err)
            return None

        try:
            pacman.release()
            del pacman
        except Exception as err:
            logging.error(_("Can't release pyalpm: %s"), err)

        return downloads

    def queue_event(self, event_type, event_text=""):
        """ Adds an event to Cnchi event queue """

        if self.callback_queue is None:
            if event_type != "percent":
                logging.debug(event_type + " : " + str(event_text))
            return

        if event_type in self.last_event:
            if self.last_event[event_type] == event_text:
                # do not repeat same event
                return

        self.last_event[event_type] = event_text

        try:
            # Add the event
            self.callback_queue.put_nowait((event_type, event_text))
        except queue.Full:
            pass

''' Test case '''
if __name__ == '__main__':
    import gettext
    _ = gettext.gettext

    formatter = logging.Formatter(
        '[%(asctime)s] [%(module)s] %(levelname)s: %(message)s',
        "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    DownloadPackages(
        package_names=["gnome-sudoku"],
        #use_aria2=False,
        use_aria2=True,
        cache_dir="",
        pacman_cache_dir="/tmp/pkg")

    '''
    DownloadPackages(
        package_names=["kde"],
        use_aria2=False,
        cache_dir="",
        pacman_cache_dir="/tmp/pkg")
    '''
