#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  download_requests.py
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

""" Module to download packages using requests library """

import os
import logging
import queue
import shutil
import requests
import time
import hashlib

def get_md5(file_name):
    """ Gets md5 hash from a file """
    md5_hash = hashlib.md5()
    with open(file_name, "rb") as myfile:
        for line in myfile:
            md5_hash.update(line)
    return md5_hash.hexdigest()


class Download(object):
    """ Class to download packages using requests
        This class tries to previously download all necessary packages for
        Antergos installation using requests """

    def __init__(self, pacman_cache_dir, cache_dir, callback_queue):
        """ Initialize Download class. Gets default configuration """
        self.pacman_cache_dir = pacman_cache_dir
        self.cache_dir = cache_dir
        self.callback_queue = callback_queue

        # Stores last issued event (to prevent repeating events)
        self.last_event = {}

    def start(self, downloads):
        """ Downloads using requests """

        downloaded = 0
        total_downloads = len(downloads)

        self.queue_event('downloads_progress_bar', 'show')
        self.queue_event('downloads_percent', '0')

        while len(downloads) > 0:
            identity, element = downloads.popitem()

            self.queue_event('percent', '0')

            txt = _("Downloading {0} {1} ({2}/{3})...").format(
                element['identity'],
                element['version'],
                downloaded + 1,
                total_downloads)
            self.queue_event('info', txt)

            try:
                total_length = int(element['size'])
            except TypeError:
                # No problem, we will get the total length from the requests GET
                pass

            # If the user doesn't give us a cache dir to copy xz files from, self.cache_dir will be None
            if self.cache_dir:
                dst_cache_path = os.path.join(self.cache_dir, element['filename'])
            else:
                dst_cache_path = ""

            dst_path = os.path.join(self.pacman_cache_dir, element['filename'])

            needs_to_download = True

            if os.path.exists(dst_path):
                # File already exists (previous install?)
                # We check the file md5 hash
                md5 = get_md5(dst_path)
                if element['hash'] != md5:
                    logging.warning(
                        _("MD5 hash of %s does not match!"),
                        element['filename'])
                    # Wrong hash. Force to download it
                    logging.warning(_("Cnchi will download it"))
                    needs_to_download = True
                else:
                    # Hash ok. Do not download it
                    logging.warning(
                        _("File %s already exists, Cnchi will not overwrite it"),
                        element['filename'])
                    needs_to_download = False
                    downloaded += 1
            elif os.path.exists(dst_cache_path):
                # We're lucky, the package is already downloaded
                # in the cache the user has given us

                # We check the file md5 hash
                md5 = get_md5(dst_cache_path)
                if element['hash'] != md5:
                    logging.warning(
                        _("MD5 hash of %s does not match!"),
                        element['filename'])
                    logging.warning(_("Cnchi will download it"))
                    # Wrong hash. Force to download it
                    needs_to_download = True
                else:
                    # let's copy it to our destination
                    logging.debug(_('%s found in suplied pkg cache. Copying...'), element['filename'])
                    try:
                        shutil.copy(dst_cache_path, dst_path)
                        needs_to_download = False
                        downloaded += 1
                    except OSError as os_error:
                        logging.warning(
                            _("Error copying %s to %s."),
                            dst_cache_path,
                            dst_path)
                        logging.warning(_("Cnchi will download it"))
                        logging.error(os_error)
                        needs_to_download = True

            if needs_to_download:
                # Let's download our filename using url
                for url in element['urls']:
                    if url is None:
                        # Something bad has happened
                        logging.warning(
                            _("Package %s v%s has an empty url for this mirror"),
                            element['identity'],
                            element['version'])
                        continue
                    # msg = _("Downloading file from url {0}").format(url)
                    # logging.debug(msg)
                    percent = 0
                    completed_length = 0
                    start = time.clock()
                    r = requests.get(url, stream=True)
                    total_length = int(r.headers.get('content-length'))
                    if r.status_code == requests.codes.ok:
                        md5_hash = hashlib.md5()
                        with open(dst_path, 'wb') as xz_file:
                            for data in r.iter_content(1024):
                                if not data:
                                    break
                                xz_file.write(data)
                                md5_hash.update(data)
                                completed_length += len(data)
                                old_percent = percent
                                if total_length > 0:
                                    percent = round(float(completed_length / total_length), 2)
                                else:
                                    percent += 0.1
                                if old_percent != percent:
                                    self.queue_event('percent', percent)

                                bps = (completed_length // (time.clock() - start)) / 1024
                                if bps > 1024:
                                    Mbps = bps / 1024
                                    progress_text = "{0}% {1:.2f} Mbps".format(percent * 100, Mbps)
                                else:
                                    progress_text = "{0}% {1:.2f} bps".format(percent * 100, bps)
                                self.queue_event('progress_bar_show_text', progress_text)

                            md5 = md5_hash.hexdigest()

                            if element['hash'] != md5:
                                logging.warning(
                                    _("MD5 hash of %s does not match!"),
                                    element['filename'])
                                logging.warning(_("Cnchi will try another mirror."))
                                # Force to download it again
                                download_error = True
                            else:
                                download_error = False
                                downloaded += 1
                                # Get out of the for loop, as we managed
                                # to download the package
                                break
                    else:
                        download_error = True
                        logging.warning(_("Can't download {0}").format(url))
                        logging.warning(_("Cnchi will try another mirror."))

                if download_error:
                    # None of the mirror urls works.
                    # Stop right here, so the user does not have to wait
                    # to download the other packages.
                    msg = _("Can't download {0}, even after trying all available mirrors").format(element['filename'])
                    logging.error(msg)
                    return False

            downloads_percent = round(float(downloaded / total_downloads), 2)
            self.queue_event('downloads_percent', str(downloads_percent))

        self.queue_event('progress_bar_show_text', '')
        self.queue_event('downloads_progress_bar', 'hide')
        return True

    def queue_event(self, event_type, event_text=""):
        """ Adds an event to Cnchi event queue """

        if self.callback_queue is None:
            if event_type != "percent":
                logging.debug("{0}: {1}".format(event_type, event_text))
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
