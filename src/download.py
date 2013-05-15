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

import pm2ml
import sys
import os
import time
import subprocess
import log
import xmlrpc.client

from pprint import pprint

class DownloadPackages():
    def __init__(self, package_names, conf_file=None, cache_dir=None, callback_queue=None):
        if conf_file == None:
            self.conf_file = "/etc/pacman.conf"
        else:
            self.conf_file = conf_file
            
        if cache_dir == None:
            self.cache_dir = "/var/cache/pacman/pkg"
        else:
            self.cache_dir = cache_dir
            
        self.callback_queue = callback_queue

        self.rpc_user = "antergos"
        self.rpc_passwd = "antergos"
        self.rpc_port = "6800"

        self.run_aria2_as_daemon()

        aria2_url = 'http://%s:%s@localhost:%s/rpc' % (self.rpc_user, self.rpc_passwd, self.rpc_port)

        try:
            s = xmlrpc.client.ServerProxy(aria2_url)
        except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as e:
            print(_("Can't connect to Aria2. Won't be able to speed up the download:"))
            print(e)
            return

        # Add all metalinks in pause mode (we start aria2 with --pause)
        all_gids = []
        names = {}
        for package_name in package_names:
            metalink = self.get_metalink(package_name)
            if metalink != None:
                #meta_path = "/tmp/%s.metalink" % package_name
                #with open(meta_path, "wb") as f:
                #    f.write(str(metalink).encode())
                try:
                    log.debug(_("Adding metalink for package %s") % package_name)
                    binary_metalink = xmlrpc.client.Binary(str(metalink).encode())
                    gids = s.aria2.addMetalink(binary_metalink)
                    for gid in gids:
                        all_gids.append(gid)
                        names[gid] = package_name
                except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as e:
                    print("Can't communicate with Aria2. Won't be able to speed up the download:")
                    print(e)
                    return
            else:
                log.debug(_("Error creating metalink for package %s") % package_name)
        
        # pause all (just in case)
        s.aria2.pauseAll()

        # Download gids one by one
        for gid in all_gids:
            total = 0
            completed = 0
            old_percent = -1
            
            # unpause our gid
            try:
                s.aria2.unpause(gid)
            except xmlrpc.client.Fault as e:
                print(package_name, e)
            
            # wait until our gid starts downloading (active status)
            
            r = s.aria2.tellStatus(gid)
            while r['status'] == 'waiting':
                r = s.aria2.tellStatus(gid)
                time.sleep(0.1)
            
            totalLength = int(r['totalLength'])
            # why sometimes gives 0 as totalLength is a mistery to me
            if totalLength == 0:
                files = r['files']
                totalLength = int(files[0]['length'])
            total += totalLength
                
            action = _("Downloading package '%s'...") % package_name
            self.queue_event('action', action)

            while r['status'] == "active" :
                r = s.aria2.tellStatus(gid)
                completed = int(r['completedLength'])
                percent = float(completed / total)
                if percent != old_percent:
                    self.queue_event('percent', percent)
                    old_percent = percent

            log.debug(_("Package %s downloaded.") % package_name)

    def run_aria2_as_daemon(self):
        aria2_args = [
            "--log=/tmp/download-aria2.log",
            "--max-concurrent-downloads=5",
            "--split=5",
            "--min-split-size=5M",
            "--max-connection-per-server=1",
            #"--metalink-file=/tmp/packages.metalink",
            "--check-integrity",
            "--continue=false",
            "--enable-rpc",
            "--rpc-user=%s" % self.rpc_user,
            "--rpc-passwd=%s" % self.rpc_passwd,
            "--rpc-listen-port=%s" % self.rpc_port,
            "--rpc-save-upload-metadata=false",
            "--rpc-max-request-size=4M",
            "--pause",
            "--allow-overwrite=true",
            "--always-resume=false",
            "--auto-save-interval=0",
            "--daemon=true",
            "--log-level=notice",
            "--show-console-readout=false",
            "--summary-interval=0",
            "--no-conf",
            "--quiet",
            "--remove-control-file",
            "--stop-with-process=%d" % os.getpid(),
            "--auto-file-renaming=false",
            "--conditional-get=true",
            "--dir=%s" % self.cache_dir]
        
        aria2_cmd = ['/usr/bin/aria2c', ] + aria2_args
        
        aria2c_p = subprocess.Popen(aria2_cmd)
        aria2c_p.wait()

    def get_metalink(self, package_name):
        args = str("-c %s" % self.conf_file).split() 
        args += [package_name]
        args += ["--noconfirm"]
        args += "-r -p http -l 50".split()
        
        try:
            pargs, conf, download_queue, not_found, missing_deps = pm2ml.build_download_queue(args)
        except:
            log.debug(_("Unable to create download queue for package %s") % package_name)
            return None  

        if not_found:
            log.debug(_("Warning! Can't find these packages:"))
            for nf in sorted(not_found):
                log.debug(nf)
      
        if missing_deps:
            log.debug(_("Warning! Can't resolve these dependencies:"))
            for md in sorted(missing_deps):
                log.debug(md)
      
        metalink = pm2ml.download_queue_to_metalink(
            download_queue,
            output_dir=pargs.output_dir,
            set_preference=pargs.preference
        )
        
        return metalink

    def queue_event(self, event_type, event_text=""):
        if self.callback_queue != None:
            self.callback_queue.put((event_type, event_text))
        elif event_type != "percent":
            log.debug(event_text)

if __name__ == '__main__':
    import gettext
    _ = gettext.gettext
    log._debug = True

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
     "dosfstools", "xorg-server", "xorg-server-utils", "sudo", "pacmanxg4", 
     "pkgfile", "chromium", "flashplugin", "alsa-utils", "whois", "dnsutils", 
     "transmission-cli", "libreoffice-installer", "faenza-hotot-icon", 
     "faenza-icon-theme", "antergos-wallpapers", "unzip", "unrar", 
     "net-tools", "xf86-input-synaptics", "usb_modeswitch", "modemmanager"])

