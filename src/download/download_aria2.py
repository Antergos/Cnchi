#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  download_aria2.py
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

""" Module to download packages using Aria2 """

import os
import subprocess
import logging
import xmlrpc.client
import queue

import aria2
import pacman.pac as pac

MAX_CONCURRENT_DOWNLOADS = 1

class Download(object):
    """ Class to download packages using Aria2
        This class tries to previously download all necessary packages for
        Antergos installation using aria2 """

    def __init__(self, pacman_cache_dir, cache_dir, callback_queue):
        """ Initialize DownloadAria2 class. Gets default configuration """
        self.pacman_cache_dir = pacman_cache_dir
        self.cache_dir = cache_dir
        self.callback_queue = callback_queue

        # Stores last issued event (to prevent repeating events)
        self.last_event = {}

        self.rpc_uid = aria2.run_as_daemon()

    '''
    def start(self, downloads):
        """ Downloads using aria2 """

        # FIXME: As it is now, this does not differ from downloading with urllib one file at a time
        # For that, this method only works if MAX_CONCURRENT_DOWNLOADS value is 1

        if MAX_CONCURRENT_DOWNLOADS is not 1:
            logging.error("Our Aria2 code still does not support concurrent downloads")
            return

        try:
            keys = ["gid", "status", "totalLength", "completedLength", "files"]

            for package_name in package_names:
                metalink = ml.create(pacman, package_name, self.pacman_conf_file)
                if metalink == None:
                    logging.error(_("Error creating metalink for package %s"), package_name)
                    continue

                gids = self.add_metalink(metalink)

                if len(gids) <= 0:
                    logging.error(_("Error adding metalink for package %s"), package_name)
                    continue

                # Get global statistics
                global_stat = self.get_global_stat()

                # Get num of active downloads
                num_active = int(global_stat["numActive"])

                old_percent = -1
                old_path = ""

                action = _("Downloading package '%s' and its dependencies...") % package_name
                self.queue_event('info', action)

                while num_active > 0:
                    result = self.tell_active(keys)

                    total_length = 0
                    completed_length = 0

                    try:
                        for i in range(0, num_active - 1):
                            total_length += int(result[i]['totalLength'])
                            completed_length += int(result[i]['completedLength'])

                        # As MAX_CONCURRENT_DOWNLOADS value is 1 we can be sure that only
                        # one file is downloaded at a time

                        # path will store full file name (destination)
                        path = result[0]['files'][0]['path']
                    except Exception as err:
                        logging.error(err)

                    percent = round(float(completed_length / total_length), 2)

                    if path != old_path and percent == 0:
                        old_path = path
                        # Update download file name
                        path = os.path.basename(path)
                        # Do not show the package's extension to the user
                        ext = ".pkg.tar.xz"
                        if path.endswith(ext):
                            path = path[:-len(ext)]

                        self.queue_event('info', _("Downloading %s...") % path)

                    if percent != old_percent:
                        self.queue_event('percent', percent)
                        old_percent = percent

                    # Get global statistics
                    global_stat = self.get_global_stat()

                    # Get num of active downloads
                    num_active = int(global_stat["numActive"])

                # This method purges completed/error/removed downloads, in order to free memory
                self.purge_download_result()

            # Finished, close aria2
            self.shutdown()
        except Exception as err:
            logging.error(err)
    '''

    def start(self, downloads):
        """ Downloads using aria2 """

        downloaded = 0
        total_downloads = len(downloads)

        self.queue_event('downloads_progress_bar', 'show')
        self.queue_event('downloads_percent', 0)

        keys = ["gid", "status", "totalLength", "completedLength", "files"]

        total_size = 0

        for element in downloads:
            total_size += int(element['size'])

        while len(downloads) > 0:
            max_num = MAX_CONCURRENT_DOWNLOADS
            if len(downloads) < max_num:
                max_num = len(downloads)

            # Get num of active downloads
            num_active = int(global_stat["numActive"])

            if num_active < 1:
                # Let's queue more downloads
                for i in range(0, max_num - 1):
                    element = downloads.pop()
                    gid = self.add_uris(element['urls'])

                # Get global statistics
                global_stat = self.get_global_stat()

            # Get num of active downloads
            num_active = int(global_stat["numActive"])

            if num_active > 0:
                result = self.tell_active(keys)

                total_length = 0
                completed_length = 0

                    try:
                        for i in range(0, num_active - 1):
                            total_length += int(result[i]['totalLength'])
                            completed_length += int(result[i]['completedLength'])

                        # As --max-concurrent-downloads=1 we can be sure only one file is downloaded at a time
                        # path will store full file name (destination)
                        path = result[0]['files'][0]['path']
                    except Exception as err:
                        logging.error(err)

                    percent = round(float(completed_length / total_length), 2)

                    if path != old_path and percent == 0:
                        old_path = path
                        # Update download file name
                        path = os.path.basename(path)
                        # Do not show the package's extension to the user
                        ext = ".pkg.tar.xz"
                        if path.endswith(ext):
                            path = path[:-len(ext)]

                        self.queue_event('info', _("Downloading %s...") % path)

                    if percent != old_percent:
                        self.queue_event('percent', percent)
                        old_percent = percent

                    # Get global statistics
                    global_stat = self.get_global_stat()

                    # Get num of active downloads
                    num_active = int(global_stat["numActive"])

                # This method purges completed/error/removed downloads, in order to free memory
                self.purge_download_result()

            # Finished, close aria2
            self.shutdown()
        except Exception as err:
            logging.error(err)


    def queue_event(self, event_type, event_text=""):
        """ Adds an event to Cnchi event queue """
        if self.callback_queue is None:
            logging.debug(event_text)
            return

        if event_type in self.last_event:
            if self.last_event[event_type] == event_text:
                # do not repeat same event
                return

        self.last_event[event_type] = event_text

        try:
            self.callback_queue.put_nowait((event_type, event_text))
        except queue.Full:
            pass

if __name__ == '__main__':
    ''' Test case '''
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

    #DownloadAria2(package_names=["gnome-sudoku"], cache_dir="", pacman_cache_dir="/tmp/aria2")
    DownloadAria2(package_names=["alsa-utils"], cache_dir="", pacman_cache_dir="/tmp/aria2")
    #DownloadAria2(package_names=["base"], cache_dir="", pacman_cache_dir="/tmp/aria2")

    #DownloadAria2(package_names=["gnome-software"], pacman_cache_dir="/tmp/aria2")
    #DownloadAria2(package_names=["base", "base-devel"], pacman_cache_dir="/tmp/aria2")
