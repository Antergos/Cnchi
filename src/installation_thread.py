#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_thread.py
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

import threading
import subprocess
import os
import sys
import time
import shutil
import xml.etree.ElementTree as etree
from urllib.request import urlopen
import crypt

import config

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
_postinstall_script = 'postinstall.sh'

class InstallError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InstallationThread(threading.Thread):
    def __init__(self, settings, callback_queue, mount_devices, grub_device, fs_devices, ssd=None):
        threading.Thread.__init__(self)
        
        self.callback_queue = callback_queue
        self.settings = settings

        self.method = self.settings.get('partition_mode')
        
        self.queue_event('info', _("Installing using the '%s' method") % self.method)
        
        self.ssd = ssd
        self.mount_devices = mount_devices
        self.grub_device = grub_device

        # Check desktop selected to load packages needed
        self.desktop = self.settings.get('desktop')
        self.desktop_manager = 'gdm'
    
        self.fs_devices = fs_devices

        self.running = True
        self.error = False
    
    def queue_fatal_event(self, txt):
        self.error = True
        self.running = False
        self.queue_event('error', txt)
         
    def queue_event(self, event_type, event_text=""):
        self.callback_queue.put((event_type, event_text))

    @misc.raise_privileges    
    def run(self):
        # Common vars
        self.packages = []
        
        self.dest_dir = "/install"
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)

        self.kernel_pkg = "linux"
        self.vmlinuz = "vmlinuz-%s" % self.kernel_pkg
        self.initramfs = "initramfs-%s" % self.kernel_pkg       

        self.arch = os.uname()[-1]
        
        ## Create/Format partitions
        
        if self.method == 'automatic':
            self.auto_device = self.mount_devices["/"].replace("3","")
            cnchi_dir = self.settings.get("CNCHI_DIR")
            script_path = os.path.join(cnchi_dir, "scripts", _autopartition_script)
            try:
                self.queue_event('debug', "Automatic device: %s" % self.auto_device)
                self.queue_event('debug', "Running automatic script...")
                subprocess.check_call(["/bin/bash", script_path, self.auto_device])
                self.queue_event('debug', "Automatic script done.")
            except subprocess.FileNotFoundError as e:
                self.queue_fatal_event(_("Can't execute the auto partition script"))
                return False
            except subprocess.CalledProcessError as e:
                self.queue_fatal_event("CalledProcessError.output = %s" % e.output)
                return False                  
        
        if self.method == 'easy' or self.method == 'advanced':
            root_partition = self.mount_devices["/"]
            if "/boot" in self.mount_devices:
                boot_partition = self.mount_devices["/boot"]
            else:
                boot_partition = ""
            # Easy and avanced methods format root by default
            (error, msg) = fs.create_fs(self.mount_devices["/"], "ext4")

        if self.method == 'advanced':
            # TODO: format partitions using mkfs (but which ones?)
            # Is this really necessary? Won't they be previously formatted in
            # installation_advanced?
            pass

        # Create the directory where we will mount our new root partition
        if not os.path.exists(self.dest_dir):
            os.mkdir(self.dest_dir)

        # Mount root and boot partitions (only if it's needed)
        if self.method == 'easy' or self.method == 'advanced':
            # not doing this in automatic mode as our script mounts the root and boot devices
            try:
                subprocess.check_call(['mount', root_partition, self.dest_dir])
                # We also mount the boot partition if it's needed
                subprocess.check_call(['mkdir', '-p', '%s/boot' % self.dest_dir]) 
                if "/boot" in self.mount_devices:
                    subprocess.check_call(['mount', boot_partition, "%s/boot" % self.dest_dir])
            except subprocess.CalledProcessError as e:
                self.queue_fatal_event(_("Couldn't mount root and boot partitions"))
                return False
        
        # In advanced mode, mount all partitions (root and boot are already mounted)
        if self.method == 'advanced':
            for path in self.mount_devices:
                mp = self.mount_devices[path]
                # Root and Boot are already mounted.
                # Just try to mount all the rest.
                if mp != root_partition and mp != boot_partition:
                    try:
                        mount_dir = self.dest_dir + path
                        if not os.path.exists(mount_dir):
                            os.mkdir(mount_dir)
                        subprocess.check_call(['mount', mp, mount_dir])
                    except subprocess.CalledProcessError as e:
                        # we try to continue as root and boot mounted ok
                        self.queue_event('debug', _("Can't mount %s in %s") % (mp, mount_dir))
                        # self.queue_fatal_event(_("Couldn't mount %s") % mount_dir)
                        # return False

        try:
            subprocess.check_call(['mkdir', '-p', '%s/var/lib/pacman' % self.dest_dir])
            subprocess.check_call(['mkdir', '-p', '%s/etc/pacman.d/gnupg/' % self.dest_dir])
            subprocess.check_call(['mkdir', '-p', '%s/var/log/' % self.dest_dir]) 
        except subprocess.CalledProcessError as e:
            self.queue_fatal_event(_("Can't create necessary directories on destination system"))
            return False

        try:
            self.queue_event('debug', 'Selecting packages...')
            self.select_packages()
            self.queue_event('debug', 'Packages selected')
            
            self.queue_event('debug', 'Installing packages...')
            self.install_packages()
            self.queue_event('debug', 'Packages installed.')

            self.queue_event('debug', 'Installing bootloader...')
            self.install_bootloader()
            self.queue_event('debug', 'Bootloader installed.')

            self.queue_event('debug', 'Configuring system...')
            self.configure_system()
            self.queue_event('debug', 'System configured.')            
        except subprocess.CalledProcessError as e:
            self.queue_fatal_event("CalledProcessError.output = %s" % e.output)
            return False
        except InstallError as e:
            self.queue_fatal_event(e.value)
            return False

        # installation finished ok
        self.queue_event("finished")
        self.running = False
        return True

    # creates temporary pacman.conf file
    def create_pacman_conf(self):
        self.queue_event('debug', "Creating pacman.conf for %s architecture" % self.arch)
        
        # Common repos
        
        # Instead of hardcoding pacman.conf, we could use an external file

        with open("/tmp/pacman.conf", "wt") as tmp_file:
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

            tmp_file.write("#### Antergos repos start here\n")
            tmp_file.write("[antergos]\n") 
            tmp_file.write("SigLevel = PackageRequired\n")
            tmp_file.write("Include = /etc/pacman.d/antergos-mirrorlist\n\n")
            tmp_file.write("#### Antergos repos end here\n\n")
        
        ## Init pyalpm

        try:
            self.pac = pac.Pac("/tmp/pacman.conf", self.callback_queue)
        except:
            raise InstallError("Can't initialize pyalpm.")
        
    # Add gnupg pacman files to installed system
    # Needs testing, but it seems to be the way to do it now
    # Must be also changed in the CLI Installer
    def prepare_pacman_keychain(self):
        # removed / from etc to make path relative...
        dest_path = os.path.join(self.dest_dir, "etc/pacman.d/gnupg")
        # use copytree for cp -r
        try:
            misc.copytree('/etc/pacman.d/gnupg', dest_path)
        except FileExistsError:
            # ignore if exists
            pass

    # Configures pacman and syncs db on destination system
    def prepare_pacman(self):
        dirs = [ "var/cache/pacman/pkg", "var/lib/pacman" ]
        
        for d in dirs:
            mydir = os.path.join(self.dest_dir, d)
            if not os.path.exists(mydir):
                os.makedirs(mydir)

        self.prepare_pacman_keychain()
        
        self.pac.do_refresh()

    # Prepare pacman and get package list from Internet
    def select_packages(self):
        self.create_pacman_conf()
        self.prepare_pacman()
        
        '''The list of packages is retrieved from an online XML to let us
        control the pkgname in case of any modification'''
        
        self.queue_event('info', "Getting package list...")

        try:
            packages_xml = urlopen('http://install.antergos.com/packages.xml')
        except URLError as e:
            # If the installer can't retrieve the remote file, try to install with a local
            # copy, that may not be updated
            self.queue_event('error', "Can't retrieve remote package list. Local file instead.")
            data_dir = self.settings.get("DATA_DIR")
            packages_xml = os.path.join(data_dir, 'packages.xml')
            return False

        tree = etree.parse(packages_xml)
        root = tree.getroot()

        self.queue_event('debug', "Adding base packages")

        for child in root.iter('common_system'):
            for pkg in child.iter('pkgname'):
                self.packages.append(pkg.text)

        self.queue_event('debug', "Adding desktop packages")

        for child in root.iter(self.desktop + '_desktop'):
            for pkg in child.iter('pkgname'):
                if pkg.attrib.get('desktop-manager'):
                    self.desktop_manager = pkg.text
                self.packages.append(pkg.text)
        
        if self.settings.get("use_ntp"):
            for child in root.iter('ntp'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        graphics = self.get_graphics_card()
        
        self.card = ""

        if "ati " in graphics:
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
        
        if "via " in graphics:
            for child in root.iter('via'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
        
        wlan = subprocess.check_output(\
            ["hwinfo", "--wlan", "--short"]).decode()

        if "broadcom" in wlan:
            for child in root.iter('broadcom'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
        
        # Add filesystem packages
        
        self.queue_event('debug', "Adding filesystem packages")       
        
        fs_types = subprocess.check_output(\
            ["blkid", "-c", "/dev/null", "-o", "value", "-s", "TYPE"]).decode()

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

        self.queue_event('debug', 'Selecting chinese fonts.')

        # Install chinese fonts
        lang_code = self.settings.get("language_code")
        if lang_code == "zh_TW" or lang_code == "zh_CN":
            for child in root.iter('chinese'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        # Lets start from a basic install, installing grub2 (bios) by default
        for child in root.iter('grub'):
            for pkg in child.iter('pkgname'):
                self.packages.append(pkg.text)

    def get_graphics_card(self):
        p1 = subprocess.Popen(["hwinfo", "--gfxcard"], \
                              stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "Model:[[:space:]]"],\
                              stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        out, err = p2.communicate()
        return out.decode().lower()
    
    def install_packages(self):
        self.chroot_mount()        
        self.run_pacman()
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

        subprocess.check_call(["mount", "-t", "sysfs", "sysfs", mydir])
        subprocess.check_call(["chmod", "555", mydir])

        mydir = os.path.join(self.dest_dir, "proc")
        subprocess.check_call(["mount", "-t", "proc", "proc", mydir])
        subprocess.check_call(["chmod", "555", mydir])

        mydir = os.path.join(self.dest_dir, "dev")
        subprocess.check_call(["mount", "-o", "bind", "/dev", mydir])
        
    def chroot_umount(self):
        dirs = [ "proc", "sys", "dev" ]
        
        for d in dirs:
            mydir = os.path.join(self.dest_dir, d)
            subprocess.check_call(["umount", mydir])

    def chroot(self, cmd, stdin=None, stdout=None):
        run = ['chroot', self.dest_dir]
        
        for c in cmd:
            run.append(c)
      
        try:
            proc = subprocess.Popen(run,
                                    stdin=stdin,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate()[0]
        except OSError as e:
            print("Error running command: %s" % e.strerror)
            raise
        
        
    def is_running(self):
        return self.running

    def is_ok(self):
        return not self.error

    def copy_network_config(self):
        source_nm = "/etc/NetworkManager/system-connections/"
        target_nm = "%s/etc/NetworkManager/system-connections/" % self.dest_dir

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

    # TODO: Take care of swap partitions
    def auto_fstab(self):
        all_lines = []
        all_lines.append("# /etc/fstab: static file system information.")
        all_lines.append("#")
        all_lines.append("# Use 'blkid' to print the universally unique identifier for a")
        all_lines.append("# device; this may be used with UUID= as a more robust way to name devices")
        all_lines.append("# that works even if disks are added and removed. See fstab(5).")
        all_lines.append("#")
        all_lines.append("# <file system> <mount point>   <type>  <options>       <dump>  <pass>")
        all_lines.append("#")

        root_ssd = 0

        for path in self.mount_devices:
            opts = 'defaults'
            chk = '0'
            parti = self.mount_devices[path]
            info = fs.get_info(parti)
            uuid = info['UUID']
            if parti in self.fs_devices:
                myfmt = self.fs_devices[parti]
            else:
                # It hasn't any filesystem defined (maybe swap?)
                # TODO: don't skip it and mount it as it should be if it is a swap partition
                continue

            if path == '/':
                chk = '1'
                opts = "rw,relatime,data=ordered"
            else:
                full_path = os.path.join(self.dest_dir, path)
                subprocess.check_call(["mkdir", "-p", full_path])

            if self.ssd != None:
                for i in self.ssd:
                    if i in self.mount_devices[path] and self.ssd[i]:
                        opts = 'defaults,noatime,nodiratime'
                        # As of linux kernel version 3.7, the following
                        # filesystems support TRIM: ext4, btrfs, JFS, and XFS.
                        # If using a TRIM supported SSD, discard is a valid mount option for swap
                        if myfmt == 'ext4' or myfmt == 'btrfs' or myfmt == 'jfs' or myfmt == 'xfs' or myfmt == 'swap':
                            opts += ',discard'
                        if path == '/':
                            root_ssd = 1

            all_lines.append("UUID=%s %s %s %s 0 %s" % (uuid, path, myfmt, opts, chk))

        if root_ssd:
            all_lines.append("tmpfs /tmp tmpfs defaults,noatime,mode=1777 0 0")

        full_text = '\n'.join(all_lines)

        with open('/install/etc/fstab','w') as f:
            f.write(full_text)

    def install_bootloader(self):
        # TODO: Install Grub2
        # check dogrub_config and dogrub_bios from arch-setup

        self.queue_event('info', "Installing GRUB(2) BIOS boot loader in %s" % self.grub_device)
        self.chroot_mount()

        self.chroot(['grub-install', \
                  '--directory=/usr/lib/grub/i386-pc', \
                  '--target=i386-pc', \
                  '--boot-directory=/boot', \
                  '--recheck', \
                  self.grub_device])
        
        grub_d_dir = os.path.join(self.dest_dir, "etc/grub.d")
        
        if not os.path.exists(grub_d_dir):
            os.makedirs(grub_d_dir)

        try:
            shutil.copy2("/arch/10_linux", grub_d_dir)
        except FileNotFoundError:
            self.chroot_umount()            
            self.queue_event('warning', _("ERROR installing GRUB(2) BIOS."))
            return
        except FileExistsError:
            # ignore if exists
            pass

        self.chroot(['/usr/sbin/grub-mkconfig', '-o', '/boot/grub/grub.cfg'])
        
        self.chroot_umount()

        core_path = os.path.join(self.dest_dir, "boot/grub/i386-pc/core.img")
        
        if os.path.exists(core_path):
            self.queue_event('info', _("GRUB(2) BIOS has been successfully installed."))
            try:
                code = self.settings.get("language_code")[0:2]
                shutil.copy2("%s/boot/grub/locale/en@quot.mo" % self.dest_dir, 
                             "%s/boot/grub/locale/%s.mo.gz" % (self.dest_dir, code))
            except FileExistsError:
                # ignore if exists
                pass
        else:
            self.queue_event('warning', _("ERROR installing GRUB(2) BIOS."))

    def enable_services(self, services):
        for name in services:
            name += '.service'
            self.chroot(['systemctl', 'enable', name])

    def change_user_password(self, user, new_password):
        try:
            shadow_password = crypt.crypt(new_password,"$6$%s$" % user)
        except:
            self.queue_event('warning', _('Error creating password hash for user %s') % user)
            return False

        try:
            self.chroot(['usermod', '-p', shadow_password, user])
        except:
            self.queue_event('warning', _('Error changing password for user %s') % user)
            return False
        
        return True

    def auto_timesetting(self):
        subprocess.check_call(["hwclock", "--systohc", "--utc"])
        shutil.copy2("/etc/adjtime", "%s/etc/" % self.dest_dir)

    # runs mkinitcpio on the target system
    def run_mkinitcpio(self):
        self.chroot_mount()
        self.chroot(["/usr/bin/mkinitcpio", "-p", self.kernel_pkg])
        self.chroot_umount()

    # Uncomment selected locale in /etc/locale.gen
    def uncomment_locale_gen(self, locale):
        #self.chroot(['sed', '-i', '-r', '"s/#(.*%s)/\1/g"' % locale, "/etc/locale.gen"])
            
        text = []
        with open("%s/etc/locale.gen" % self.dest_dir, "rt") as gen:
            text = gen.readlines()
        
        with open("%s/etc/locale.gen" % self.dest_dir, "wt") as gen:
            for line in text:
                if locale in line and line[0] == "#":
                    # uncomment line
                    line = line[1:]
                gen.write(line)
        
    def configure_system(self):
        # final install steps
        # set clock, language, timezone
        # run mkinitcpio
        # populate pacman keyring
        # setup systemd services
        # ... check configure_system from arch-setup

        # Generate the fstab file        
        self.auto_fstab()
        #Copy configured networks in Live medium to target system
        self.copy_network_config()

        # copy mirror list
        shutil.copy2('/etc/pacman.d/mirrorlist', \
                    os.path.join(self.dest_dir, 'etc/pacman.d/mirrorlist'))       

        self.queue_event("action", _("Configuring your new system"))

        # Copy important config files to target system
        files = [ "/etc/pacman.conf", "/etc/yaourtrc" ]        
        
        for path in files:
            shutil.copy2(path, os.path.join(self.dest_dir, 'etc/'))

        # enable services      
        self.enable_services([ self.desktop_manager, "NetworkManager" ])

        # TODO: we never ask the user about this...
        if self.settings.get("use_ntp"):
            self.enable_services([ "ntpd" ])

        # Wait FOREVER until the user sets the timezone
        while self.settings.get('timezone_done') is False:
            # wait five seconds and try again
            time.sleep(5)

        # set timezone
        zoneinfo_path = os.path.join("/usr/share/zoneinfo", \
                                     self.settings.get("timezone_zone"))
        self.chroot(['ln', '-s', zoneinfo_path, "/etc/localtime"])
        
        # Wait FOREVER until the user sets his params
        while self.settings.get('user_info_done') is False:
            # wait five seconds and try again
            time.sleep(5)         

        # Set user parameters
        username = self.settings.get('username')
        fullname = self.settings.get('fullname')
        password = self.settings.get('password')
        hostname = self.settings.get('hostname')
        
        sudoers_path = os.path.join(self.dest_dir, "etc/sudoers")
        with open(sudoers_path, "wt") as sudoers:
            sudoers.write('# Sudoers file\n')
            sudoers.write('root ALL=(ALL) ALL\n')
            sudoers.write('%s ALL=(ALL) ALL\n' % username)
        
        subprocess.check_call(["chmod", "440", sudoers_path])
        
        try:
            misc.copytree('/etc/skel', os.path.join(self.dest_dir, "etc/skel"))
        except FileExistsError:
            # ignore if exists
            pass

        process = subprocess.check_call(["rm", "-rf", "%s/etc/skel/Desktop" % self.dest_dir])
        
        self.chroot(['useradd', '-m', '-s', '/bin/bash', \
                  '-g', 'users', '-G', 'lp,video,network,storage,wheel,audio', \
                  username])

        self.change_user_password(username, password)

        self.chroot(['chfn', '-f', fullname, username])
        
        try:
            misc.copytree('/etc/skel', os.path.join(self.dest_dir, "home/%s" % username))
        except FileExistsError:
            # ignore if exists
            pass

        self.chroot(['chown', '-R', '%s:users' % username, "/home/%s" % username])
        
        hostname_path = os.path.join(self.dest_dir, "etc/hostname")
        if not os.path.exists(hostname_path):
            with open(hostname_path, "wt") as f:
                f.write(hostname)
        
        # User password is the root password  
        self.change_user_password('root', password)

        ## Generate locales
        lang_code = self.settings.get("language_code")
        locale = self.settings.get("locale")
        self.queue_event('info', _("Generating locales"))
        
        self.uncomment_locale_gen(locale)
        
        self.chroot(['locale-gen'])
        locale_conf_path = os.path.join(self.dest_dir, "etc/locale.conf")
        with open(locale_conf_path, "wt") as locale_conf:
            locale_conf.write('LANG=%s \n' % locale)
            locale_conf.write('LC_COLLATE=C \n')
            
        # Set /etc/vconsole.conf
        vconsole_conf_path = os.path.join(self.dest_dir, "etc/vconsole.conf")
        with open(vconsole_conf_path, "wt") as vconsole_conf:
            vconsole_conf.write('KEYMAP=%s \n' % lang_code)

        self.auto_timesetting()

        # Let's start without using hwdetect for mkinitcpio.conf.
        # I think it should work out of the box most of the time.
        # This way we don't have to fix deprecated hooks.    
        self.queue_event('info', _("Running mkinitcpio"))
        self.run_mkinitcpio()
        
        # TODO: Mirrorlist has to be generated using our rank-mirrorlist script
        # located in /arch and then copy that generated file to the target system.
        # In the CLI installer I'm running this script when the user opens the installer,
        # because it has to search for the 5 fastest mirrors, which takes time.
        
        # Ok, we already did this before, in another thread
        
        # Call post-install script
        script_path_postinstall = os.path.join(self.settings.get("CNCHI_DIR"), \
            "scripts", _postinstall_script)
        subprocess.check_call(["/bin/bash", script_path_postinstall, username, self.dest_dir, self.desktop])
