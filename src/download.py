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

def download_packages(package_names, conf_file=None, cache_dir=None, callback_queue=None):
    if conf_file == None:
        conf_file = "/etc/pacman.conf"
        
    if cache_dir == None:
        cache_dir = "/var/cache/pacman/pkg"
    
    args = str("-c %s" % conf_file).split() 
    args += package_names
    args += ["--noconfirm"]
    args += "-r -p http -l 50".split()
    
    try:
        pargs, conf, download_queue, not_found, missing_deps = pm2ml.build_download_queue(args)
    except:
        log.debug(_("Unable to create download queue.\nDownload process won't be accelerated with aria2."))
        return
    
    metalink = pm2ml.download_queue_to_metalink(
        download_queue,
        output_dir=pargs.output_dir,
        set_preference=pargs.preference
    )

    log.debug(metalink)
        
    if not_found:
        log.debug("Packages not found:")
        for nf in sorted(not_found):
            log.debug(nf)
  
    if missing_deps:
        log.debug("Unresolved dependencies:")
        for md in sorted(missing_deps):
            log.debug(md)
    
    rpc_user = "antergos"
    rpc_passwd = "antergos"
    rpc_port = "6800"
    
    aria2_args = [
        "--log=/tmp/download-aria2.log",
        "--max-concurrent-downloads=50",
        #"--metalink-file=/tmp/packages.metalink",
        "--check-integrity",
        "--continue=false",
        "--max-connection-per-server=5",
        "--min-split-size=5M",
        "--enable-rpc",
        "--rpc-listen-port=%s" % rpc_port,
        "--rpc-user=%s" % rpc_user,
        "--rpc-passwd=%s" % rpc_passwd,
        "--rpc-save-upload-metadata=false",
        "--allow-overwrite=true",
        "--always-resume=false",
        "--auto-save-interval=0",
        "--daemon=false",
        "--log-level=notice",
        "--show-console-readout=false",
        "--summary-interval=0",
        "--no-conf",
        "--quiet",
        "--remove-control-file",
        "--stop-with-process=%d" % os.getpid(),
        "--auto-file-renaming=false",
        "--conditional-get=true",
        "--dir=%s" % cache_dir]
    
    aria2_cmd = ['/usr/bin/aria2c', ] + aria2_args
    
    log.debug(aria2_cmd)

    aria2c_p = subprocess.Popen(aria2_cmd)
    
    time.sleep(1)
    
    aria2_url = 'http://%s:%s@localhost:%s/rpc' % (rpc_user, rpc_passwd, rpc_port)

    try:
        s = xmlrpc.client.ServerProxy(aria2_url)
        gids = s.aria2.addMetalink(xmlrpc.client.Binary(str(metalink).encode()))
    except (xmlrpc.client.Fault, ConnectionRefusedError, BrokenPipeError) as e:
        print("Can't communicate with Aria2. Won't be able to speed up the download")
        return

    total = 1
    completed = 0
    
    while completed < total:
        total = 0
        completed = 0
        
        for gid in gids:
            r = s.aria2.tellStatus(gid, ['gid', 'totalLength', 'completedLength'])
            total += int(r['totalLength'])
            completed += int(r['completedLength'])

        action = _('Downloading packages with Aria2...')
        percent = int(completed * 100.0 / total)
        
        if callback_queue != None:
            callback_queue.put(('action', action))
            callback_queue.put(('percent', percent))
        
        time.sleep(0.1)


if __name__ == '__main__':
    import gettext
    _ = gettext.gettext
    download_packages(["vim", "gedit", "zip"])
