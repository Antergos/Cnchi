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

try:
    _("")
except NameError as err:
    def _(message): return message

MAX_CONCURRENT_DOWNLOADS = 4

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

        self.aria2 = aria2.Aria2(pacman_cache_dir, MAX_CONCURRENT_DOWNLOADS)

    def start(self, downloads):
        """ Downloads using aria2 """

        downloaded = 0
        total_downloads = len(downloads)
        downloads_percent = 0

        self.queue_event('downloads_progress_bar', 'show')
        self.queue_event('downloads_percent', 0)

        #keys = ["gid", "status", "totalLength", "completedLength", "files"]

        # start Aria2
        self.aria2.run()

        while len(downloads) > 0:
            # Get num of active downloads
            global_stat = self.aria2.get_global_stat()
            num_active = int(global_stat["numActive"])

            while num_active < MAX_CONCURRENT_DOWNLOADS and len(downloads) > 0:
                identity, element = downloads.popitem()

                #dst_cache_path = os.path.join(self.cache_dir, element['filename'])
                #dst_path = os.path.join(self.pacman_cache_dir, element['filename'])

                gid = self.aria2.add_uris(element['urls'])
                global_stat = self.aria2.get_global_stat()
                num_active = int(global_stat["numActive"])

            old_num_active = num_active

            old_downloads_percent = downloads_percent
            while num_active > 0:
                global_stat = self.aria2.get_global_stat()
                num_active = int(global_stat["numActive"])

                #active_info = self.aria2.tell_active(keys)

                if old_num_active > num_active:
                    downloaded += old_num_active - num_active
                    old_num_active = num_active

                downloads_percent = round(float(downloaded / total_downloads), 2)
                if downloads_percent != old_downloads_percent:
                    print(downloaded, total_downloads)
                    self.queue_event('downloads_percent', downloads_percent)
                    old_downloads_percent = downloads_percent

            # This method purges completed/error/removed downloads, in order to free memory
            self.aria2.purge_download_result()

        # Finished, close aria2
        self.aria2.shutdown()
        self.queue_event('downloads_progress_bar', 'hide')


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
