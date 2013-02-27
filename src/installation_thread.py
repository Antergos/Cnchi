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
import xml.etree.ElementTree as etree
from urllib.request import urlopen

from config import installer_settings

# Insert the src/pacman directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
pacman_dir = os.path.join(base_dir, 'pacman')
sys.path.insert(0, pacman_dir)

# Insert the src/parted directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
parted_dir = os.path.join(base_dir, 'parted')
sys.path.insert(0, parted_dir)

import fs_module as fs
import misc

import pac

_autopartition_script = 'auto_partition.sh'

class InstallationThread(threading.Thread):
    def __init__(self, callback_queue, mount_devices, format_devices=None, ssd=None):
        threading.Thread.__init__(self)
        
        self.callback_queue = callback_queue

        self.method = installer_settings['partition_mode']
        
        print("Installing using '%s' method" % self.method)
        self.ssd = ssd
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
        # TODO: Check if /boot is in another partition than root!!!!
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
        elif self.method == 'advanced':
            if not os.path.exists('/install'):
                os.mkdir('/install')
            boot_partition = self.mount_devices["/boot"]
            root_partition = self.mount_devices["/"]
            subprocess.getoutput('mount %s /install' % root_partition)
            subprocess.getoutput('mkdir -p /install/var/lib/pacman')
            subprocess.getoutput('mkdir -p /install/etc/pacman.d/gnupg/')
            subprocess.getoutput('mkdir -p /install/var/log/') 
        elif self.method == 'easy' or self.method == 'advanced':
            # TODO: format partitions using mkfs (format_devices)
            pass

        if self.error:
            self.running = False
            return
            
        ## Do real installation here

        self.packages = []
        
        self.dest_dir = "/install"
        self.kernel_pkg = "linux"
        self.vmlinuz = "vmlinuz-%s" % self.kernel_pkg
        self.initramfs = "initramfs-%s" % self.kernel_pkg       

        self.arch = os.uname()[-1]
    
        # List of tasks

        self.select_packages()
        self.install_packages()
        self.install_bootloader(boot_partition)
        self.configure_system()

        # installation finished (0 means no error)
        self.callback_queue.put(("finished", 0))

        self.running = False

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

        tmp_file.write("#### Cinnarch repos start here\n")
        tmp_file.write("[cinnarch-core]\n") 
        tmp_file.write("SigLevel = PackageRequired\n")
        tmp_file.write("Include = /etc/pacman.d/cinnarch-mirrorlist\n\n")

        tmp_file.write("[cinnarch-repo]\n")
        tmp_file.write("SigLevel = PackageRequired\n")
        tmp_file.write("Include = /etc/pacman.d/cinnarch-mirrorlist\n")
        tmp_file.write("#### Cinnarch repos end here\n\n")

        tmp_file.close()
        
        ## Init pyalpm

        try:
            self.pac = pac.Pac("/tmp/pacman.conf", self.callback_queue)
        except:
            print("Can't initialize pyalpm. Aborting...")
            sys.exit(1)
        
    # add gnupg pacman files to installed system
    # needs testing, but it seems to be the way to do it now
    # must be also changed in the CLI Installer
    def prepare_pacman_keychain(self):
        #removed / from etc to make path relative...
        dest_path = os.path.join(self.dest_dir, "etc/pacman.d/gnupg")
        #use copytree for cp -r
        try:
            misc.copytree('/etc/pacman.d/gnupg', dest_path)
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

    def select_packages(self):
        self.create_pacman_conf()
        self.prepare_pacman()
        
        '''The list of packages is retrieved from an online XML to let us
        control the pkgname in case of any modification'''

        packages_xml=urlopen('http://install.cinnarch.com/packages.xml')
        tree = etree.parse(packages_xml)
        root = tree.getroot()
        for child in root.iter('base_system'):
            for pkg in child.iter('pkgname'):
                self.packages.append(pkg.text)
        with open('/proc/cmdline') as fp:
            for line in fp:
                if "uvesafb" in line:
                    for child in root.iter('uvesafb'):
                        for pkg in child.iter('pkgname'):
                            self.packages.append(pkg.text)
        
        if installer_settings["use_ntp"]:
            for child in root.iter('ntp'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        graphics = self.get_graphic_card()
        
        self.card = ""

        if "ati" in graphics:
            for child in root.iter('ati'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
            self.card = "ati"
        
        if "nvidia" in graphics:
            for child in root.iter('nvidia'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
            self.card = "nvidia"
        
        if "intel" in graphics or "lenovo" in graphics:
            for child in root.iter('intel'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
        
        if "virtualbox" in graphics:
            for child in root.iter('virtualbox'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
        
        if "vmware" in graphics:
            for child in root.iter('vmware'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
        
        if "via" in graphics:
            for child in root.iter('via'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
        
        wlan = subprocess.check_output(["hwinfo", "--wlan", "--short"]).decode()

        if "broadcom" in wlan:
            for child in root.iter('broadcom'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
        
        # Add filesystem packages
        
        fs_types = subprocess.check_output(["blkid", "-c", "/dev/null",\
                                            "-o", "value", "-s", "TYPE"]).decode()

        if "ntfs" in fs_types:
            for child in root.iter('ntfs'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
        
        if "btrfs" in fs_types:
            for child in root.iter('btrfs'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        if "nilfs2" in fs_types:
            for child in root.iter('nilfs2'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        if "ext" in fs_types:
            for child in root.iter('ext'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        if "reiserfs" in fs_types:
            for child in root.iter('reiserfs'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        if "xfs" in fs_types:
            for child in root.iter('xfs'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        if "jfs" in fs_types:
            for child in root.iter('jfs'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        if "vfat" in fs_types:
            for child in root.iter('vfat'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        # Install chinese fonts
        if installer_settings["language_code"] == "zh_TW" or \
           installer_settings["language_code"] == "zh_CN":
            for child in root.iter('chinese'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        # Lets start from a basic install, installing grub2 (bios) by default
        for child in root.iter('grub'):
            for pkg in child.iter('pkgname'):
                self.packages.append(pkg.text)

    def get_graphic_card(self):
        p1 = subprocess.Popen(["hwinfo", "--gfxcard"], \
                              stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "Model:[[:space:]]"],\
                              stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        return p2.communicate()[0].decode()
    
    def is_uvesafb(self):
        #grep -w uvesafb /proc/cmdline
        p = subprocess.Popen(["grep", "-w", "uvesafb", "/proc/cmdline"])
        out, err = p.comunicate()
        if len(out) > 0:
            return True
        else:
            return False
    
    def install_packages(self):
        # create chroot environment on target system
        self.chroot_mount()
        
        self.run_pacman()
        self.auto_fstab()
        self.copy_network_config()

        # tear down the chroot environment        
        self.chroot_umount()
    
    def run_pacman(self):
        self.pac.install_packages(self.packages)
    
    def chroot_mount(self):
        dirs = [ "sys", "proc", "dev" ]
        for d in dirs:
            mydir = os.path.join(self.dest_dir, d)
            if not os.path.exists(mydir):
                os.makedirs(mydir)

        mydir = os.path.join(self.dest_dir, "sys")
        subprocess.Popen(["mount", "-t", "sysfs", "sysfs", mydir])
        subprocess.Popen(["chmod", "555", mydir])

        mydir = os.path.join(self.dest_dir, "proc")
        subprocess.Popen(["mount", "-t", "proc", "proc", mydir])
        subprocess.Popen(["chmod", "555", mydir])

        mydir = os.path.join(self.dest_dir, "dev")
        subprocess.Popen(["mount", "-o", "bind", "/dev", mydir])
        
    def chroot_umount(self):
        dirs = [ "proc", "sys", "dev" ]
        
        for d in dirs:
            mydir = os.path.join(self.dest_dir, d)
            subprocess.Popen(["umount", mydir])

    def is_running(self):
        return self.running

    def is_ok(self):
        return not self.error

    def copy_network_config(self):
        source_nm = "/etc/NetworkManager/system-connections/"
        target_nm = "%s/etc/NetworkManager/system-connections/" % self.destdir

        # Sanity checks.  We don't want to do anything if a network
        # configuration already exists on the target
        if os.path.exists(source_nm) and os.path.exists(target_nm):
            for network in os.listdir(source_nm):
                # Skip LTSP live
                if network == "LTSP":
                    continue

                source_network = os.path.join(source_nm, network)
                target_network = os.path.join(target_nm, network)

                if os.path.exists(target_network):
                    continue

                shutil.copy(source_network, target_network)

    def auto_fstab(self):
        all_lines = []
        rootssd = 0
        for e in self.mount_devices:
            opts = 'defaults'
            parti = self.mount_devices[e]
            info = fs.get_info(parti)
            uuid = info['UUID']
            myfmt = self.format_devices[parti]
            if e == '/':
                chk = '1'
            else:
                chk = '0'
                #subprocess.getoutput('mkdir -p /install%s' % e)
                subprocess.Popen(["mkdir", "-p", os.path.join(self.dest_dir, e)])
            for i in self.ssd:
                if i in self.mount_devices[e]:
                    if self.ssd[i]:
                        opts = 'defaults,noatime,nodiratime,discard'
                        if e == '/':
                            rootssd = 1
                    else:
                        opts = 'defaults'
            all_lines.append("UUID=%s %s %s %s 0 %s" % (uuid, e, myfmt, opts, chk))
        if rootssd:
            all_lines.append("tmpfs /tmp tmpfs defaults,noatime,mode=1777 0 0")
        full_text = '\n'.join(all_lines)
        with open('/install/etc/fstab','w') as f:
            f.write(full_text)

    def grub_probe(self, target, device):
        probe_bin = 'LD_LIBRARY_PATH="%s/usr/lib:%s/lib" %s/usr/sbin/grub-probe' % (self.dest_dir, self.dest_dir, self.dest_dir)
        dst = os.path.join(self.dest_dir, device)
        process = subprocess.Popen([probe_bin, '--target="%s"' % target, dst], stdout=subprocess.PIPE)
        out, err = process.communicate()
        return out.decode()
        
    def install_bootloader(self, boot_partition):
        # TODO: Install Grub2
        # check dogrub_config and dogrub_bios from arch-setup

        print("Installing GRUB(2) BIOS boot loader in %s" % boot_partition)
        self.chroot_mount()

        process = subprocess.Popen(['chroot', \
                  self.dest_dir, \
                  '/usr/sbin/grub-install', \
                  '--directory="/usr/lib/grub/i386-pc"', \
                  '--target="i386-pc"', \
                  '--boot-directory="/boot"', \
                  '--recheck', \
                  '--debug', \
                  boot_partition])
        out, err = process.communicate()
        
        grub_log = '/tmp/grub_bios_install.log'

        with open(grub_log, 'w') as f:
            # should use .decode() on out before writing to disk?
            f.write(out)
            f.close()

        grub_d_dir = os.path.join(self.dest_dir, "etc/grub.d")
        
        if not os.path.exists(grub_d_dir):
            os.makedirs(grub_d_dir)

        misc.copytree("/arch/10_linux", grub_d_dir)

        process = subprocess.Popen(['chroot', \
                  self.dest_dir, \
                  '/usr/sbin/grub-mkconfig', \
                  '-o',
                  '/boot/grub/grub.cfg'])
        out, err = process.communicate()
        
        with open(grub_log, 'a') as f:
            # should use .decode() on out before writing to disk?
            f.write(out)
            f.close()

        self.chroot_umount()

        core_path = os.path.join(self.dest_dir, "boot/grub/i386-pc/core.img")
        
        if os.path.exists(core_path):
            print("GRUB(2) BIOS has been successfully installed.")
        else:
            print("ERROR installing GRUB(2) BIOS.")
        
    def configure_system(self):
        # final install steps
        # set clock, language, timezone
        # run mkinitcpio
        # populate pacman keyring
        # setup systemd services
        # ... check configure_system from arch-setup

        # copy cinnarch menu icon
        cinnarch_path = os.path.join(self.dest_dir, "usr/share/cinnarch")
        if not os.path.exists(cinnarch_path):
            os.makedirs(cinnarch_path)
        shutil.copy('/usr/share/cinnarch/cinnarch_menu.png', \
                    os.path.join(cinnarch_path, 'cinnarch_menu.png'))

        # copy mirror list
        shutil.copy('/etc/pacman.d/mirrorlist', \
                    os.path.join(self.dest_dir, 'etc/pacman.d/mirrorlist'))
        
        
        # TODO: set timezone
        '''
        if [[ -s  /tmp/.timezone ]]; then
            DIALOG --infobox $"Setting the timezone: $(cat /tmp/.timezone | sed -e 's/\..*//g') ..." 0 0
            chroot ${DESTDIR} ln -s /usr/share/zoneinfo/$(cat /tmp/.timezone | sed -e 's/\..*//g') /etc/localtime
                
        fi
        '''

        # TODO: set uvesa framebuffer if necessary
        '''
        if [[ -e ${DESTDIR}/lib/initcpio/hooks/v86d && "$(grep -w uvesafb /proc/cmdline)" ]]; then
            UVESAFB="$(grep ^[a-z] /etc/modprobe.d/uvesafb.conf)" 
            sed -i -e "s#options.*#${UVESAFB}#g" ${DESTDIR}/etc/modprobe.d/uvesafb.conf
        fi
        '''

        # TODO: use hwdetect to create /etc/mkinitcpio.conf (check auto_hwdetect from arch-setup)
        
        # TODO: populate keyring and setup systemd scripts
        '''
        cp -f /usr/bin/pacman-key ${DESTDIR}/usr/bin/pacman-key

        cp -f /usr/lib/systemd/system/lightdm.service ${DESTDIR}/usr/lib/systemd/system/lightdm.service
        cp -f /etc/systemd/system/pacman-init.service ${DESTDIR}/usr/lib/systemd/system/pacman-init.service
        chroot ${DESTDIR} systemctl enable lightdm.service NetworkManager.service pacman-init.service >/dev/null 2>&1
        if [[ -f /tmp/use_ntp ]];then
            chroot ${DESTDIR} systemctl enable ntpd.service >/dev/null 2>&1
        fi

        cp -f /etc/pacman.conf ${DESTDIR}/etc/pacman.conf
        cp -f /etc/yaourtrc ${DESTDIR}/etc/yaourtrc
        '''
        
        # TODO: set user parameters (to be done in user.py ¿?)
        

