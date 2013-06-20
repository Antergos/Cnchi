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
#  
#  Antergos Team:
#   Alex Filgueira (faidoc) <alexfilgueira.antergos.com>
#   Raúl Granados (pollitux) <raulgranados.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>
#   Marc Miralles (arcnexus) <arcnexus.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>

import sys
import os
import time
import subprocess
import logging
import xmlrpc.client
import queue

try:
    import pm2ml
except:
    print("pm2ml not found! This installer won't work.")

_test = False

class DownloadPackages():
    def __init__(self, package_names, conf_file=None, cache_dir=None, databases_dir=None, callback_queue=None):
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
            
        if databases_dir == None:
            self.databases_dir = "/var/lib/pacman/sync"
        else:
            self.databases_dir = databases_dir
            
        if not os.path.exists(self.databases_dir):
            os.makedirs(self.databases_dir)
            
        self.last_event = {}
        
        self.aria2_process = None

        self.callback_queue = callback_queue

        self.set_aria2_defaults(databases_dir)

        self.run_aria2_as_daemon()
        
        self.s = self.aria2_connect()
        
        if self.s == None:
            return

        # first, update pacman databases
        # "databases"
        
        #self.download_databases()
        
        # now, download packages
        
        self.aria2_download(package_names)
        
    def aria2_download(self, package_names):
        for package_name in package_names:
            metalink = self.create_metalink(package_name)
            if metalink == None:
                logging.error(_("Error creating metalink for package %s") % package_name)
                continue
            
            gids = self.add_metalink(metalink)
            
            if len(gids) <= 0:
                logging.error(_("Error adding metalink for package %s") % package_name)
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
                        r = self.s.aria2.tellStatus(gid)
                    except xmlrpc.client.Fault as e:
                        logging.exception(e)
                        gids_to_remove.append(gid)
                        continue
                    
                    # remove completed gid's
                    if r['status'] == "complete":
                        self.s.aria2.removeDownloadResult(gid)
                        gids_to_remove.append(gid)
                        continue

                    # if gid is not active, go to the next gid
                    if r['status'] != "active":
                        continue

                    all_gids_done = False

                    totalLength = int(r['totalLength'])
                    files = r['files']
                    if totalLength == 0:
                        totalLength = int(files[0]['length'])
                    total += totalLength

                    if total <= 0:
                        continue
                        
                    # Get first uri to get the real package name
                    # (we need to use this if we want to show individual
                    # packages from metapackages like base or base-devel)
                    uri = files[0]['uris'][0]['uri']
                    basename = os.path.basename(uri)
                    if basename.endswith(".pkg.tar.xz"):
                        basename = basename[:-11]
                    
                    action = _("Downloading package '%s'...") % basename
                    self.queue_event('action', action)

                    while r['status'] == "active" :
                        r = self.s.aria2.tellStatus(gid)
                        completed = int(r['completedLength'])
                        percent = float(completed / total)
                        if percent != old_percent:
                            self.queue_event('percent', percent)
                            old_percent = percent
                            
                gids = self.remove_old_gids(gids, gids_to_remove)

    def aria2_connect(self):
        s = None
        
        aria2_url = 'http://%s:%s@localhost:%s/rpc' % (self.rpc_user, self.rpc_passwd, self.rpc_port)
        
        try:
            s = xmlrpc.client.ServerProxy(aria2_url)
        except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as e:
            logging.exception(_("Can't connect to Aria2. Won't be able to speed up the download."))
        
        return s

    def remove_old_gids(self, gids, gids_to_remove):
        new_gids_list = []
        for gid in gids:
            if gid not in gids_to_remove:
                new_gids_list.append(gid)
        return new_gids_list

    def set_aria2_defaults(self, dest_dir):
        self.rpc_user = "antergos"
        self.rpc_passwd = "antergos"
        self.rpc_port = "6800"
        
        self.aria2_args = [
            "--log=/tmp/download-aria2.log",
            #"--max-concurrent-downloads=1",
            #"--split=5",
            #"--min-split-size=5M",
            #"--max-connection-per-server=2",
            #"--check-integrity",
            #"--continue=false",
            "--enable-rpc",
            "--rpc-user=%s" % self.rpc_user,
            "--rpc-passwd=%s" % self.rpc_passwd,
            "--rpc-listen-port=%s" % self.rpc_port,
            "--rpc-save-upload-metadata=false",
            "--rpc-max-request-size=4M",
            "--allow-overwrite=true",
            #"--always-resume=false",
            #"--auto-save-interval=0",
            "--log-level=notice",
            "--show-console-readout=false",
            #"--summary-interval=0",
            "--no-conf",
            "--quiet",
            "--remove-control-file",
            "--stop-with-process=%d" % os.getpid(),
            "--auto-file-renaming=false",
            #"--conditional-get=true",
            #"--metalink-file=/tmp/packages.metalink",
            #"--pause",
            "--dir=%s" % dest_dir]

    def run_aria2_as_daemon(self):
        # start aria2 as a daemon
        aria2_cmd = ['/usr/bin/aria2c'] + self.aria2_args + ['--daemon=true']
        self.aria2_process = subprocess.Popen(aria2_cmd)
        self.aria2_process.wait()

    def create_metalink(self, package_name):
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
            logging.error(_("Unable to create download queue for package %s") % package_name)
            return None  

        if not_found:
            msg = _("Can't find these packages: ")
            for nf in sorted(not_found):
                msg = msg + nf + " "
            logging.warning(msg)
      
        if missing_deps:
            msg = _("Warning! Can't resolve these dependencies: ")
            for md in sorted(missing_deps):
                msg = msg + md + " "
            logging.warning(msg)
      
        metalink = pm2ml.download_queue_to_metalink(
            download_queue,
            output_dir=pargs.output_dir,
            set_preference=pargs.preference
        )        
        return metalink

    def add_metalink(self, metalink):
        gids = []
        if metalink != None:
            try:
                binary_metalink = xmlrpc.client.Binary(str(metalink).encode())
                gids = self.s.aria2.addMetalink(binary_metalink)
            except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as e:
                logging.exception("Can't communicate with Aria2. Won't be able to speed up the download")

        return gids

    def queue_event(self, event_type, event_text=""):
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
    _test = True

    logging.basicConfig(filename="/tmp/download.log", level=logging.DEBUG)
    
    '''
    DownloadPackages(\
    ["antergos-keyring", "antergos-mirrorlist",
     "haveged", "crda", "ipw2200-fw", "ipw2100-fw", "zd1211-firmware",
     "wireless_tools", "wpa_actiond", "b43-fwcutter", "ntfs-3g", 
     "dosfstools", "xorg-server", "xorg-server-utils", "sudo", "pacmanxg4", 
     "pkgfile", "chromium", "flashplugin", "alsa-utils", "whois", "dnsutils", 
     "transmission-cli", "libreoffice-installer", "faenza-hotot-icon", 
     "faenza-icon-theme", "antergos-wallpapers", "unzip", "unrar", 
     "net-tools", "xf86-input-synaptics", "usb_modeswitch", "modemmanager"])
    '''
    
    DownloadPackages(\
    ["base", "base-devel", "antergos-keyring", "antergos-mirrorlist",
     "haveged", "crda", "ipw2200-fw", "ipw2100-fw", "zd1211-firmware",
     "wireless_tools", "wpa_actiond", "b43-fwcutter", "ntfs-3g", 
     "dosfstools", "xorg-server", "xorg-server-utils", "sudo",
     "pacmanxg4", "pkgfile", "chromium", "flashplugin", "alsa-utils",
     "whois", "dnsutils", "transmission-cli", "libreoffice-installer",
     "faenza-hotot-icon", "faenza-icon-theme", "antergos-wallpapers",
     "unzip", "unrar", "net-tools", "xf86-input-synaptics",
     "usb_modeswitch", "modemmanager", "ttf-dejavu", "ttf-bitstream-vera",
     "network-manager-applet", "networkmanager-openvpn", "gnome-terminal",
     "file-roller", "evince", "gnome-screenshot", "gnome-bluetooth",
     "gnome-calculator", "xdg-user-dirs-gtk", "gedit", "xfburn",
     "gnome-system-monitor", "empathy", "transmission-gtk", "xnoise",
     "hotot-gtk3", "shotwell", "gnome-themes-standard",
     "hicolor-icon-theme", "gdm", "gnome-keyring", "libgnomeui",
     "gnome-shell", "gnome-control-center", "nautilus",	"zukitwo-themes",
     "gstreamer0.10-bad-plugins", "gstreamer0.10-base-plugins",
     "gstreamer0.10-ffmpeg", "gstreamer0.10-good-plugins",
     "gstreamer0.10-ugly-plugins", "gst-libav"])
