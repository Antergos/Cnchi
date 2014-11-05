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
import subprocess
import logging
import queue

import urllib
import aria2
import metalink as ml

_PM2ML = True
try:
    import pm2ml
except ImportError:
    _PM2ML = False

def url_open_read(urlp, chunk_size=8192):
    """ Helper function to download and read a fragment of a remote file """

    download_error = True
    data = None

    try:
        data = urlp.read(chunk_size)
        download_error = False
    except urllib.error.HTTPError as err:
        msg = ' HTTPError : %s' % err.reason
        logging.exception(msg)
    except urllib.error.URLError as err:
        msg = ' URLError : %s' % err.reason
        logging.exception(msg)

    return (data, download_error)

def url_open(url):
    """ Helper function to open a remote file """

    msg = _('Error opening %s:') % url

    try:
        urlp = urllib.request.urlopen(url)
    except urllib.error.HTTPError as err:
        urlp = None
        msg += ' HTTPError : %s' % err.reason
        logging.exception(msg)
    except urllib.error.URLError as err:
        urlp = None
        msg += ' URLError : %s' % err.reason
        logging.exception(msg)

    return urlp

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

        if not _PM2ML:
            logging.warning(_("pm2ml not found."))
            return

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

        # Stores last issued event (to prevent repeating events)
        self.last_event = {}

        self.callback_queue = callback_queue

        if use_aria2:
            aria2.DownloadAria2(
                package_names,
                pacman_conf_file,
                pacman_cache_dir,
                cache_dir,
                callback_queue)
        else:
            self.download(package_names)

    def download(self, package_names):
        """ Downloads needed packages in package_names list
            and its dependencies using urllib """
        downloads = {}

        self.queue_event('info', _('Creating list of packages to download...'))
        percent = 0
        processed_packages = 0
        total_packages = len(package_names)

        for package_name in package_names:
            metalink = ml.create(package_name, self.pacman_conf_file)
            if metalink == None:
                msg = _("Error creating metalink for package %s") % package_name
                logging.error(msg)
                continue

            # Update downloads dict with the new info
            # from the processed metalink
            downloads.update(ml.get_info(metalink))

            # Show progress to the user
            processed_packages += 1
            percent = round(float(processed_packages / total_packages), 2)
            self.queue_event('percent', percent)

        downloaded = 1
        total_downloads = len(downloads)
        
        self.queue_event('downloads_percent', 0)
        self.queue_event('downloads_progress_bar', 'show')
        
        for key in downloads:
            element = downloads[key]
            txt = _("Downloading %s %s (%d/%d)...")
            txt = txt % (element['identity'], element['version'], downloaded, total_downloads)
            self.queue_event('info', txt)
            filename = os.path.join(self.pacman_cache_dir, element['filename'])
            completed_length = 0
            total_length = int(element['size'])
            percent = 0
            self.queue_event('percent', percent)
            
            downloads_percent = round(float(downloaded / total_downloads), 2)
            self.queue_event('downloads_percent', downloads_percent)

            if os.path.exists(filename):
                # File exists, do not download
                # Note: In theory this won't ever happen
                # (metalink assures us this)
                # print("File %s already exists" % filename)
                self.queue_event('percent', 1.0)
                downloaded += 1
                continue

            # Check if user has given us a cache of xz packages
            if len(self.cache_dir) > 0 and os.path.exists(self.cache_dir):
                full_path = os.path.join(self.cache_dir, filename)
                if os.path.exists(full_path):
                    # We're lucky, the package is already downloaded
                    # let's copy it to our destination
                    dst = os.path.join(self.pacman_cache_dir, filename)
                    try:
                        shutil.copy(full_path, dst)
                        self.queue_event('percent', 1.0)
                        downloaded += 1
                        continue
                    except FileNotFoundError:
                        pass
                    except FileExistsError:
                        # print("File %s already exists" % filename)
                        pass

            for url in element['urls']:
                download_error = False
                urlp = url_open(url)
                if urlp is None:
                    continue
                #print("Downloading %s..." % filename)
                with open(filename, 'w+b') as xzfile:
                    (data, download_error) = url_open_read(urlp)

                    if download_error:
                        # alpm will retry later
                        continue

                    while len(data) > 0 and download_error == False:
                        xzfile.write(data)
                        completed_length += len(data)
                        old_percent = percent
                        percent = round(float(completed_length / total_length), 2)
                        if old_percent != percent:
                            self.queue_event('percent', percent)
                        (data, download_error) = url_open_read(urlp)

                    if not download_error:
                        # There're some downloads, that are so quick,
                        # that percent does not reach 100.
                        # We simulate it here
                        self.queue_event('percent', 1.0)
                        downloaded += 1
                        break

            if download_error:
                # This is not a total disaster, maybe alpm will be able
                # to download it for us later in pac.py
                logging.warning(_("Can't download %s"), element['filename'])
        
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

''' Test case '''
if __name__ == '__main__':
    import gettext
    _ = gettext.gettext

    logging.basicConfig(
        filename="/tmp/cnchi-download-test.log",
        level=logging.DEBUG)

    DownloadPackages(
        package_names=["kde"],
        cache_dir="",
        pacman_cache_dir="/tmp/pkg")
