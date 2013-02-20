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
import shutil

from config import installer_settings

# Insert the src/pacman directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
pacman_dir = os.path.join(base_dir, 'pacman')
sys.path.insert(0, pacman_dir)

import misc

import pac

_autopartition_script = 'auto_partition.sh'

class InstallationThread(threading.Thread):
    def __init__(self, callback_queue, mount_devices, format_devices=None):
        threading.Thread.__init__(self)
        
        self.callback_queue = callback_queue

        self.method = installer_settings['partition_mode']
        
        print("Installing using '%s' method" % self.method)
        
        self.mount_devices = mount_devices
        print(mount_devices)

        self.format_devices = format_devices

        self.running = True
        self.error = False
        
        self.auto_partition_script_path = os.path.join(\
            installer_settings["CNCHI_DIR"], \
            "scripts", _autopartition_script)
    
    @misc.raise_privileges    
    def run(self):
        ## Create/Format partitions
        if self.method == 'automatic':
            try:
                if os.path.exists(self.auto_partition_script_path):
                       self.root = self.mount_devices["automatic"]
                       print("Root device: %s" % self.root)
                       subprocess.Popen(["/bin/bash", \
                                         self.auto_partition_script_path, \
                                         self.root])
            except subprocess.FileNotFoundError as e:
                self.error = True
                print (_("Can't execute the auto partition script"))
            except subprocess.CalledProcessError as e:
                self.error = True
                print (_("CalledProcessError.output = %s") % e.output)
        elif self.method == 'easy' or self.method == 'advanced':
            # TODO: format partitions using mkfs (format_devices)
            pass

        if self.error:
            self.running = False
            return
            
        ## Do real installation here
        
        # Extracted from /arch/setup script

        self.packages = []
        
        self.dest_dir = "/install"
        kernel_pkg = "linux"
        vmlinuz = "vmlinuz-%s" % kernel_pkg
        initramfs = "initramfs-%s" % kernel_pkg       
        pacman = "powerpill --root %s --config /tmp/pacman.conf --noconfirm --noprogressbar" % self.dest_dir

        self.arch = os.uname()[-1]
    
        self.select_packages()
        self.install_packages()

        # installation finished (0 means no error)
        self.callback_queue.put(("finished", 0))

        self.running = False

    def select_packages(self):
        self.create_pacman_conf()
        self.prepare_pacman()
        
        # TODO: use packages.xml instead of this hardcoded list

        with open('/proc/cmdline') as fp:
            for line in fp:
                if "uvesafb" in line:
                    self.packages.append("v86d")
        
        # Always install base and base-devel
        self.packages.append("base")
        self.packages.append("base-devel")
               
        self.packages.append("libgnomeui")
        
        # TODO: Do not use cinnarch-meta!!!
        self.packages.append("cinnarch-meta")

        if installer_settings["use_ntp"]:
            self.packages.append("ntp")

        graphics = self.get_graphic_card()
        
        self.card = ""

        if "ati" in graphics:
            self.packages.append("xf86-video-ati")
            self.packages.append("ati-dri")
            self.card = "ati"
        
        if "nvidia" in graphics:
            self.packages.append("xf86-video-nouveau")
            self.packages.append("nouveau-dri")
            self.card = "nvidia"
        
        if "intel" in graphics or "lenovo" in graphics:
            self.packages.append("xf86-video-intel")
            self.packages.append("intel-dri")
        
        if "virtualbox" in graphics:
            self.packages.append("virtualbox-guest-utils")
            self.packages.append("virtualbox-guest-modules")
        
        if "vmware" in graphics:
            self.packages.append("xf86-video-vmware")
        
        if "via" in graphics:
            self.packages.append("xf86-video-openchrome")
        
        wlan = subprocess.check_output(["hwinfo", "--wlan", "--short"]).decode()

        if "broadcom" in wlan:
            self.packages.append("broadcom-wl")
            
        if os.path.exists("/var/state/dhcp/dhclient.leases"):
            self.packages.append("dhclient")
        
        # Add filesystem packages
        
        fs_types = subprocess.check_output(["blkid", "-c", "/dev/null",\
                                            "-o", "value", "-s", "TYPE"]).decode()

        if "ntfs" in fs_types:
            self.packages.append("ntfs-3g")
        
        if "btrfs" in fs_types:
            self.packages.append("btrfs-progs")

        if "nilfs2" in fs_types:
            self.packages.append("nilfs-utils")

        if "ext" in fs_types:
            self.packages.append("e2fsprogs")

        if "reiserfs" in fs_types:
            self.packages.append("reiserfsprogs")

        if "xfs" in fs_types:
            self.packages.append("xfsprogs")

        if "jfs" in fs_types:
            self.packages.append("jfsutils")

        if "vfat" in fs_types:
            self.packages.append("dosfstools")

        # if raid:
            #self.packages.append("dmraid")

        # Install chinese fonts
        # TODO: check this out, not sure about this vars
        if installer_settings["locale"] == "zh_TW" or \
           installer_settings["locale"] == "zh_CN" or \
           installer_settings["language_name"] == "chinese":
            self.packages.append("opendesktop-fonts")

    def get_graphic_card():
        p1 = subprocess.Popen(["hwinfo", "--gfxcard"], \
                              stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "Model:[[:space:]]"],\
                              stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        return p2.communicate()[0].decode()
        
    
    
    
    
    
    def install_packages(self):
        self.run_pacman()
        
        self.chroot_mount()
        
        #self.auto_addons()
        #self.auto_fstab()
        #self.auto_mdadm()
        #self.auto_luks()

        # tear down the chroot environment
        #self.chroot_umount()
        
        pass


    def run_pacman(self):
        # create chroot environment on target system
        # code straight from mkarchroot
        self.chroot_mount()
        
        self.pac.install_packages(self.packages)

        # ensure the disk is synced
        #self.sync()

        #self.chroot_umount()










    # creates temporary pacman.conf file
    def create_pacman_conf(self):

        print("Creating pacman.conf for %s architecture" % self.arch)
        
        # Common repos
        
        # Instead of hardcoding pacman.conf, we could use an external file
               
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

        self.pac = pac.Pac("/tmp/pacman.conf", self.callback_queue)
        
        #self.pac.set_callback('totaldl', self.pacman_cb_total_dl)
        #self.pac.set_callback('event', self.pacman_cb_event)
        #self.pac.set_callback('conv', self.pacman_cb_conv)
        #self.pac.set_callback('progress', self.pacman_cb_progress)
        #self.pac.set_callback('log', self.pacman_cb_log)
        
        
    # add gnupg pacman files to installed system
    # needs testing, but it seems to be the way to do it now
    # must be also changed in the CLI Installer
    def prepare_pacman_keychain(self):
        #removed / from etc to make path relative...
        dest_path = os.path.join(self.dest_dir, "etc/pacman.d/")
        #use copytree for cp -r
        try:
            shutil.copytree('/etc/pacman.d/gnupg', dest_path)
        except FileExistsError:
            #ignore if exists
            pass

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
        
