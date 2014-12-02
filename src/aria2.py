#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  aria2.py
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
import urllib.request
import urllib.error

import metalink as ml

import pacman.pac as pac

ARIA2_URL = 'http://localhost:6800/rpc'

class DownloadAria2(object):
    """ Class to download packages using Aria2
        This class tries to previously download all necessary packages for
        Antergos installation using aria2 """

    def __init__(
        self,
        package_names,
        pacman_conf_file=None,
        pacman_cache_dir=None,
        cache_dir=None,
        callback_queue=None):
        """ Initialize DownloadAria2 class. Gets default configuration """

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

        self.aria2_process = None
        self.callback_queue = callback_queue
        self.rpc_uid = None

        if not self.run_as_daemon():
            return

        self.download(package_names)

    def get_global_stat(self):
        """ This method returns global statistics such as
            the overall download and upload speeds. """
        try:
            s = xmlrpc.client.ServerProxy(ARIA2_URL)
            stat = s.aria2.getGlobalStat(self.rpc_uid)
            return stat
        except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as err:
            logging.debug(_("Can't call Aria2. Error Output: %s"), err)
            return None

    def tell_active(self, keys):
        """ This method returns  a  list  of  active  downloads. """
        try:
            s = xmlrpc.client.ServerProxy(ARIA2_URL)
            active = s.aria2.tellActive(self.rpc_uid, keys)
            return active
        except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as err:
            logging.debug(_("Can't call Aria2. Error Output: %s"), err)
            return None

    def add_metalink(self, metalink):
        """ This method adds a Metalink download by uploading a ".metalink" file. """
        gids = []
        if metalink != None:
            try:
                s = xmlrpc.client.ServerProxy(ARIA2_URL)
                binary_metalink = xmlrpc.client.Binary(str(metalink).encode())
                gids = s.aria2.addMetalink(self.rpc_uid, binary_metalink)
            except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError, OverflowError) as err:
                logging.error("Can't add metalink to Aria2. Error Output: %s", err)

        return gids

    def purge_download_result(self):
        """ This method purges completed/error/removed downloads to free memory. """
        try:
            s = xmlrpc.client.ServerProxy(ARIA2_URL)
            s.aria2.purgeDownloadResult(self.rpc_uid)
        except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as err:
            logging.debug(_("Can't call Aria2. Error Output: %s"), err)

    def shutdown(self):
        """ This method shuts down aria2. """
        try:
            s = xmlrpc.client.ServerProxy(ARIA2_URL)
            s.aria2.shutdown(self.rpc_uid)
        except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as err:
            logging.debug(_("Can't call Aria2. Error Output: %s"), err)

    def download(self, package_names):
        """ Downloads needed packages in package_names list and its dependencies using aria2 """
        try:
            pacman = pac.Pac(
                conf_path=self.pacman_conf_file,
                callback_queue=self.callback_queue)

            for package_name in package_names:
                metalink = ml.create(pacman, package_name, self.pacman_conf_file)
                if metalink == None:
                    logging.error(_("Error creating metalink for package %s"), package_name)
                    continue

                gids = self.add_metalink(metalink)

                if len(gids) <= 0:
                    logging.error(_("Error adding metalink for package %s"), package_name)
                    continue

                global_stat = self.get_global_stat()
                num_active = int(global_stat["numActive"])

                old_percent = -1
                old_path = ""

                action = _("Downloading package '%s' and its dependencies...") % package_name
                self.queue_event('info', action)

                while num_active > 0:
                    keys = ["gid", "status", "totalLength", "completedLength", "files"]
                    result = self.tell_active(keys)

                    total_length = 0
                    completed_length = 0

                    for i in range(0, num_active):
                        total_length += int(result[i]['totalLength'])
                        completed_length += int(result[i]['completedLength'])

                    # As --max-concurrent-downloads=1 we can be sure only one file is downloaded at a time

                    # path will store full file name (destination)
                    path = result[0]['files'][0]['path']

                    percent = round(float(completed_length / total_length), 2)

                    if path != old_path and percent == 0:
                        # Update download file name
                        path = os.path.basename(path)
                        # Do not show the package's extension to the user
                        ext = ".pkg.tar.xz"
                        if path.endswith(ext):
                            path = path[:-len(ext)]
                        self.queue_event('info', _("Downloading %s...") % path)
                        old_path = path

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

    def run_as_daemon(self):
        """ Start aria2 as a daemon """

        pid = os.getpid()
        pacman_cache = self.pacman_cache_dir

        import uuid
        uid = uuid.uuid4().hex[:16]

        aria2_options = [
            "--allow-overwrite=false",      # If file is already downloaded overwrite it
            "--always-resume=true",         # Always resume download.
            "--auto-file-renaming=false",   # Rename file name if the same file already exists.
            "--auto-save-interval=0",       # Save a control file(*.aria2) every SEC seconds.
            "--dir=%s" % pacman_cache,      # The directory to store the downloaded file(s).
            "--enable-rpc=true",            # Enable XML-RPC server.
            "--file-allocation=prealloc",   # Specify file allocation method (default 'prealloc')
            "--log=/tmp/cnchi-aria2.log",   # The file name of the log file
            "--log-level=warn",             # Set log level to output to console. LEVEL is either debug, info, notice,
                                            # warn or error (default notice)
            "--min-split-size=20M",         # Do not split less than 2*SIZE byte range (default 20M)
            "--max-concurrent-downloads=1", # Set maximum number of parallel downloads for each metalink (default 5)
            "--max-connection-per-server=1",# The maximum number of connections to one server for each download
            "--max-tries=5",                # Set number of tries (default 5)
            "--no-conf=true",               # Disable loading aria2.conf file.
            "--quiet=true",                 # Make aria2 quiet (no console output).
            "--remote-time=false",          # Retrieve timestamp of the remote file from the remote HTTP/FTP server
                                            # and if it is available, apply it to the local file.
            "--remove-control-file=true",   # Remove control file before download.
            "--retry-wait=0",               # Set the seconds to wait between retries (default 0)
            "--rpc-secret=%s" % uid,        # Set RPC secret authorization token
            "--rpc-secure=false",           # RPC transport will be encrypted by SSL/TLS
            "--rpc-listen-port=6800",
            "--rpc-save-upload-metadata=false", # Save the uploaded torrent or metalink metadata in the directory
                                                # specified by --dir option.
            "--rpc-max-request-size=16M",   # Set max size of XML-RPC request. If aria2 detects the request is more
                                            # than SIZE bytes, it drops connection (default 2M)
            "--show-console-readout=false", # Show console readout (default true)
            "--split=5",                    # Download a file using N connections (default 5)
            "--stop-with-process=%d" % pid, # Stop aria2 if Cnchi ends unexpectedly
            "--summary-interval=0",         # Set interval in seconds to output download progress summary. Setting 0
                                            # suppresses the output (default 60)
            "--timeout=60"]                 # Set timeout in seconds (default 60)

        self.rpc_uid = "token:" + uid

        try:
            aria2_cmd = ['/usr/bin/aria2c'] + aria2_options + ['--daemon=true']
            self.aria2_process = subprocess.Popen(aria2_cmd)
            self.aria2_process.wait()
        except FileNotFoundError as err:
            # aria2 is not installed ¿?
            logging.warning(_("Can't run aria2: %s"), err)
            return False
        return True

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

    DownloadAria2(package_names=["gnome-sudoku"], cache_dir="", pacman_cache_dir="/tmp/aria2")
    #DownloadAria2(package_names=["gnome"], cache_dir="", pacman_cache_dir="/tmp/aria2")

    #DownloadAria2(package_names=["gnome-software"], pacman_cache_dir="/tmp/aria2")
    #DownloadAria2(package_names=["base", "base-devel"], pacman_cache_dir="/tmp/aria2")
