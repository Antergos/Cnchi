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


""" Module to download packages using requests library """

import os
import logging
import queue
import shutil
import requests
import time
import hashlib
import socket
import io
import threading

def get_md5(file_name):
    """ Gets md5 hash from a file """
    md5_hash = hashlib.md5()
    with open(file_name, "rb") as myfile:
        for line in myfile:
            md5_hash.update(line)
    return md5_hash.hexdigest()


class CopyToCache(threading.Thread):
    ''' Class thread to copy a xz file to the user's provided cache directory '''
    def __init__(self, origin, xz_cache_dirs):
        threading.Thread.__init__(self)
        self.origin = origin
        self.xz_cache_dirs = xz_cache_dirs

    def run(self):
        basename = os.path.basename(self.origin)
        for xz_cache_dir in self.xz_cache_dirs:
            dst = os.path.join(xz_cache_dir, basename)
            # Try to copy the file, do not worry if it's not possible
            try:
                shutil.copy(self.origin, dst)
            except (FileNotFoundError, FileExistsError, OSError):
                pass


class Download(object):
    """ Class to download packages using requests
        This class tries to previously download all necessary packages for
        Antergos installation using requests """

    def __init__(self, pacman_cache_dir, xz_cache_dirs, callback_queue):
        """ Initialize Download class. Gets default configuration """
        self.pacman_cache_dir = pacman_cache_dir
        self.xz_cache_dirs = xz_cache_dirs
        self.callback_queue = callback_queue

        # Check that pacman cache directory exists
        os.makedirs(self.pacman_cache_dir, mode=0o755, exist_ok=True)

        # Determine path to alpm database files and ensure it exists
        self.dbfiles_path = os.path.normpath(
                os.path.join(self.pacman_cache_dir, '../../../lib/pacman/local')
        )
        os.makedirs(self.dbfiles_path, mode=0o755, exist_ok=True)

        # Stores last issued event (to prevent repeating events)
        self.last_event = {}

    def start(self, downloads):
        """ Downloads using requests """
        downloaded = 0
        total_downloads = len(downloads)
        download_error = False
        needs_to_download = None

        self.queue_event('downloads_progress_bar', 'show')
        self.queue_event('downloads_percent', '0')

        copy_to_cache_threads = []

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

            dst_path = os.path.join(self.pacman_cache_dir, element['filename'])

            if os.path.exists(dst_path):
                # File already exists in destination pacman's cache (previous install?)
                # We check the file md5 hash
                md5 = get_md5(dst_path)
                md5hash = element.get('hash', False)
                if md5hash and md5hash != md5:
                    logging.debug("MD5 hash of file %s does not match what's in the repo"
                                  "database! Cnchi will download it", element['filename'])
                    # Wrong hash. Force to download it
                    needs_to_download = True
                elif md5hash == md5 or not md5hash:
                    # Hash ok or can't be checked (is False or an empty string). Do not
                    # download the pkg but store the pkg name in case it causes problems later.
                    self.queue_event('cache_pkgs_md5_check_failed', element['identity'])
                    logging.debug(
                            'Checksum unavailable for cached package: %s',
                            element['identity'])
                    logging.debug(
                        "File %s already exists, Cnchi will not overwrite it",
                        element['filename'])
                    needs_to_download = False
                    downloaded += 1
            else:
                needs_to_download = True
                for xz_cache_dir in self.xz_cache_dirs:
                    dst_xz_cache_path = os.path.join(xz_cache_dir, element['filename'])

                    if os.path.exists(dst_xz_cache_path):
                        # We're lucky, the package is already downloaded
                        # in the cache the user has given us

                        # Check the file's md5 hash
                        # element['hash'] is not always available
                        # that is why we use get() with default of False
                        copy_it = False
                        if element.get('hash', False):
                            md5 = get_md5(dst_xz_cache_path)
                            if element['hash'] == md5:
                                # File exists in cache and its md5 is ok
                                # Let's copy it to our destination
                                copy_it = True
                        else:
                            # File exists in cache but we can't check if its md5 is ok or not
                            # Let's copy it to our destination but store the pkg's name in case
                            # it causes problems later on.
                            copy_it = True
                            self.queue_event(
                                    'cache_pkgs_md5_check_failed',
                                    element['identity'])
                            logging.debug(
                                    'Checksum unavailable for cached package: %s',
                                    element['identity'])

                        if copy_it:
                            logging.debug("%s found in suplied xz packages' cache. Copying...", element['filename'])
                            try:
                                shutil.copy(dst_xz_cache_path, dst_path)
                                needs_to_download = False
                                downloaded += 1
                                # Copy alpm database files for the this package if available
                                dbfiles_dirname = element['identity'] + '-' + element['version']
                                dbfiles_srcpath = os.path.join('/var/lib/pacman/local', dbfiles_dirname)
                                if os.path.exists(dbfiles_srcpath):
                                    try:
                                        shutil.copytree(dbfiles_srcpath, self.dbfiles_path)
                                    except shutil.Error as err:
                                        logging.warning(
                                                'failed to copy dbfiles for %s. src was: %s, dst was: %s, err was: %s',
                                                element['name'], dbfiles_srcpath, self.dbfiles_path, err
                                        )
                                # Get out of the for loop, as we managed
                                # to find the package in this cache directory
                                break
                            except OSError as os_error:
                                logging.debug("Error copying %s to %s : %s", dst_xz_cache_path, dst_path, os_error)

            if needs_to_download:
                # Package wasn't previously downloaded or its md5 was wrong
                # We'll have to download it
                # Let's download our file using its url
                for url in element['urls']:
                    # Let's catch empty values as well as None just to be safe
                    if not url:
                        # Something bad has happened
                        download_error = True
                        logging.debug(
                            "Package %s v%s has an empty url for this mirror",
                            element['identity'],
                            element['version'])
                        continue
                    percent = 0
                    completed_length = 0
                    start = time.perf_counter()
                    try:
                        # By default, get waits five minutes before
                        # issuing a timeout, which is too much.
                        r = requests.get(url, stream=True, timeout=30)
                        if r.status_code == requests.codes.ok:
                            # Get total file length
                            try:
                                total_length = int(r.headers.get('content-length'))
                            except TypeError:
                                total_length = 0
                                logging.debug(
                                    "Metalink for package %s has no size info",
                                    element['identity'])

                            with open(dst_path, 'wb') as xz_file:
                                for data in r.iter_content(io.DEFAULT_BUFFER_SIZE):
                                    if not data:
                                        break
                                    xz_file.write(data)
                                    completed_length += len(data)
                                    old_percent = percent
                                    if total_length > 0:
                                        percent = round(float(completed_length / total_length), 2)
                                    else:
                                        percent += 0.1
                                    if old_percent != percent:
                                        self.queue_event('percent', percent)
                                    bps = completed_length // (time.perf_counter() - start)
                                    if bps >= (1024 * 1024):
                                        Mbps = bps / (1024 * 1024)
                                        progress_text = "{0}%   {1:.2f} Mbps".format(int(percent * 100), Mbps)
                                    elif bps >= 1024:
                                        Kbps = bps / 1024
                                        progress_text = "{0}%   {1:.2f} Kbps".format(int(percent * 100), Kbps)
                                    else:
                                        progress_text = "{0}%   {1:.2f} bps".format(int(percent * 100), bps)
                                    self.queue_event('progress_bar_show_text', progress_text)

                            # element['hash'] is not always available
                            # that is why we have to check against None
                            if element['hash'] is not None:
                                md5 = get_md5(dst_path)
                                if element['hash'] != md5:
                                    # Wrong md5! Force to download it again
                                    download_error = True
                                    logging.debug(
                                        "MD5 hash of file %s (%s) do not match! Cnchi will try another mirror.",
                                        element['filename'],
                                        url)
                                    continue

                            # If we've reached here let's assume it's ok
                            download_error = False
                            downloaded += 1

                            # Copy downloaded xz file to the cache the user has provided, too.
                            copy_to_cache_thread = CopyToCache(dst_path, self.xz_cache_dirs)
                            copy_to_cache_threads += [copy_to_cache_thread]
                            copy_to_cache_thread.start()

                            # Get out of the for loop, as we managed
                            # to download the package
                            break
                        else:
                            # requests failed to obtain the file. Wrong url?
                            download_error = True
                            msg = "Can't download {0}, Cnchi will try another mirror.".format(url)
                            logging.debug(msg)
                            continue
                    except (socket.timeout, requests.exceptions.Timeout, requests.exceptions.ConnectionError) as connection_error:
                        download_error = True
                        msg = "Can't download {0} ({1}), Cnchi will try another mirror in a minute.".format(url, connection_error)
                        logging.debug(msg)
                        time.sleep(60) # delays for 60 seconds
                        continue

                if download_error:
                    # None of the mirror urls works.
                    # Stop right here, so the user does not have to wait
                    # to download the other packages.
                    msg = "Can't download {0}, even after trying all available mirrors".format(element['filename'])
                    logging.error(msg)
                    return False

            self.queue_event('progress_bar_show_text', '')

            downloads_percent = round(float(downloaded / total_downloads), 2)
            self.queue_event('downloads_percent', str(downloads_percent))

        # Wait until all xz packages are also copied to provided cache (if any)
        for x in copy_to_cache_threads:
            x.join()

        self.queue_event('downloads_progress_bar', 'hide')
        return True

    def queue_event(self, event_type, event_text=None):
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
