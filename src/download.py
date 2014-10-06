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

import os
import subprocess
import logging
import xmlrpc.client
import queue
import logging
import urllib
import xml.etree.ElementTree as etree

_PM2ML = True
try:
    import pm2ml
except ImportError:
    _PM2ML = False

#from pprint import pprint

""" Module to download packages using Aria2 or urllib """
class DownloadPackages(object):
    """ Class to download packages using Aria2 or urllib
        This class tries to previously download all necessary packages for
        Antergos installation using aria2 or urllib
        Aria2 is known to use too much memory (not Aria2's fault but ours)
        so it's not advised to use it """

    def __init__(self, package_names, use_aria2=False, conf_file=None, cache_dir=None, callback_queue=None):
        """ Initialize DownloadPackages class. Gets default configuration """

        if not _PM2ML:
            logging.warning(_("pm2ml not found. Download won't work, will use alpm instead."))
            return

        self.use_aria2 = use_aria2

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

        if use_aria2:
            self.set_aria2_options(self.cache_dir)
            self.run_aria2_as_daemon()
            self.connection = self.aria2_connect()
            if self.connection == None:
                logging.warning(_("Can't connect with aria2, downloading will be performed by alpm."))
                return
            self.aria2_download(package_names)
        else:
            self.download(package_names)

    def get_metalink_info(self, metalink):
        """ Reads metalink xml and stores it in a dict """

        metalink_info = {}
        TAG = "{urn:ietf:params:xml:ns:metalink}"
        root = etree.fromstring(str(metalink))

        for child1 in root.iter(TAG + "file"):
            el = {}

            el['filename'] = child1.attrib['name']

            for child2 in child1.iter(TAG + "identity"):
                el['identity'] = child2.text
            
            for child2 in child1.iter(TAG + "size"):
                el['size'] = child2.text
            
            for child2 in child1.iter(TAG + "version"):
                el['version'] = child2.text
            
            for child2 in child1.iter(TAG + "description"):
                el['description'] = child2.text
            
            for child2 in child1.iter(TAG + "hash"):
                el[child2.attrib['type']] = child2.text 

            el['urls'] = []
            for child2 in child1.iter(TAG + "url"):
                el['urls'].append(child2.text)
    
            metalink_info[el['identity']] = el

        return metalink_info
        
    def download(self, package_names):
        """ Downloads needed packages in package_names list and its dependencies using urllib """
        downloads = {}
        
        for package_name in package_names:
            metalink = self.create_metalink(package_name)
            if metalink == None:
                print("Error creating metalink for package %s" % package_name)
                logging.error(_("Error creating metalink for package %s"), package_name)
                continue

            # Update our downloads dict with the new info from the processed metalink
            downloads.update(self.get_metalink_info(metalink))
            
        for key in downloads:
            el = downloads[key]
            txt = _("Downloading %s %s...") % (el['identity'], el['version'])
            self.queue_event('info', txt)
            filename = os.path.join(self.cache_dir, el['filename'])
            completed_length = 0
            # TODO: Check el['size'] units
            total_length = el['size']
            chunk_size = 8192
            percent = 0
            self.queue_event('percent', percent)
            for url in el['urls']
                url_open = urllib.request.urlopen(url)
                with open(filename, 'b+w') as xzfile:
                    data = url_open.read(chunk_size)
                    while len(data) > 0:
                        xzfile.write(data)
                        completed_length += len(data)
                        percent = round(float(completed_length / total_length), 2)
                        self.queue_event('percent', percent)
                        data = url_open.read(chunk_size)
                # There're some downloads, that are so quick, that percent does not reach 100.
                # We simulate it here
                self.queue_event('percent', 1.0)

    def create_metalink(self, package_name):
        """ Creates a metalink to download package_name and its dependencies """
        args = ["-c"]
        args.append(self.conf_file)

        #args += ["--noconfirm", "--all-deps", "--needed"]
        args += ["--noconfirm", "--all-deps"]

        if package_name is "databases":
            args += ["--refresh"]
        
        if self.use_aria2:
            args += "-r -p http -l 50".split()

        if package_name is not "databases":
            args += [package_name]

        print(args)
        
        try:
            pargs, conf, download_queue, not_found, missing_deps = pm2ml.build_download_queue(args)
        except Exception as e:
            print(e)
            print("Unable to create download queue for package %s" % package_name)
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

    def aria2_download(self, package_names):
        """ Downloads needed packages in package_names list and its dependencies using aria2 """
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
            
            old_percent = -1
            old_path = ""
                        
            action = _("Downloading package '%s' and its dependencies...") % package_name
            self.queue_event('info', action)

            while num_active > 0:
                try:
                    keys = ["gid", "status", "totalLength", "completedLength", "files"]
                    result = self.connection.aria2.tellActive(keys)
                    #pprint(result)
                    #logging.debug(result)
                except xmlrpc.client.Fault as e:
                    logging.exception(e)

                total_length = 0
                completed_length = 0

                for x in range(0, num_active):
                    total_length += int(result[x]['totalLength'])
                    completed_length += int(result[x]['completedLength'])
                
                # As --max-concurrent-downloads=1 we can be sure only one file is downloaded at a time
                path = result[x]['files'][0]['path']
                ext = ".pkg.tar.xz"
                if path.endswith(ext):
                    path = path[:-len(ext)]
                                
                percent = round(float(completed_length / total_length), 2)
                
                if path != old_path and percent == 0:
                    # There're some downloads, that are so quick, that percent does not reach 100. We simulate it here
                    self.queue_event('percent', 1.0)
                    # Update download file name
                    self.queue_event('info', _("Downloading %s...") % path)
                    old_path = path
                
                if percent != old_percent:
                    self.queue_event('percent', percent)
                    old_percent = percent

                # Get global statistics
                global_stat = self.connection.aria2.getGlobalStat()
                #pprint(global_stat)
                #logging.debug(global_stat)
                
                num_active = int(global_stat["numActive"])

            # This method purges completed/error/removed downloads to free memory
            self.connection.aria2.purgeDownloadResult()
            
        self.connection.aria2.shutdown()
    
    def aria2_connect(self):
        """ Connect to aria2 daemon """
        connection = None

        user = self.rpc["user"]
        passwd = self.rpc["passwd"]
        port = self.rpc["port"]
        
        aria2_url = 'http://%s:%s@localhost:%s/rpc' % (user, passwd, port)

        try:
            connection = xmlrpc.client.ServerProxy(aria2_url)
        except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as err:
            logging.debug(_("Can't connect to Aria2. Error Output: %s") % err)

        return connection

    def set_aria2_options(self, cache_dir):
        """ Set aria2 options """
        user = self.rpc["user"]
        passwd = self.rpc["passwd"]
        port = self.rpc["port"]
        pid = os.getpid()

        self.aria2_options = [
            "--allow-overwrite=false",      # If file is already downloaded overwrite it
            "--always-resume=true",         # Always resume download.
            "--auto-file-renaming=false",   # Rename file name if the same file already exists.
            "--auto-save-interval=0",       # Save a control file(*.aria2) every SEC seconds.
            "--dir=%s" % cache_dir,         # The directory to store the downloaded file(s).
            "--enable-rpc",                 # Enable XML-RPC server. It is strongly recommended to set username and
                                            # password using --rpc-user and --rpc-passwd option. See also
                                            # --rpc-listen-port option (default false)
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
            "--rpc-user=%s" % user,
            "--rpc-passwd=%s" % passwd,
            "--rpc-listen-port=%s" % port,
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

    def run_aria2_as_daemon(self):
        """ Start aria2 as a daemon """
        aria2_cmd = ['/usr/bin/aria2c'] + self.aria2_options + ['--daemon=true']
        self.aria2_process = subprocess.Popen(aria2_cmd)
        self.aria2_process.wait()

    def add_metalink(self, metalink):
        """ Adds a metalink to aria2 download queue """
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

''' Test case '''
if __name__ == '__main__':
    import gettext
    _ = gettext.gettext

    logging.basicConfig(filename="/tmp/cnchi-aria2-test.log", level=logging.DEBUG)

    #DownloadPackages(package_names=["gnome-software"], cache_dir="/tmp/aria2", use_aria2=False)
    DownloadPackages(package_names=["gnome-sudoku"], cache_dir="/tmp/aria2", use_aria2=False)
    #DownloadPackages(package_names=["base", "base-devel"], cache_dir="/tmp/aria2", use_aria2=False)
