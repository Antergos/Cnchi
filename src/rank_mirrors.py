#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rank_mirrors.py
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

""" Creates mirrorlist sorted by both latest updates and fastest connection """

import threading
import subprocess
import logging
import time
import os
import shutil
import canonical.misc as misc
import requests

class AutoRankmirrorsThread(threading.Thread):
    """ Thread class that downloads and sorts the mirrorlist """
    def __init__(self):
        """ Initialize thread class """
        super(AutoRankmirrorsThread, self).__init__()
        self.rankmirrors_pid = None
        self.script = "/usr/share/cnchi/scripts/update-mirrors.sh"
        self.antergos_mirrorlist = "/etc/pacman.d/antergos-mirrorlist"
        self.arch_mirrorlist = "/etc/pacman.d/mirrorlist"
        self.arch_mirror_status = "http://www.archlinux.org/mirrors/status/json/"

    def check_status(self, mirrors=None, url=None):
        if mirrors is None or url is None:
            return False

        for mirror in mirrors:
            if url == mirror['url'] and mirror['completion_pct'] == 1:
                return True

        return False

    def run(self):
        """ Run thread """

        # Wait until there is an Internet connection available
        while not misc.has_connection():
            if self.settings.get('stop_all_threads'):
                return
            time.sleep(1)  # Delay

        if not os.path.exists(self.script):
            logging.warning(_("Can't find update mirrors script"))
            return

        # Uncomment antergos mirrors and comment out auto selection so rankmirrors can find the best mirror.
        
        autoselect = "http://mirrors.antergos.com/$repo/$arch"

        if os.path.exists(self.antergos_mirrorlist):
            with open(self.antergos_mirrorlist) as mirrors:
                lines = [x.strip() for x in mirrors.readlines()]
        
            for i in range(len(lines)):
                if lines[i].startswith("Server") and autoselect in lines[i]:
                    lines[i] = "#" + lines[i]
                elif lines[i].startswith("#Server") and autoselect not in lines[i]:
                    lines[i] = lines[i].lstrip("#")
                    
            with misc.raised_privileges():
                # Backup original file
                shutil.copy(self.antergos_mirrorlist, self.antergos_mirrorlist + ".cnchi")
                # Write new one
                with open(self.antergos_mirrorlist, 'w') as mirrors:
                    mirrors.write("\n".join(lines) + "\n")

        # Run rankmirrors command
        try:
            with misc.raised_privileges():
                self.rankmirrors_pid = subprocess.Popen([self.script]).pid

        except subprocess.CalledProcessError as err:
            logging.error(_("Couldn't execute auto mirror selection"))

        # Check arch mirrorlist against mirror status data, remove any bad mirrors.
        if os.path.exists(self.arch_mirrorlist):
            # Use session to avoid silly warning
            # See https://github.com/kennethreitz/requests/issues/1882
            with requests.Session() as session:
                status = session.get(self.arch_mirror_status).json()
                mirrors = status['urls']
            
            with open(self.arch_mirrorlist) as arch_mirrors:
                lines = [x.strip() for x in arch_mirrors.readlines()]

            for i in range(len(lines)):
                if lines[i].startswith("Server"):
                    url = lines[i].split('=')[1]
                    check = self.check_status(mirrors, url)
                    if not check:
                        lines[i] = "#" + lines[i]

            with misc.raised_privileges():
                # Backup original file
                shutil.copy(self.arch_mirrorlist, self.arch_mirrorlist + ".cnchi")
                # Write new one
                with open(self.arch_mirrorlist, 'w') as arch_mirrors:
                    arch_mirrors.write("\n".join(lines) + "\n")

        logging.debug(_("Auto mirror selection has been run successfully"))
