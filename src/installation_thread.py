#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_thread.py
#  
#  Copyright 2013 Cinnarch
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
#  Cinnarch Team:
#   Alex Filgueira (faidoc) <alexfilgueira.cinnarch.com>
#   Raúl Granados (pollitux) <raulgranados.cinnarch.com>
#   Gustau Castells (karasu) <karasu.cinnarch.com>
#   Kirill Omelchenko (omelcheck) <omelchek.cinnarch.com>
#   Marc Miralles (arcnexus) <arcnexus.cinnarch.com>
#   Alex Skinner (skinner) <skinner.cinnarch.com>

import threading
import subprocess

from config import installer_settings

_automatic_script = 'auto_partition.sh'
_easy_script = ''
_manual_script = ''

class InstallationThread(threading.Thread):
    def __init__(self, method):
        threading.Thread.__init__(self)

        self.method = method
        self.script_path = script_path

        self.running = True
        self.error = False
        
        self.script_path = os.path.join(installer_settings["CNCHI_DIR"], "scripts", _autopartition_script)

    def set_devices(auto_device, root_device=None, swap_device=None, mount_devices=None):
        self.auto_device = auto_device
        self.root_device = root_device
        self.swap_device = swap_device
        self.mount_devices = mount_devices
        
    def run(self):
        try:
            #if os.path.exists(self.script_path):
            #       subprocess.Popen(["/bin/bash", self.script_path, self.auto_device])
            # copy some files just for testing
            subprocess.check_call(["/usr/bin/cp", "-Rv", "/usr/share/icons", "/tmp"])
        except subprocess.FileNotFoundError as e:
            self.error = True
            print (_("Can't execute the installation script"))
        except subprocess.CalledProcessError as e:
            self.error = True
            print (_("subprocess CalledProcessError.output = %s") % e.output)

        self.running = False

    def is_running(self):
        return self.running

    def is_ok(self):
        return not self.error
