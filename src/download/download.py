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
import shutil
import urllib

import metalink as ml
import download_aria2
import download_urllib
import pacman.pac as pac

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

        downloads = self.get_downloads_list(package_names)

        if use_aria2:
            logging.debug(_("Using aria2 to download packages"))
            download = download_aria2.Download(
                pacman_cache_dir,
                callback_queue)
        else:
            logging.debug(_("Using urlib to download packages"))
            download = download_urllib.Download(
                pacman_cache_dir,
                callback_queue)
        
        download.start()

    def get_downloads_list(self, package_names):
        self.queue_event('percent', 0)
        self.queue_event('info', _('Creating list of packages to download...'))
        percent = 0
        processed_packages = 0
        total_packages = len(package_names)

        downloads = []

        try:
            pacman = pac.Pac(
                conf_path=self.pacman_conf_file,
                callback_queue=self.callback_queue)

            for package_name in package_names:
                metalink = ml.create(pacman, package_name, self.pacman_conf_file)
                if metalink == None:
                    logging.error(_("Error creating metalink for package %s"), package_name)
                    continue

                # Update downloads list with the new info
                # from the processed metalink
                downloads.append(ml.get_info(metalink))

                # Show progress to the user
                processed_packages += 1
                percent = round(float(processed_packages / total_packages), 2)
                self.queue_event('percent', percent)

            pacman.release()
            del pacman
        except Exception as err:
            logging.error("Can't initialize pyalpm: %s" % err)

        return downloads        

    def download(self, package_names):
        """ Downloads needed packages in package_names list
            and its dependencies using urllib """

        self.queue_event('percent', 0)
        self.queue_event('info', _('Creating list of packages to download...'))
        percent = 0
        processed_packages = 0
        total_packages = len(package_names)

        downloads = []

        try:
            pacman = pac.Pac(
                conf_path=self.pacman_conf_file,
                callback_queue=self.callback_queue)

            for package_name in package_names:
                metalink = ml.create(pacman, package_name, self.pacman_conf_file)
                if metalink == None:
                    msg = _("Error creating metalink for package %s") % package_name
                    logging.error(msg)
                    continue

                # Update downloads list with the new info
                # from the processed metalink
                downloads.append(ml.get_info(metalink))

                # Show progress to the user
                processed_packages += 1
                percent = round(float(processed_packages / total_packages), 2)
                self.queue_event('percent', percent)

            pacman.release()
            del pacman
        except Exception as err:
            logging.error("Can't initialize pyalpm: %s" % err)

        downloaded = 0
        total_downloads = len(downloads)

        self.queue_event('downloads_progress_bar', 'show')
        self.queue_event('downloads_percent', 0)

        for i in range(0, total_downloads - 1):
            element = downloads.pop()

            self.queue_event('percent', 0)

            txt = _("Downloading %s %s (%d/%d)...")
            txt = txt % (element['identity'], element['version'], downloaded, total_downloads)
            self.queue_event('info', txt)

            try:
                total_length = int(element['size'])
            except TypeError as err:
                logging.warning(_("Metalink for package %s has no size info"), element['identity'])
                total_length = 0

            dst_cache_path = os.path.join(self.cache_dir, element['filename'])
            dst_path = os.path.join(self.pacman_cache_dir, element['filename'])

            if os.path.exists(dst_path):
                # File already exists (previous install?) do not download
                logging.warning(_("File %s already exists, Cnchi will not overwrite it"), element['filename'])
                self.queue_event('percent', 1.0)
                downloaded += 1
            elif os.path.exists(dst_cache_path):
                # We're lucky, the package is already downloaded in the cache the user has given us
                # let's copy it to our destination
                try:
                    shutil.copy(dst_cache_path, dst_path)
                    self.queue_event('percent', 1.0)
                    downloaded += 1
                    continue
                except FileNotFoundError:
                    pass
                except FileExistsError:
                    # print("File %s already exists" % element['filename'])
                    pass
            else:
                # Let's download our filename using url
                for url in element['urls']:
                    msg = _("Downloading file from url %s") % url
                    logging.debug(msg)
                    download_error = False
                    percent = 0
                    completed_length = 0
                    urlp = url_open(url)
                    if urlp != None:
                        with open(dst_path, 'wb') as xzfile:
                            (data, download_error) = url_open_read(urlp)

                            while len(data) > 0 and download_error == False:
                                xzfile.write(data)
                                completed_length += len(data)
                                old_percent = percent
                                if total_length > 0:
                                    percent = round(float(completed_length / total_length), 2)
                                else:
                                    percent += 0.1
                                if old_percent != percent:
                                    self.queue_event('percent', percent)
                                (data, download_error) = url_open_read(urlp)

                            if not download_error:
                                downloaded += 1
                                break
                            else:
                                # try next mirror url
                                completed_length = 0
                                msg = _("Can't download %s, will try another mirror if available") % url
                                logging.warning(msg)
                    else:
                        # try next mirror url
                        msg = _("Can't open %s, will try another mirror if avaliable") % url
                        logging.warning(msg)

                if download_error:
                    # None of the mirror urls works.
                    # This is not a total disaster, maybe alpm will be able
                    # to download it for us later in pac.py
                    msg = _("Can't download %s, even after trying all available mirrors") % element['filename']
                    logging.warning(msg)

            downloads_percent = round(float(downloaded / total_downloads), 2)
            self.queue_event('downloads_percent', downloads_percent)

        self.queue_event('downloads_progress_bar', 'hide')

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
        cache_dir="",
        pacman_cache_dir="/tmp/pkg")
    '''
    DownloadPackages(
        package_names=["kde"],
        cache_dir="",
        pacman_cache_dir="/tmp/pkg")
    '''
