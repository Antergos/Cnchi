#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rank_mirrors.py
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

""" Creates mirrorlist sorted by both latest updates and fastest connection """

import threading
import subprocess
import logging
import time
import os
import shutil
import canonical.misc as misc

class AutoRankmirrorsThread(threading.Thread):
    """ Thread class that downloads and sorts the mirrorlist """
    def __init__(self):
        """ Initialize thread class """
        super(AutoRankmirrorsThread, self).__init__()
        self.rankmirrors_pid = None
        self.script = "/usr/share/cnchi/scripts/update-mirrors.sh"
        self.antergos_mirrorlist = "/etc/pacman.d/antergos-mirrorlist"

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
        
        with open(self.antergos_mirrorlist) as mirrors:
            lines = [x.strip() for x in mirrors.readlines()]
        
        autoselect = "http://mirrors.antergos.com/$repo/$arch"
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
            logging.error(err)
        logging.debug(_("Auto mirror selection has been run successfully"))

