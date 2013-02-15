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
import os
import sys

from config import installer_settings

# Insert the src/pacman directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
pacman_dir = os.path.join(base_dir, 'pacman')
sys.path.insert(0, pacman_dir)

import misc

import pac

_autopartition_script = 'auto_partition.sh'

class InstallationThread(threading.Thread):
    def __init__(self, method, mount_devices):
        threading.Thread.__init__(self)

        self.method = method
        self.mount_devices = mount_devices
        
        print(mount_devices)

        self.running = True
        self.error = False
        
        self.auto_partition_script_path = \
            os.path.join(installer_settings["CNCHI_DIR"], "scripts", _autopartition_script)
    
    @misc.raise_privileges    
    def run(self):
        ## Create and format partitions if we're in automatic mode
        if installer_settings['partition_mode'] == 'automatic':
            try:
                if os.path.exists(self.auto_partition_script_path):
                       self.root = self.mount_devices["automatic"]
                       print("Root device: %s" % self.root)
                       subprocess.Popen(["/bin/bash", self.auto_partition_script_path, self.root])
            except subprocess.FileNotFoundError as e:
                self.error = True
                print (_("Can't execute the auto partition script"))
            except subprocess.CalledProcessError as e:
                self.error = True
                print (_("subprocess CalledProcessError.output = %s") % e.output)

        ## Do real installation here
        
        # Extracted from /arch/setup script
        
        self.dest_dir = "/install"
        kernel_pkg = "linux"
        vmlinuz = "vmlinuz-%s" % kernel_pkg
        initramfs = "initramfs-%s" % kernel_pkg       
        pacman = "powerpill --root %s --config /tmp/pacman.conf --noconfirm --noprogressbar" % self.dest_dir

        self.arch = os.uname()[-1]
    
        self.create_pacman_conf()
        self.prepare_pacman()
        
        # TODO: everything else!

        self.running = False
    
    # creates temporary pacman.conf file
    def create_pacman_conf(self):

        print("Creating pacman.conf for %s architecture" % self.arch)
        
        # Common repos
               
        tmp_file = open("/tmp/pacman.conf", "wt")

        tmp_file.write("[options]\n")
        tmp_file.write("Architecture = auto\n")
        tmp_file.write("SigLevel = PackageOptional\n")
        tmp_file.write("CacheDir = %s/var/cache/pacman/pkg\n" % self.dest_dir)
        tmp_file.write("CacheDir = /packages/core-%s/pkg\n" % self.arch)
        tmp_file.write("CacheDir = /packages/core-any/pkg\n\n")

        tmp_file.write("#### Cinnarch repos start here\n")
        tmp_file.write("[cinnarch-core]\n")
        tmp_file.write("SigLevel = PackageRequired\n")
        tmp_file.write("Include = /etc/pacman.d/cinnarch-mirrorlist\n\n")

        tmp_file.write("[cinnarch-repo]\n")
        tmp_file.write("SigLevel = PackageRequired\n")
        tmp_file.write("Include = /etc/pacman.d/cinnarch-mirrorlist\n")
        tmp_file.write("#### Cinnarch repos end here\n\n")

        tmp_file.write("[core]\n")
        tmp_file.write("SigLevel = PackageRequired\n")
        tmp_file.write("Include = /etc/pacman.d/mirrorlist\n\n")

        tmp_file.write("[extra]\n")
        tmp_file.write("SigLevel = PackageRequired\n")
        tmp_file.write("Include = /etc/pacman.d/mirrorlist\n\n")

        tmp_file.write("[community]\n")
        tmp_file.write("SigLevel = PackageRequired\n")
        tmp_file.write("Include = /etc/pacman.d/mirrorlist\n\n")

        # x86_64 repos only
        if self.arch == 'x86_64':   
            tmp_file.write("[multilib]\n")
            tmp_file.write("SigLevel = PackageRequired\n")
            tmp_file.write("Include = /etc/pacman.d/mirrorlist\n")
    
        tmp_file.close()
        
        ## Init pyalpm

        self.pac = pac.Pac("/tmp/pacman.conf")
        
        # set callback functions
        '''
        self.cb['dl'] = None
        self.cb['totaldl'] = None
        self.cb['dl'] = None
        self.cb['event'] = None
        self.cb['conv'] = None
        self.cb['progress'] = None
        self.cb['log'] = None
        '''

        self.pac.set_callback('dl', self.pacman_cb_dl)
        
    # Pacman callback functions
    def pacman_cb_dl(_target, _transferred, total):
        pass
            
    
    # add gnupg pacman files to installed system
    # needs testing, but it seems to be the way to do it now
    # must be also changed in the CLI Installer
    def prepare_pacman_keychain(self):
        import shutil
        shutil.copy2('/etc/pacman.d/gnupg', '%s/etc/pacman.d' % self.dest_dir)
    
    # Configures pacman and syncs db on destination system
    def prepare_pacman(self):
        dirs = [ "/var/cache/pacman/pkg", "/var/lib/pacman" ]
        
        for d in dirs:
            mydir = os.path.join(self.dest_dir, d)
            if not os.path.exists(mydir):
                os.makedirs(mydir)

        self.prepare_pacman_keychain()
        
        self.pac.do_refresh()
    
    
    def chroot_mount(self):
        dirs = [ "/sys", "/proc", "/dev" ]
        for d in dirs:
            mydir = os.path.join(self.dest_dir, d)
            if not os.path.exists(mydir):
                os.makedirs(mydir)

        mydir = os.path.join(self.dest_dir, "/sys")
        subprocess.Popen(["mount", "-t", "sysfs", "sysfs", mydir])
        subprocess.Popen(["chmod", "555", mydir])

        mydir = os.path.join(self.dest_dir, "/proc")
        subprocess.Popen(["mount", "-t", "proc", "proc", mydir])
        subprocess.Popen(["chmod", "555", mydir])

        mydir = os.path.join(self.dest_dir, "/dev")
        subprocess.Popen(["mount", "-o", "bind", "/dev", mydir])

        

    def is_running(self):
        return self.running

    def is_ok(self):
        return not self.error
        
