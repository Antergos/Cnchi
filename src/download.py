#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  download.py
#
#  Copyright 2013 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import os
import subprocess
import logging
import xmlrpc.client
import queue

""" Module to download packages using Aria2 """

try:
    import pm2ml
except:
    print("pm2ml not found. Aria2 download won't work.")

class DownloadPackages(object):
    """ Class to download packages using Aria2
        This class tries to previously download all necessary packages for
        Antergos installation using aria2.
        It's known to use too much memory so it's not advised to use it """
    def __init__(self, package_names, conf_file=None, cache_dir=None, callback_queue=None):
        """ Initialize DownloadPackages class. Gets default configuration """
        if conf_file == None:
            self.conf_file = "/etc/pacman.conf"
        else:
            self.conf_file = conf_file

        if cache_dir == None:
            self.cache_dir = "/var/cache/pacman/pkg"
        else:
            self.cache_dir = cache_dir

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        # Stores last issued event (to prevent repeating events)
        self.last_event = {}

        self.aria2_process = None

        self.callback_queue = callback_queue

        self.rpc = {}
        self.rpc["user"] = "antergos"
        self.rpc["passwd"] = "antergos"
        self.rpc["port"] = "6800"
        
        self.aria2_options = []

        self.set_aria2_options(self.cache_dir)

        self.run_aria2_as_daemon()

        self.connection = self.aria2_connect()

        if self.connection == None:
            logging.warning(_("Can't connect with aria2, downloading will be performed by alpm."))
            return

        self.aria2_download(package_names)

    '''
    def aria2_download(self, package_names):
        """ Main method. Downloads all packages in package_names list and its dependencies using aria2 """
        for package_name in package_names:
            metalink = self.create_metalink(package_name)
            if metalink == None:
                logging.error(_("Error creating metalink for package %s"), package_name)
                continue

            gids = self.add_metalink(metalink)

            if len(gids) <= 0:
                logging.error(_("Error adding metalink for package %s"), package_name)
                continue

            all_gids_done = False

            while all_gids_done == False:
                all_gids_done = True
                gids_to_remove = []
                for gid in gids:
                    total = 0
                    completed = 0
                    old_percent = -1

                    try:
                        keys = ["gid", "status", "totalLength", "completedLength", "files"]
                        result = self.connection.aria2.tellStatus(gid, keys)
                        #pprint(result)
                        logging.debug(result)
                    except xmlrpc.client.Fault as e:
                        logging.exception(e)
                        gids_to_remove.append(gid)
                        continue

                    # remove completed gid's
                    if result['status'] == "complete":
                        self.connection.aria2.removeDownloadResult(gid)
                        gids_to_remove.append(gid)
                        continue

                    # if gid is not active, go to the next gid
                    if result['status'] != "active":
                        continue

                    # There's still an active download
                    all_gids_done = False

                    # Get files managed by this gid.
                    files = result['files']
                    #pprint(files)
                    logging.debug(files)

                    total_length = int(result['totalLength'])
                    if total_length == 0:
                        total_length = int(files[0]['length'])
                    total += total_length

                    if total <= 0:
                        continue

                    # Get first uri to get the real package name
                    # (we need to use this if we want to show individual
                    # packages from metapackages like base or base-devel)
                    uri = files[0]['uris'][0]['uri']
                    basename = os.path.basename(uri)
                    ext = ".pkg.tar.xz"
                    if basename.endswith(ext):
                        basename = basename[:-len(ext)]

                    action = _("Downloading package '%s'...") % basename
                    self.queue_event('info', action)

                    while result['status'] == "active":
                        result = self.connection.aria2.tellStatus(gid)
                        completed = int(result['completedLength'])
                        percent = float(completed / total)
                        if percent != old_percent:
                            self.queue_event('local_percent', percent)
                            old_percent = percent

                gids = self.remove_old_gids(gids, gids_to_remove)
                
                # Show some debug info
                result = self.connection.aria2.getGlobalStat()
                #pprint(result)
                logging.debug(result)

            # This method purges completed/error/removed downloads to free memory
            self.connection.aria2.purgeDownloadResult()
    '''
    def aria2_download(self, package_names):
        """ Main method. Downloads all packages in package_names list and its dependencies using aria2 """
        for package_name in package_names:
            metalink = self.create_metalink(package_name)
            if metalink == None:
                logging.error(_("Error creating metalink for package %s"), package_name)
                continue

            gids = self.add_metalink(metalink)

            if len(gids) <= 0:
                logging.error(_("Error adding metalink for package %s"), package_name)
                continue

            global_stat = self.connection.aria2.getGlobalStat()
            num_active = int(global_stat["numActive"])
                        
            while num_active > 0:
                try:
                    keys = ["gid", "status", "totalLength", "completedLength", "files"]
                    result = self.connection.aria2.tellActive(keys)
                    pprint(result)
                    logging.debug(result)
                except xmlrpc.client.Fault as e:
                    logging.exception(e)

                total_length = 0
                completed_length = 0

                for x in range(0, num_active):
                    # Get files managed by this gid.
                    files = result[x]['files']
                    #pprint(files)
                    logging.debug(files)

                    total_length += int(result[x]['totalLength'])
                    #total_length += int(files['totalLength'])
                    path = files['path']

                ext = ".pkg.tar.xz"
                if path.endswith(ext):
                    path = path[:-len(ext)]
                    
                ####

                action = _("Downloading package '%s'...") % basename
                self.queue_event('info', action)

                #while result['status'] == "active":
                if result['status'] == "active":
                    #result = self.connection.aria2.tellStatus(gid)
                    completed = int(result['completedLength'])
                    percent = float(completed / total)
                    if percent != old_percent:
                        self.queue_event('local_percent', percent)
                        old_percent = percent

                gids = self.remove_old_gids(gids, gids_to_remove)
                
                # Show some debug info
                global_stat = self.connection.aria2.getGlobalStat()
                #pprint(global_stat)
                logging.debug(global_stat)
                num_active = int(global_stat["numActive"])

                # This method purges completed/error/removed downloads to free memory
                self.connection.aria2.purgeDownloadResult()
    
    def aria2_connect(self):
        """ Connect to aria2 daemon """
        connection = None

        user = self.rpc["user"]
        password = self.rpc["passwd"]
        port = self.rpc["port"]
        
        aria2_url = 'http://%s:%s@localhost:%s/rpc' % (user, password, port)

        try:
            connection = xmlrpc.client.ServerProxy(aria2_url)
        except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as err:
            logging.debug(_("Can't connect to Aria2. Error Output: %s" % err))

        return connection

    def remove_old_gids(self, gids, gids_to_remove):
        """ Remove old downloads """
        new_gids_list = []
        for gid in gids:
            if gid not in gids_to_remove:
                new_gids_list.append(gid)
        return new_gids_list

    def set_aria2_options(self, cache_dir):
        """ Set aria2 options """

        self.aria2_options = [
            #"--max-concurrent-downloads=1",
            #"--split=5",
            #"--check-integrity",
            #"--continue=false",
            #"--always-resume=false",
            #"--auto-save-interval=0",
            #"--summary-interval=0",
            #"--remove-control-file",
            #"--metalink-file=/tmp/packages.metalink",
            #"--pause"
            "--log=/tmp/cnchi-downloads.log",
            "--min-split-size=5M",
            "--max-connection-per-server=2",
            "--max-tries=2",
            "--timeout=5",
            "--enable-rpc",
            "--rpc-user=%s" % self.rpc["user"],
            "--rpc-passwd=%s" % self.rpc["passwd"],
            "--rpc-listen-port=%s" % self.rpc["port"],
            "--rpc-save-upload-metadata=false",
            "--rpc-max-request-size=16M",
            "--allow-overwrite=false",
            "--auto-file-renaming=false",
            "--log-level=error",
            "--show-console-readout=false",
            "--no-conf",
            "--quiet",
            "--stop-with-process=%d" % os.getpid(),
            "--file-allocation=none",
            "--max-file-not-found=5",
            "--remote-time=true",
            "--conditional-get=true",
            "--dir=%s" % cache_dir]

    def run_aria2_as_daemon(self):
        """ Start aria2 as a daemon """
        aria2_cmd = ['/usr/bin/aria2c'] + self.aria2_options + ['--daemon=true']
        self.aria2_process = subprocess.Popen(aria2_cmd)
        self.aria2_process.wait()

    def create_metalink(self, package_name):
        """ Creates a metalink to download package_name and its dependencies """
        args = str("-c %s" % self.conf_file).split()

        if package_name == "databases":
            args += ["-y"]
        else:
            args += [package_name]

        args += ["--noconfirm"]
        args += "-r -p http -l 50".split()

        try:
            pargs, conf, download_queue, not_found, missing_deps = pm2ml.build_download_queue(args)
        except:
            logging.error(_("Unable to create download queue for package %s"), package_name)
            return None

        if not_found:
            msg = _("Can't find these packages: ")
            for not_found in sorted(not_found):
                msg = msg + not_found + " "
            logging.warning(msg)

        if missing_deps:
            msg = _("Warning! Can't resolve these dependencies: ")
            for missing in sorted(missing_deps):
                msg = msg + missing + " "
            logging.warning(msg)

        metalink = pm2ml.download_queue_to_metalink(
            download_queue,
            output_dir=pargs.output_dir,
            set_preference=pargs.preference
        )
        return metalink

    def add_metalink(self, metalink):
        """ Adds a metalink to the download queue """
        gids = []
        if metalink != None:
            try:
                binary_metalink = xmlrpc.client.Binary(str(metalink).encode())
                gids = self.connection.aria2.addMetalink(binary_metalink)
            except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as err:
                logging.exception("Can't communicate with Aria2. Error Output: %s" % err)

        return gids

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
    import gettext
    _ = gettext.gettext

    logging.basicConfig(filename="/tmp/download.log", level=logging.DEBUG)

    DownloadPackages(["base", "base-devel"])

