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

class InstallError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InstallationThread(threading.Thread):
    def __init__(self, callback_queue, mount_devices, grub_device, format_devices=None, ssd=None):
        threading.Thread.__init__(self)
        
        self.callback_queue = callback_queue

        self.method = installer_settings['partition_mode']
        
        self.queue_event('info', _("Installing using the '%s' method") % self.method)
        
        self.ssd = ssd
        self.mount_devices = mount_devices
        self.grub_device = grub_device
    
        #print(mount_devices)

        self.format_devices = format_devices

        self.running = True
        self.error = False
    
    def queue_fatal_event(self, txt):
        self.error = True
        self.running = False
        self.queue_event('error', txt)
         
    def queue_event(self, event_type, event_text=""):
        self.callback_queue.put((event_type, event_text))
        print("Queued an event of type %s : %s" % (event_type, event_text))

    @misc.raise_privileges    
    def run(self):
        # Common vars
        self.packages = []
        
        self.dest_dir = "/install"
        self.kernel_pkg = "linux"
        self.vmlinuz = "vmlinuz-%s" % self.kernel_pkg
        self.initramfs = "initramfs-%s" % self.kernel_pkg       

        self.arch = os.uname()[-1]
        
        ## Create/Format partitions
        
        # TODO: Check if /boot is in another partition than root.
        # (and then mount it)
        
        if self.method == 'automatic':
            script_path = os.path.join(installer_settings["CNCHI_DIR"], \
                "scripts", _autopartition_script)
            try:
                if os.path.exists(script_path):
                    self.auto_device = self.mount_devices["automatic"]
                    self.queue_event('debug', "Automatic device: %s" % self.auto_device)
                    subprocess.check_call(["/bin/bash", script_path, \
                                     self.auto_device])
            except subprocess.FileNotFoundError as e:
                self.queue_fatal_event(_("Can't execute the auto partition script"))
                return False
            except subprocess.CalledProcessError as e:
                self.queue_fatal_event("CalledProcessError.output = %s" % e.output)
                return False
        
        if self.method == 'easy' or self.method == 'advanced':
            # TODO: format partitions using mkfs (format_devices)
            pass

        # Create the directory where we will mount our new root partition
        if not os.path.exists(self.dest_dir):
            os.mkdir(self.dest_dir)
            
        if self.method == 'automatic':
            # In automatic install we have (Alex F, check this out please!)
            # /dev/sdX1 boot
            # /dev/sdX2 swap
            # /dev/sdX3 root
            boot_partition = self.auto_device + "1"
            root_partition = self.auto_device + "3"
        elif self.method == 'easy':
            # we don't create a specific boot partition in easy mode (this could change in the future)
            boot_partition = ""
            root_partition = self.mount_devices["/"]
        elif self.method == 'advanced':
            boot_partition = self.mount_devices["/boot"]
            root_partition = self.mount_devices["/"]
            
        try:
            subprocess.check_call(['mount', root_partition, self.dest_dir])
            subprocess.check_call(['mkdir', '-p', '%s/var/lib/pacman' % self.dest_dir])
            subprocess.check_call(['mkdir', '-p', '%s/etc/pacman.d/gnupg/' % self.dest_dir])
            subprocess.check_call(['mkdir', '-p', '%s/var/log/' % self.dest_dir]) 
            
            # We also mount the boot partition if it's needed
            subprocess.check_call(['mkdir', '-p', '%s/boot' % self.dest_dir]) 
            if len(boot_partition) > 0:
                subprocess.check_call(['mount', boot_partition, "%s/boot" % self.dest_dir])
        except subprocess.CalledProcessError as e:
            self.queue_fatal_event("CalledProcessError.output = %s" % e.output)
            return False

        ## Do real installation here

        try:
            self.select_packages()
            self.install_packages()
            self.install_bootloader()
            self.configure_system()
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

            tmp_file.write("#### Cinnarch repos start here\n")
            tmp_file.write("[cinnarch-core]\n") 
            tmp_file.write("SigLevel = PackageRequired\n")
            tmp_file.write("Include = /etc/pacman.d/cinnarch-mirrorlist\n\n")

            tmp_file.write("[cinnarch-repo]\n")
            tmp_file.write("SigLevel = PackageRequired\n")
            tmp_file.write("Include = /etc/pacman.d/cinnarch-mirrorlist\n")
            tmp_file.write("#### Cinnarch repos end here\n\n")
        
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
        if self.is_uvesafb():
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
        
        wlan = subprocess.check_output(\
            ["hwinfo", "--wlan", "--short"]).decode()

        if "broadcom" in wlan:
            for child in root.iter('broadcom'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)
        
        # Add filesystem packages
        
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
        out, err = p2.communicate()
        return out.decode()
    
    def is_uvesafb(self):
        out = subprocess.check_output(["grep", "-w", "uvesafb", "/proc/cmdline"])
        if len(out) > 0:
            return True
        else:
            return False
    
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

    def chroot(self, cmd):
        run = ['chroot', self.dest_dir]
        
        for c in cmd:
            run.append(c)
                
        subprocess.check_call(run)
        
        
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
        for path in self.mount_devices:
            opts = 'defaults'
            parti = self.mount_devices[path]
            info = fs.get_info(parti)
            uuid = info['UUID']
            myfmt = self.format_devices[parti]
            if path == '/':
                chk = '1'
            else:
                chk = '0'
                full_path = os.path.join(self.dest_dir, path)
                subprocess.check_call(["mkdir", "-p", full_path])

            for i in self.ssd:
                if i in self.mount_devices[path]:
                    if self.ssd[i]:
                        opts = 'defaults,noatime,nodiratime,discard'
                        if path == '/':
                            rootssd = 1
                    else:
                        opts = 'defaults'

            all_lines.append("UUID=%s %s %s %s 0 %s" % (uuid, path, myfmt, opts, chk))

        if rootssd:
            all_lines.append("tmpfs /tmp tmpfs defaults,noatime,mode=1777 0 0")

        full_text = '\n'.join(all_lines)

        with open('/install/etc/fstab','w') as f:
            f.write(full_text)

    def install_bootloader(self):
        # TODO: Install Grub2
        # check dogrub_config and dogrub_bios from arch-setup

        self.queue_event('info', "Installing GRUB(2) BIOS boot loader in %s" % self.grub_device)
        self.chroot_mount()

        self.chroot(['/usr/sbin/grub-install', \
                  '--directory="/usr/lib/grub/i386-pc"', \
                  '--target="i386-pc"', \
                  '--boot-directory="/boot"', \
                  '--recheck', \
                  '--debug', \
                  self.grub_device])
        
        grub_log = '/tmp/grub_bios_install.log'

        grub_d_dir = os.path.join(self.dest_dir, "etc/grub.d")
        
        if not os.path.exists(grub_d_dir):
            os.makedirs(grub_d_dir)

        try:
            misc.copytree("/arch/10_linux", grub_d_dir)
        except FileExistsError:
            # ignore if exists
            pass

        self.chroot(['/usr/sbin/grub-mkconfig', '-o', \
                  '/boot/grub/grub.cfg'])
        
        self.chroot_umount()

        core_path = os.path.join(self.dest_dir,\
                    "boot/grub/i386-pc/core.img")
        
        if os.path.exists(core_path):
            self.queue_event('info', _("GRUB(2) BIOS has been successfully installed."))
        else:
            # should we stop installation here?
            self.queue_event('warning', _("ERROR installing GRUB(2) BIOS."))

    # Wait for an installer_settings var change with a timeout
    # Timeout is in seconds (by default wait 5 minutes)
    def wait_true(self, var, timeout=300):
        import time

        # set initial time and initial variables
        start_time = time.time()
        elapsed_time = 0
        
        self.queue_event('debug', "Waiting for user to fill %s..." % var)

        while installer_settings[var] == False and \
              elapsed_time < timeout:
            elapsed_time = time.time() - start_time

        if elapsed_time < timeout:
            return False
        else:
            return True

    def enable_services(self, services):
        for name in services:
            name += '.service'
            self.chroot(['systemctl', 'enable', name])

    def change_user_password(self, user, new_password):
        process = subprocess.Popen(['mkpasswd', '-m', 'sha-512', new_password], stdout=subprocess.PIPE)
        shadow_password = process.communicate()[0].strip()

        if process.returncode != 0:
            self.queue_event('warning', _('Error creating password hash for user %s') % user)
            return False

        result = subprocess.call(['usermod', '-p', shadow_password, user])

        if result != 0:
            self.queue_event('warning', _('Error changing password for user %s') % user)
            return False
        
        return True

    def auto_timesetting(self):
        subprocess.check_call(["hwclock", "--systohc", "--utc"])
        shutil.copy("/etc/adjtime", "%s/etc/adjtime" % self.dest_dir)

    # runs mkinitcpio on the target system
    def run_mkinitcpio(self):
        self.chroot_mount()
        self.chroot(["/usr/bin/mkinitcpio", "-p", self.kernel_pkg])
        self.chroot_umount()
        
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

        # copy cinnarch menu icon
        cinnarch_path = os.path.join(self.dest_dir, "usr/share/cinnarch")
        if not os.path.exists(cinnarch_path):
            os.makedirs(cinnarch_path)
        shutil.copy('/usr/share/cinnarch/cinnarch_menu.png', \
                    os.path.join(cinnarch_path, 'cinnarch_menu.png'))

        # copy mirror list
        shutil.copy('/etc/pacman.d/mirrorlist', \
                    os.path.join(self.dest_dir, 'etc/pacman.d/mirrorlist'))       
        
        # TODO: set uvesa framebuffer if necessary
        if self.is_uvesafb():
            v86d_path = os.path.join(self.dest_dir, "lib/initcpio/hooks/v86d")
            if os.path.exists(v86d_path):
                # Help? I really don't know what grep/sed are doing here.
                pass
                '''
                UVESAFB="$(grep ^[a-z] /etc/modprobe.d/uvesafb.conf)" 
                sed -i -e "s#options.*#${UVESAFB}#g" ${DESTDIR}/etc/modprobe.d/uvesafb.conf
                '''

        self.queue_event("action", _("Configuring your new system"))

        # Copy important config files to target system
        files = [ "/etc/pacman.conf", "/etc/yaourtrc" ]        
        
        for path in files:
            shutil.copy(path, os.path.join(self.dest_dir, path))

        # enable services      
        self.enable_services([ "lightdm", "NetworkManager" ])

        # TODO: we never ask the user about this...
        if installer_settings["use_ntp"]:
            self.enable_services([ "ntpd" ])

        # set timezone       
        if self.wait_true('timezone_done'):
            zoneinfo_path = os.path.join("/usr/share/zoneinfo", \
                                         installer_settings["timezone_zone"])
            self.chroot(['ln', '-s', zoneinfo_path, "/etc/localtime"])
        
        # TODO: set user parameters
        if self.wait_true('user_done'):
            username = installer_settings['username']
            fullname = installer_settings['fullname']
            password = installer_settings['password']
            hostname = installer_settings['hostname']
            
            sudoers_path = os.path.join(self.dest_dir, "etc/sudoers")
            with open(sudoers_path, "wt") as sudoers:
                sudoers.write('# Sudoers file')
                sudoers.write('root ALL=(ALL) ALL')
                sudoers.write('%s ALL=(ALL) ALL' % username)
            
            subprocess.check_call(["chmod", "440", sudoers_path])
            
            self.queue_event('debug', _("Creating new user"))
            
            try:
                misc.copytree('/etc/skel', os.path.join(self.dest_dir, "etc"))
            except FileExistsError:
                # ignore if exists
                pass

            process = subprocess.check_call(["rm", "-rf", "%s/etc/skel" % self.dest_dir])
            
            self.chroot(['useradd', '-m', '-s', '/bin/bash', \
                      '-g', 'users', '-G', 'lp,video,network,storage,wheel,audio', \
                      username])

            self.change_user_password(username, password)

            self.chroot(['chfn', '-f', fullname, username])
                      
            home = os.path.join(self.dest_dir, "home", username)
            skel_dirs = ['/etc/skel/.config', '/etc/skel/.gconf', '/etc/skel/.cache', '/etc/skel/.local', '/etc/skel/.gnome2', '/etc/skel/.gtkrc-2']
            try:
                for d in skel_dirs:
                    misc.copytree(d, home)
            except FileExistsError:
                # ignore if exists
                pass
            
            self.chroot(['chown', '-R', '%s:users' % username, "/home/%s" % username])
            
            hostname_path = os.path.join(self.dest_dir, "etc/hostname")
            if not os.path.exists(hostname_path):
                with open(hostname_path, "wt") as f:
                    f.write(hostname)

            # TODO: At this point, cli installer allows to edit mkinitcpio.conf.
            # Let's start without using hwdetect for mkinitcpio.conf.
            # I think it should work out of the box most of the time.
            # This way we don't have to fix deprecated hooks.    
            
            self.run_mkinitcpio()
            
            # TODO: Should we ask for a password for root? Or we leave it as it is?
            # we could set the user password to be the root password (i like this!)
            # Or maybe we could just ask for root password like Fedora? What do you think?
            
            self.change_user_password('root', password)
            
            # Specific user configurations
            
            ## Set defaults directories
            self.chroot(["su", "-c", "xdg-user-dirs-update", username])

            ## Unmute alsa channels
            self.chroot(["amixer", "-c", "0", "set", "Master", "playback", "100%", "unmute"])

            ## Copy locales
            # TODO : I think we didn't store locale.gen in /tmp... ¿?¿?¿?
            shutil.copy("/tmp/locale.gen",  "%s/etc/locale.gen" % self.dest_dir)

            self.auto_timesetting()

            self.run_mkinitcpio()
            
            # TODO: Mirrorlist has to be generated using our rank-mirrorlist script
            # located in /arch and then copy that generated file to the target system.
            # In the CLI installer I'm running this script when the user opens the installer,
            # because it has to search for the 5 fastest mirrors, which takes time.
            
            # Ok, we should do this before, in another thread
            
            #self.search_for_fastest_mirrors()

            
            # TODO : To set the user locale, we just need to uncoment the
            # language_code variable value in /install/etc/locale.gen and
            # execute in chroot locale-gen
            '''
            # /etc/locale.gen
            sleep 2
            DIALOG --infobox $"Generating locales..." 4 25
            cp -f /tmp/locale.conf ${DESTDIR}/etc/locale.conf
            chroot ${DESTDIR} locale-gen >/dev/null 2>&1
            '''

            '''
            # Set gsettings
            cp /arch/set-gsettings ${DESTDIR}/usr/bin/set-gsettings
            mkdir -p ${DESTDIR}/var/run/dbus
            mount -o bind /var/run/dbus ${DESTDIR}/var/run/dbus
            chroot ${DESTDIR} su -c "/usr/bin/set-gsettings" ${USER_NAME} >/dev/null 2>&1
            rm ${DESTDIR}/usr/bin/set-gsettings
            '''

            '''
            # Fix transmission leftover
            mv ${DESTDIR}/usr/lib/tmpfiles.d/transmission.conf ${DESTDIR}/usr/lib/tmpfiles.d/transmission.conf.backup

            # Configure touchpad
            _set_50-synaptics
            # cp /etc/X11/xorg.conf.d/10-synaptics.conf ${DESTDIR}/etc/X11/xorg.conf.d/10-synaptics.conf

            # Fix grub locale error
            chroot ${DESTDIR} cp "/boot/grub/locale/en@quot.mo" "/boot/grub/locale/$(echo ${LOCALE}|cut -b 1-2).mo.gz"

            # Fix QT apps
            echo 'export GTK2_RC_FILES="$HOME/.gtkrc-2.0"' >> ${DESTDIR}/etc/bash.bashrc

            # Change pantheon-greeter wallpaper
            chroot ${DESTDIR} unlink /usr/share/backgrounds/cinnarch-default
            chroot ${DESTDIR} ln -s /usr/share/cinnarch/wallpapers/83II_by_bo0xVn.jpg /usr/share/backgrounds/cinnarch-default

            # Set Cinnarch name in filesystem files
            cp /etc/arch-release ${DESTDIR}/etc
            cp /etc/issue ${DESTDIR}/etc
            cp -f /etc/os-release ${DESTDIR}/etc/os-release

            # Set Adwaita cursor theme
            chroot ${DESTDIR} ln -s /usr/share/icons/Adwaita /usr/share/icons/default

            # Fix multilib repo in last release
            cp -f /etc/pacman.conf ${DESTDIR}/etc/pacman.conf

            if [[ $(uname -m) = 'x86_64' ]];then
                echo "" >> ${DESTDIR}/etc/pacman.conf
                echo "[multilib]" >> ${DESTDIR}/etc/pacman.conf
                echo "SigLevel = PackageRequired" >> ${DESTDIR}/etc/pacman.conf
                echo "Include = /etc/pacman.d/mirrorlist" >> ${DESTDIR}/etc/pacman.conf
            fi
            '''
