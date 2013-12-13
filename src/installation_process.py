#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation_process.py
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

""" Installation thread module. Where the real installation happens """

import crypt
import download
import info
import logging
import multiprocessing
import os
import queue
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as etree
import encfs
import auto_partition
import parted3.fs_module as fs
import canonical.misc as misc
import pacman.pac as pac

POSTINSTALL_SCRIPT = 'postinstall.sh'

class InstallError(Exception):
    """ Exception class called upon an installer error """
    def __init__(self, value):
        """ Initialize exception class """
        super().__init__(value)
        self.value = value
    def __str__(self):
        """ Returns exception message """
        return repr(self.value)

class InstallationProcess(multiprocessing.Process):
    """ Installation process thread class """
    def __init__(self, settings, callback_queue, mount_devices, \
                 fs_devices, ssd=None, alternate_package_list="", blvm=False):
        """ Initialize installation class """
        multiprocessing.Process.__init__(self)

        self.alternate_package_list = alternate_package_list

        self.callback_queue = callback_queue
        self.settings = settings

        # Save how we have been called
        # We need this in case we have to retry the installation
        parameters = {'mount_devices' : mount_devices,
         'fs_devices' : fs_devices,
         'ssd' : ssd,
         'alternate_package_list' : alternate_package_list,
         'blvm': blvm }
        self.settings.set('installer_thread_call', parameters)

        # This flag tells us if there is a lvm partition (from advanced install)
        # If it's true we'll have to add the 'lvm2' hook to mkinitcpio
        self.blvm = blvm

        self.method = self.settings.get('partition_mode')

        self.queue_event('info', _("Installing using the '%s' method") % self.method)

        self.ssd = ssd
        self.mount_devices = mount_devices

        # Check desktop selected to load packages needed
        self.desktop = self.settings.get('desktop')

        # Set defaults
        self.desktop_manager = 'gdm'
        self.network_manager = 'NetworkManager'

        self.card = []
        # Packages to be removed
        self.conflicts = []

        self.fs_devices = fs_devices

        self.running = True
        self.error = False

        self.special_dirs_mounted = False

        # Initialize some vars that are correctly initialized elsewhere (pylint complains about it)
        self.auto_device = ""
        self.packages = []
        self.pac = None
        self.arch = ""
        self.initramfs = ""
        self.kernel_pkg = ""
        self.vmlinuz = ""
        self.features_by_desktop = {}
        self.dest_dir = ""

    def queue_fatal_event(self, txt):
        """ Queues the fatal event and exits process """
        self.error = True
        self.running = False
        self.queue_event('error', txt)
        self.callback_queue.join()
        # Is this really necessary?
        sys.exit(1)

    def queue_event(self, event_type, event_text=""):
        try:
            self.callback_queue.put_nowait((event_type, event_text))
        except queue.Full:
            pass

    @misc.raise_privileges
    def run(self):
        """ Run installation """
        # Common vars
        self.packages = []

        self.dest_dir = "/install"

        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)
        else:
            # If we're recovering from a failed/stoped install, there'll be
            # some mounted directories. Try to unmount them first.
            # We use unmount_all from auto_partition to do this.
            auto_partition.unmount_all(self.dest_dir)

        self.kernel_pkg = "linux"
        self.vmlinuz = "vmlinuz-%s" % self.kernel_pkg
        self.initramfs = "initramfs-%s" % self.kernel_pkg

        self.arch = os.uname()[-1]

        # Create and format partitions

        if self.method == 'automatic':
            self.auto_device = self.settings.get('auto_device')

            self.queue_event('debug', _("Creating partitions and their filesystems in %s") % self.auto_device)

            # If no key password is given a key file is generated and stored in /boot
            # (see auto_partition.py)

            try:
                auto = auto_partition.AutoPartition(self.dest_dir,
                                                    self.auto_device,
                                                    self.settings.get("use_luks"),
                                                    self.settings.get("use_lvm"),
                                                    self.settings.get("luks_key_pass"),
                                                    self.settings.get("use_home"),
                                                    self.callback_queue)
                auto.run()

                # Get mount_devices and fs_devices
                # (mount_devices will be used when configuring GRUB in modify_grub_default)
                # (fs_devices  will be used when configuring the fstab file)
                self.mount_devices = auto.get_mount_devices()
                self.fs_devices = auto.get_fs_devices()
            except subprocess.CalledProcessError as err:
                logging.error(err.output)
                self.queue_event('error', _("Error creating partitions and their filesystems"))
                return


        if self.method == 'alongside':
            # Alongside method shrinks selected partition
            # and creates root and swap partition in the available space
            boot_partition, root_partition = fs.shrink(self.mount_devices["alongside"])
            # Alongside method formats root by default (as it is always a new partition)
            (error, msg) = fs.create_fs(self.mount_devices["/"], "ext4")

        if self.method == 'advanced':
            root_partition = self.mount_devices["/"]

            # NOTE: Advanced method formats root by default in installation_advanced
            '''
            if root_partition in self.fs_devices:
                root_fs = self.fs_devices[root_partition]
            else:
                root_fs = "ext4"
            '''

            if "/boot" in self.mount_devices:
                boot_partition = self.mount_devices["/boot"]
            else:
                boot_partition = ""

            if "swap" in self.mount_devices:
                swap_partition = self.mount_devices["swap"]
            else:
                swap_partition = ""


        # Create the directory where we will mount our new root partition
        if not os.path.exists(self.dest_dir):
            os.mkdir(self.dest_dir)

        # Mount root and boot partitions (only if it's needed)
        # Not doing this in automatic mode as AutoPartition class mounts the root and boot devices itself.
        if self.method == 'alongside' or self.method == 'advanced':
            try:
                txt = _("Mounting partition %s into %s directory") % (root_partition, self.dest_dir)
                self.queue_event('debug', txt)
                subprocess.check_call(['mount', root_partition, self.dest_dir])
                # We also mount the boot partition if it's needed
                subprocess.check_call(['mkdir', '-p', '%s/boot' % self.dest_dir])
                if "/boot" in self.mount_devices:
                    txt = _("Mounting partition %s into %s/boot directory") % (boot_partition, self.dest_dir)
                    self.queue_event('debug', txt)
                    subprocess.check_call(['mount', boot_partition, "%s/boot" % self.dest_dir])
            except subprocess.CalledProcessError as err:
                logging.error(err)
                self.queue_fatal_event(_("Couldn't mount root and boot partitions"))
                return False

        # In advanced mode, mount all partitions (root and boot are already mounted)
        if self.method == 'advanced':
            for path in self.mount_devices:
                mount_part = self.mount_devices[path]
                if mount_part != root_partition and mount_part != boot_partition and mount_part != swap_partition:
                    try:
                        mount_dir = self.dest_dir + path
                        if not os.path.exists(mount_dir):
                            os.makedirs(mount_dir)
                        txt = _("Mounting partition %s into %s directory") % (mount_part, mount_dir)
                        self.queue_event('debug', txt)
                        subprocess.check_call(['mount', mount_part, mount_dir])
                    except subprocess.CalledProcessError as err:
                        # We will continue as root and boot are already mounted
                        logging.warning(err)
                        self.queue_event('debug', _("Can't mount %s in %s") % (mount_part, mount_dir))


        # Nasty workaround:
        # If pacman was stoped and /var is in another partition than root
        # (so as to be able to resume install), database lock file will still be in place.
        # We must delete it or this new installation will fail

        db_lock = os.path.join(self.dest_dir, "var/lib/pacman/db.lck")
        if os.path.exists(db_lock):
            with misc.raised_privileges():
                os.remove(db_lock)
            logging.debug(_("%s deleted"), db_lock)

        # Create some needed folders
        try:
            subprocess.check_call(['mkdir', '-p', '%s/var/lib/pacman' % self.dest_dir])
            subprocess.check_call(['mkdir', '-p', '%s/etc/pacman.d/gnupg/' % self.dest_dir])
            subprocess.check_call(['mkdir', '-p', '%s/var/log/' % self.dest_dir])
        except subprocess.CalledProcessError as err:
            logging.error(err)
            self.queue_fatal_event(_("Can't create necessary directories on destination system"))
            return False

        all_ok = True

        try:
            self.queue_event('debug', _('Selecting packages...'))
            self.select_packages()
            self.queue_event('debug', _('Packages selected'))

            if self.settings.get("use_aria2"):
                self.queue_event('debug', _('Downloading packages...'))
                self.download_packages()
                self.queue_event('debug', _('Packages downloaded.'))

            cache_dir = self.settings.get("cache")
            if len(cache_dir) > 0:
                self.copy_cache_files(cache_dir)

            self.queue_event('debug', _('Installing packages...'))
            self.install_packages()
            self.queue_event('debug', _('Packages installed.'))

            self.queue_event('debug', _('Configuring system...'))
            self.configure_system()
            self.queue_event('debug', _('System configured.'))
        except subprocess.CalledProcessError as err:
            logging.error(err)
            self.queue_fatal_event("CalledProcessError.output = %s" % e.output)
            all_ok = False
        except InstallError as err:
            logging.error(err)
            self.queue_fatal_event(err.value)
            all_ok = False
        except:
            # unknown error
            logging.error(_("Unknown error"))
            self.running = False
            self.error = True
            all_ok = False

        if all_ok is False:
            return False
        else:
            # Installation finished successfully
            self.queue_event(_("Installation finished"))
            self.running = False
            self.error = False
            return True

    def download_packages(self):
        """ Downloads necessary packages using Aria2 """
        conf_file = "/tmp/pacman.conf"
        cache_dir = "%s/var/cache/pacman/pkg" % self.dest_dir
        download.DownloadPackages(self.packages, conf_file, cache_dir, self.callback_queue)

    def create_pacman_conf(self):
        """ Creates temporary pacman.conf file """
        self.queue_event('debug', _("Creating a temporary pacman.conf for %s architecture") % self.arch)

        # Common repos

        # TODO: Instead of hardcoding pacman.conf, we could use an external file

        with open("/tmp/pacman.conf", "w") as tmp_file:
            tmp_file.write("[options]\n")
            tmp_file.write("Architecture = auto\n")
            tmp_file.write("SigLevel = PackageOptional\n")

            tmp_file.write("RootDir = %s\n" % self.dest_dir)
            tmp_file.write("DBPath = %s/var/lib/pacman/\n" % self.dest_dir)
            tmp_file.write("CacheDir = %s/var/cache/pacman/pkg\n" % self.dest_dir)
            tmp_file.write("LogFile = /tmp/pacman.log\n\n")

            # ¿?
            #tmp_file.write("CacheDir = /packages/core-%s/pkg\n" % self.arch)
            #tmp_file.write("CacheDir = /packages/core-any/pkg\n\n")

            tmp_file.write("# Repositories\n\n")

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
                tmp_file.write("Include = /etc/pacman.d/mirrorlist\n\n")

            tmp_file.write("[antergos]\n")
            tmp_file.write("SigLevel = PackageRequired\n")
            tmp_file.write("Include = /etc/pacman.d/antergos-mirrorlist\n\n")

        # Init pyalpm

        try:
            self.pac = pac.Pac("/tmp/pacman.conf", self.callback_queue)
        except Exception as err:
            logging.error(err)
            raise InstallError("Can't initialize pyalpm: %s" % err)

    def prepare_pacman_keychain(self):
        """ Add gnupg pacman files to installed system """
        dest_path = os.path.join(self.dest_dir, "etc/pacman.d/gnupg")
        try:
            misc.copytree('/etc/pacman.d/gnupg', dest_path)
        except (FileExistsError, shutil.Error) as err:
            # log error but continue anyway
            logging.exception(err)

    def prepare_pacman(self):
        """ Configures pacman and syncs db on destination system """
        dirs = [ "var/cache/pacman/pkg", "var/lib/pacman" ]

        for pacman_dir in dirs:
            mydir = os.path.join(self.dest_dir, pacman_dir)
            if not os.path.exists(mydir):
                os.makedirs(mydir)

        self.prepare_pacman_keychain()

        self.pac.do_refresh()

    def select_packages(self):
        """ Prepare pacman and get package list from Internet """
        self.create_pacman_conf()
        self.prepare_pacman()

        if len(self.alternate_package_list) > 0:
            packages_xml = self.alternate_package_list
        else:
            # The list of packages is retrieved from an online XML to let us
            # control the pkgname in case of any modification

            self.queue_event('info', _("Getting package list..."))

            try:
                url = 'http://install.antergos.com/packages-%s.xml' % info.CNCHI_VERSION[:3]
                packages_xml = urllib.request.urlopen(url, timeout=5)
            except urllib.error.URLError as err:
                # If the installer can't retrieve the remote file, try to install with a local
                # copy, that may not be updated
                logging.warning(err)
                self.queue_event('debug', _("Can't retrieve remote package list, using a local file instead."))
                data_dir = self.settings.get("data")
                packages_xml = os.path.join(data_dir, 'packages.xml')

        tree = etree.parse(packages_xml)
        root = tree.getroot()

        self.queue_event('debug', _("Adding all desktops common packages"))

        for child in root.iter('common_system'):
            for pkg in child.iter('pkgname'):
                self.packages.append(pkg.text)

        if self.desktop != "nox":
            for child in root.iter('graphic_system'):
                for pkg in child.iter('pkgname'):
                    # If package is Desktop Manager, save the name to activate the correct service later
                    if pkg.attrib.get('dm'):
                        self.desktop_manager = pkg.attrib.get('name')
                    self.packages.append(pkg.text)

            self.queue_event('debug', _("Adding '%s' desktop packages") % self.desktop)

            for child in root.iter(self.desktop + '_desktop'):
                for pkg in child.iter('pkgname'):
                    # If package is Desktop Manager, save name to
                    # activate the correct service
                    if pkg.attrib.get('dm'):
                        self.desktop_manager = pkg.attrib.get('name')
                    if pkg.attrib.get('nm'):
                        self.network_manager = pkg.attrib.get('name')
                    if pkg.attrib.get('conflicts'):
                        self.conflicts.append(pkg.attrib.get('conflicts'))
                    self.packages.append(pkg.text)
        else:
            # Add specific NoX/Base packages
            for child in root.iter('nox'):
                for pkg in child.iter('pkgname'):
                    if pkg.attrib.get('nm'):
                        self.network_manager = pkg.attrib.get('name')
                    if pkg.attrib.get('conflicts'):
                        self.conflicts.append(pkg.attrib.get('conflicts'))
                    self.packages.append(pkg.text)

        # Always install ntp as the user may want to activate it
        # later (or not) in the timezone screen
        for child in root.iter('ntp'):
            for pkg in child.iter('pkgname'):
                self.packages.append(pkg.text)

        # Install graphic cards drivers except in NoX installs
        if self.desktop != "nox":
            self.queue_event('debug', _("Getting graphics card drivers"))

            graphics = self.get_graphics_card()

            if "ati " in graphics:
                for child in root.iter('ati'):
                    for pkg in child.iter('pkgname'):
                        self.packages.append(pkg.text)
                self.card.append('ati')

            if "nvidia" in graphics:
                for child in root.iter('nvidia'):
                    for pkg in child.iter('pkgname'):
                        self.packages.append(pkg.text)
                self.card.append('nvidia')

            if "intel" in graphics or "lenovo" in graphics:
                for child in root.iter('intel'):
                    for pkg in child.iter('pkgname'):
                        self.packages.append(pkg.text)
                self.card.append('intel')

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

            # Add xorg-drivers group if cnchi can't figure it out
            # the graphic card driver.
            if graphics not in ('ati ', 'nvidia', 'intel', 'virtualbox' \
                                'vmware', 'via '):
                self.packages.append('xorg-drivers')

        # Add filesystem packages

        self.queue_event('debug', _("Adding filesystem packages"))

        fs_types = subprocess.check_output(\
            ["blkid", "-c", "/dev/null", "-o", "value", "-s", "TYPE"]).decode()

        for iii in self.fs_devices:
            fs_types += self.fs_devices[iii]

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

        # Check for user desired features and add them to our installation
        self.queue_event('debug', _("Check for user desired features and add them to our installation"))
        self.add_features_packages(root)
        self.queue_event('debug', _("All features needed packages have been added"))

        # Add chinese fonts
        lang_code = self.settings.get("language_code")
        if lang_code == "zh_TW" or lang_code == "zh_CN":
            self.queue_event('debug', _('Selecting chinese fonts.'))
            for child in root.iter('chinese'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        # Add bootloader packages if needed
        self.queue_event('debug', _("Adding bootloader packages if needed"))
        if self.settings.get('install_bootloader'):
            btype = self.settings.get('bootloader_type')
            if btype == "GRUB2":
                for child in root.iter('grub'):
                    for pkg in child.iter('pkgname'):
                        self.packages.append(pkg.text)
            elif btype == "UEFI_x86_64":
                for child in root.iter('grub-efi'):
                    if root.attrib.get('uefiarch') == "x86_64":
                        for pkg in child.iter('pkgname'):
                            self.packages.append(pkg.text)
            elif btype == "UEFI_i386":
                for child in root.iter('grub-efi'):
                    if root.attrib.get('uefiarch') == "i386":
                        for pkg in child.iter('pkgname'):
                            self.packages.append(pkg.text)

    def add_features_packages(self, root):
        """ Selects packages based on user selected features """
        self.features_by_desktop = {"nox": ["aur", "bluetooth", "cups", "fonts", "firewall"],
                            "gnome": ["aur", "bluetooth", "cups", "fonts", "gnome_extra", "office", "firewall",
                                      "third_party"],
                            "cinnamon": ["aur", "bluetooth", "cups", "fonts", "office", "firewall", "third_party"],
                            "mate": ["aur", "bluetooth", "cups", "fonts", "office", "firewall", "third_party"],
                            "xfce": ["aur", "bluetooth", "cups", "fonts", "office", "firewall", "third_party"],
                            "razor": ["aur", "bluetooth", "cups", "fonts", "office", "firewall", "third_party"],
                            "openbox": ["aur", "bluetooth", "cups", "fonts", "office", "visual", "firewall",
                                        "third_party"],
                            "kde": ["aur", "bluetooth", "cups", "fonts", "office", "firewall", "third_party"]}

        desktop = self.settings.get("desktop")
        features = self.features_by_desktop[desktop]

        # TODO: For now, removed razor from qt list as it pulls in all kdelibs, Will revisit this list.
        lib = {'gtk':["gnome", "cinnamon", "xfce", "openbox", "mate"], 'qt':["norazor", "kde"]}

        for feature in features:
            # Add necessary packages for user desired features to our install list
            if self.settings.get("feature_" + feature):
                self.queue_event('debug', 'Adding packages for "%s" feature.' % feature)
                for child in root.iter(feature):
                    for pkg in child.iter('pkgname'):
                        # If it's a specific gtk or qt package we have to check it
                        # against our chosen desktop.
                        plib = pkg.attrib.get('lib')
                        if plib is None or (plib is not None and desktop in lib[plib]):
                            logging.debug("Selecting package: %s for feature: %s", pkg.text, feature)
                            self.packages.append(pkg.text)
                        else:
                            logging.debug("Skipping %s package: %s for feature: %s", plib, pkg.text, feature)


        # Add libreoffice language package
        if self.settings.get('feature_office'):
            self.queue_event('debug', _('Add libreoffice language package'))
            pkg = ""
            lang_name = self.settings.get("language_name").lower()
            if lang_name == "english":
                # There're some English variants available but not all of them.
                lang_packs = [ 'en-GB', 'en-US', 'en-ZA' ]
                locale = self.settings.get('locale').split('.')[0]
                locale = locale.replace('_', '-')
                if locale in lang_packs:
                    pkg = "libreoffice-%s" % locale
                else:
                    # Install American English if there is not an specific
                    # language package available.
                    pkg = "libreoffice-en-US"
            else:
                # All the other language packs use their language code
                lang_code = self.settings.get('language_code')
                lang_code = lang_code.replace('_', '-')
                pkg = "libreoffice-%s" % lang_code
            self.packages.append(pkg)

    def get_graphics_card(self):
        """ Get graphics card using hwinfo """
        process1 = subprocess.Popen(["hwinfo", "--gfxcard"], stdout=subprocess.PIPE)
        process2 = subprocess.Popen(["grep", "Model:[[:space:]]"], \
                              stdin=process1.stdout, stdout=subprocess.PIPE)
        process1.stdout.close()
        out, err = process2.communicate()
        return out.decode().lower()

    def install_packages(self):
        """ Start pacman installation of packages """
        self.chroot_mount_special_dirs()

        result = self.pac.do_install(self.packages, self.conflicts)
        if result == 1:
            self.chroot_umount_special_dirs()
            self.queue_fatal_event(_("Can't download and install necessary packages."))
            return False

        self.chroot_umount_special_dirs()

    def chroot_mount_special_dirs(self):
        """ Mount special directories for our chroot """
        # Don't try to remount them
        if self.special_dirs_mounted:
            self.queue_event('debug', _("Special dirs already mounted."))
            return

        special_dirs = [ "sys", "proc", "dev" ]
        for s_dir in special_dirs:
            mydir = os.path.join(self.dest_dir, s_dir)
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

        self.special_dirs_mounted = True

    def chroot_umount_special_dirs(self):
        """ Umount special directories for our chroot """
        # Do not umount if they're not mounted
        if not self.special_dirs_mounted:
            self.queue_event('debug', _("Special dirs already not mounted."))
            return

        special_dirs = [ "proc", "sys", "dev" ]

        for s_dir in special_dirs:
            mydir = os.path.join(self.dest_dir, s_dir)
            try:
                subprocess.check_call(["umount", "-l", mydir])
            except:
                self.queue_event('warning', _("Unable to umount %s") % mydir)

        self.special_dirs_mounted = False

    def chroot(self, cmd, stdin=None, stdout=None):
        """ Runs command inside the chroot """
        run = [ 'chroot', self.dest_dir ]

        for element in cmd:
            run.append(element)

        try:
            proc = subprocess.Popen(run,
                                    stdin=stdin,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate()[0]
            logging.debug(out.decode())
        except OSError as err:
            logging.exception(_("Error running command: %s"), err.strerror)
            raise

    def is_running(self):
        """ Checks if thread is running """
        return self.running

    def is_ok(self):
        """ Checks if an error has been issued """
        return not self.error

    def copy_network_config(self):
        """ Copies Network Manager configuration """
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

    def auto_fstab(self):
        """ Create /etc/fstab file """

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
            part_info = fs.get_info(parti)
            uuid = part_info['UUID']
            if parti in self.fs_devices:
                myfmt = self.fs_devices[parti]
            else:
                # It hasn't any filesystem defined
                continue

            # Take care of swap partitions
            if "swap" in myfmt:
                all_lines.append("UUID=%s %s %s %s 0 %s" % (uuid, path, myfmt, opts, chk))
                logging.debug(_("Added to fstab : UUID=%s %s %s %s 0 %s"), uuid, path, myfmt, opts, chk)
                continue

            # Avoid adding a partition to fstab when
            # it has no mount point (swap has been checked before)
            if path == "":
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
        full_text += '\n'

        with open('%s/etc/fstab' % self.dest_dir, 'w') as fstab_file:
            fstab_file.write(full_text)

    def install_bootloader(self):
        """ Installs bootloader """
        bootloader = self.settings.get('bootloader_type')

        if bootloader == "GRUB2":
            self.install_bootloader_grub2_bios()
        elif bootloader == "UEFI_x86_64" or bootloader == "UEFI_i386":
            self.install_bootloader_grub2_efi(bootloader)

    def modify_grub_default(self):
        """ If using LUKS, we need to modify GRUB_CMDLINE_LINUX to load our root encrypted partition
            This scheme can be used in the automatic installation option only (at this time) """

        if self.method == 'automatic' and self.settings.get('use_luks'):
            default_dir = os.path.join(self.dest_dir, "etc/default")

            if not os.path.exists(default_dir):
                os.mkdir(default_dir)

            root_device = self.mount_devices["/"]
            boot_device = self.mount_devices["/boot"]

            # Let GRUB automatically add the kernel parameters for root encryption
            if self.settings.get("luks_key_pass") == "":
                default_line = 'GRUB_CMDLINE_LINUX="cryptdevice=%s:cryptAntergos cryptkey=%s:ext2:/.keyfile-root"' % (root_device, boot_device)
            else:
                default_line = 'GRUB_CMDLINE_LINUX="cryptdevice=%s:cryptAntergos"' % root_device

            # Disable the usage of UUIDs for the rootfs:
            disable_uuid_line = 'GRUB_DISABLE_LINUX_UUID=true'

            default_grub = os.path.join(default_dir, "grub")

            with open(default_grub, "r") as grub_file:
                lines = [x.strip() for x in grub_file.readlines()]

            for i in range(len(lines)):
                if lines[i].startswith("#GRUB_CMDLINE_LINUX") or lines[i].startswith("GRUB_CMDLINE_LINUX"):
                    lines[i] = default_line
                elif lines[i].startswith("#GRUB_DISABLE_LINUX_UUID") or lines[i].startswith("GRUB_DISABLE_LINUX_UUID"):
                    lines[i] = disable_uuid_line

            with open(default_grub, "w") as grub_file:
                grub_file.write("\n".join(lines) + "\n")

    def install_bootloader_grub2_bios(self):
        """ Install bootloader in a BIOS system """
        grub_device = self.settings.get('bootloader_device')
        self.queue_event('info', _("Installing GRUB(2) BIOS boot loader in %s") % grub_device)

        self.modify_grub_default()

        grub_d_dir = os.path.join(self.dest_dir, "etc/grub.d")

        if not os.path.exists(grub_d_dir):
            os.makedirs(grub_d_dir)

        try:
            shutil.copy2("/arch/10_linux", grub_d_dir)
        except FileNotFoundError:
            try:
                shutil.copy2("/etc/grub.d/10_linux", grub_d_dir)
            except FileNotFoundError:
                self.queue_event('warning', _("Can't find neither '/arch/10_linux' nor '/etc/grub.d/10_linux'"))
            except FileExistsError:
                pass
        except FileExistsError:
            pass

        self.install_bootloader_grub2_locales()

        locale = self.settings.get("locale")
        self.chroot_mount_special_dirs()
        #self.chroot(['sh', '-c', 'LANG=%s grub-mkconfig -o /boot/grub/grub.cfg' % locale])
        self.chroot(['sh', '-c', 'LANG=%s grub-mkconfig > /boot/grub/grub.cfg' % locale])

        self.chroot(['grub-install', \
                  '--directory=/usr/lib/grub/i386-pc', \
                  '--target=i386-pc', \
                  '--boot-directory=/boot', \
                  '--recheck', \
                  grub_device])

        self.chroot_umount_special_dirs()

        core_path = os.path.join(self.dest_dir, "boot/grub/i386-pc/core.img")
        if os.path.exists(core_path):
            self.queue_event('info', _("GRUB(2) BIOS has been successfully installed."))
        else:
            self.queue_event('warning', _("ERROR installing GRUB(2) BIOS."))

    def install_bootloader_grub2_efi(self, arch):
        """ Install bootloader in a UEFI system """
        uefi_arch = "x86_64"
        spec_uefi_arch = "x64"

        if arch == "UEFI_i386":
            uefi_arch = "i386"
            spec_uefi_arch = "ia32"

        grub_device = self.settings.get('bootloader_device')
        self.queue_event('info', _("Installing GRUB(2) UEFI %s boot loader in %s") % (uefi_arch, grub_device))

        self.modify_grub_default()

        self.chroot_mount_special_dirs()

        subprocess.check_call(['grub-install --target=%s-efi --efi-directory=/install/boot/efi --bootloader-id=antergos_grub '
            '--boot-directory=/install/boot --recheck' % uefi_arch], shell=True)

        self.chroot_umount_special_dirs()

        self.install_bootloader_grub2_locales()

        locale = self.settings.get("locale")
        self.chroot_mount_special_dirs()
        self.chroot(['sh', '-c', 'LANG=%s grub-mkconfig -o /boot/grub/grub.cfg' % locale])
        self.chroot_umount_special_dirs()

        #grub_cfg = "%s/boot/grub/grub.cfg" % self.dest_dir
        #grub_standalone = "%s/boot/efi/EFI/arch_grub/grub%s_standalone.cfg" % (self.dest_dir, spec_uefi_arch)
        #try:
        #    shutil.copy2(grub_cfg, grub_standalone)
        #except FileNotFoundError:
        #    self.queue_event('warning', _("ERROR installing GRUB(2) configuration file."))
        #except FileExistsError:
        #    pass
        #
        #self.chroot_mount_special_dirs()
        #self.chroot(['grub-mkstandalone', \
        #          '--directory=/usr/lib/grub/%s-efi' % uefi_arch, \
        #          '--format=%s-efi' % uefi_arch, \
        #          '--compression="xz"', \
        #          '--output="/boot/efi/EFI/arch_grub/grub%s_standalone.efi' % spec_uefi_arch, \
        #          'boot/grub/grub.cfg'])
        #self.chroot_umount_special_dirs()

    def install_bootloader_grub2_locales(self):
        """ Install Grub2 locales """
        dest_locale_dir = os.path.join(self.dest_dir, "boot/grub/locale")

        if not os.path.exists(dest_locale_dir):
            os.makedirs(dest_locale_dir)

        grub_mo = os.path.join(self.dest_dir, "usr/share/locale/en@quot/LC_MESSAGES/grub.mo")

        try:
            shutil.copy2(grub_mo, os.path.join(dest_locale_dir, "en.mo"))
        except FileNotFoundError:
            self.queue_event('warning', _("Can't install GRUB(2) locale."))
        except FileExistsError:
            # Ignore if already exists
            pass

    def enable_services(self, services):
        """ Enables all services that are in the list 'services' """
        for name in services:
            self.chroot(['systemctl', 'enable', name + ".service"])
            self.queue_event('debug', _('Enabled %s service.') % name)

    def change_user_password(self, user, new_password):
        """ Changes the user's password """
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
        """ Set hardware clock """
        subprocess.check_call(["hwclock", "--systohc", "--utc"])
        shutil.copy2("/etc/adjtime", "%s/etc/" % self.dest_dir)

    def set_mkinitcpio_hooks_and_modules(self, hooks, modules):
        """ Set up mkinitcpio.conf """
        self.queue_event('debug', _('Setting hooks and modules in mkinitcpio.conf'))
        self.queue_event('debug', 'HOOKS="%s"' % ' '.join(hooks))
        self.queue_event('debug', 'MODULES="%s"' % ' '.join(modules))

        with open("/etc/mkinitcpio.conf") as mkinitcpio_file:
            mklins = [x.strip() for x in mkinitcpio_file.readlines()]

        for i in range(len(mklins)):
            if mklins[i].startswith("HOOKS"):
                mklins[i] = 'HOOKS="%s"' % ' '.join(hooks)
            elif mklins[i].startswith("MODULES"):
                mklins[i] = 'MODULES="%s"' % ' '.join(modules)

        path = os.path.join(self.dest_dir, "etc/mkinitcpio.conf")
        with open(path, "w") as mkinitcpio_file:
            mkinitcpio_file.write("\n".join(mklins) + "\n")

    def run_mkinitcpio(self):
        """ Runs mkinitcpio """
        # Add lvm and encrypt hooks if necessary

        hooks = [ "base", "udev", "autodetect", "modconf", "block" ]
        modules = []

        # It is important that the encrypt hook comes before the filesystems hook
        # (in case you are using LVM on LUKS, the order should be: encrypt lvm2 filesystems)

        if self.settings.get("use_luks"):
            hooks.append("encrypt")
            modules.extend([ "dm_mod", "dm_crypt", "ext4", "aes-x86_64", "sha256", "sha512" ])

        if self.blvm or self.settings.get("use_lvm"):
            hooks.append("lvm2")

        hooks.extend([ "filesystems", "keyboard", "fsck" ])

        self.set_mkinitcpio_hooks_and_modules(hooks, modules)

        # run mkinitcpio on the target system
        self.chroot_mount_special_dirs()
        self.chroot(["/usr/bin/mkinitcpio", "-p", self.kernel_pkg])
        self.chroot_umount_special_dirs()

    def uncomment_locale_gen(self, locale):
        """ Uncomment selected locale in /etc/locale.gen """
        #self.chroot(['sed', '-i', '-r', '"s/#(.*%s)/\1/g"' % locale, "/etc/locale.gen"])

        text = []
        with open("%s/etc/locale.gen" % self.dest_dir, "r") as gen:
            text = gen.readlines()

        with open("%s/etc/locale.gen" % self.dest_dir, "w") as gen:
            for line in text:
                if locale in line and line[0] == "#":
                    # uncomment line
                    line = line[1:]
                gen.write(line)

    def check_output(self, command):
        """ Helper function to run a command """
        return subprocess.check_output(command.split()).decode().strip("\n")

    def copy_cache_files(self, cache_dir):
        """ Copy all packages fro specified directory to install's target """
        # Check in case user has given a wrong folder
        if not os.path.exists(cache_dir):
            return
        self.queue_event('info', _('Copying xz files from cache...'))
        dest_dir = os.path.join(self.dest_dir, "var/cache/pacman/pkg")
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        self.copy_cache_files_progress(cache_dir, dest_dir)

    def copy_cache_files_progress(self, src, dst):
        """ Copy files updating the slides' progress bar """
        percent = 0.0
        items = os.listdir(src)

        step = 1.0 / len(items)
        for item in items:
            self.queue_event("percent", percent)
            source = os.path.join(src, item)
            destination = os.path.join(dst, item)
            try:
                shutil.copy2(source, destination)
            except (FileExistsError, shutil.Error) as err:
                logging.warning(err)
            percent += step

    def setup_features(self):
        """ Do all set up needed by the user's selected features """
        #features = [ "aur", "bluetooth", "cups", "office", "visual", "firewall", "third_party" ]

        #if self.settings.get("feature_aur"):
        #    self.queue_event('debug', _("Configuring AUR..."))

        if self.settings.get("feature_bluetooth"):
            self.queue_event('debug', _("Configuring bluetooth..."))
            service = os.path.join(self.dest_dir, "usr/lib/systemd/system/bluetooth.service")
            if os.path.exists(service):
                self.enable_services(['bluetooth'])

        if self.settings.get("feature_cups"):
            self.queue_event('debug', _("Configuring CUPS..."))
            service = os.path.join(self.dest_dir, "usr/lib/systemd/system/cups.service")
            if os.path.exists(service):
                self.enable_services(['cups'])

        #if self.settings.get("feature_office"):
        #    self.queue_event('debug', _("Configuring libreoffice..."))

        #if self.settings.get("feature_visual"):
        #    self.queue_event('debug', _("Configuring Compositing manager..."))

        if self.settings.get("feature_firewall"):
            self.queue_event('debug', _("Configuring firewall..."))
            self.chroot_mount_special_dirs()
            self.chroot(["ufw", "default", "deny"])
            toallow = misc.get_network()
            if toallow:
                self.chroot(["ufw", "allow", "from", toallow])
            self.chroot(["ufw", "allow", "Transmission"])
            self.chroot(["ufw", "allow", "SSH"])
            self.chroot(["ufw", "enable"])
            self.chroot_umount_special_dirs()
            service = os.path.join(self.dest_dir, "usr/lib/systemd/system/ufw.service")
            if os.path.exists(service):
                self.enable_services(['ufw'])

    def set_display_manager(self):
        """ Configures the installed desktop manager, including autologin. """
        self.queue_event('info', _("%s: Configuring display manager.") % self.desktop_manager)
        desktop = self.settings.get('desktop')
        username = self.settings.get('username')
        
        sessions = { 'gnome':'gnome', 'cinnamon':'cinnamon', 'razor':'razor-session', 'openbox':'openbox-session',
            'xfce':'startxfce4', 'kde':'kde-plasma', 'mate':'mate' }

        if self.desktop_manager == 'lightdm':
            # Systems with LightDM as Desktop Manager
            lightdm_conf_path = os.path.join(self.dest_dir, "etc/lightdm/lightdm.conf")
            text = []
            with open(lightdm_conf_path, "r") as lightdm_conf:
                text = lightdm_conf.readlines()
            with open(lightdm_conf_path, "w") as lightdm_conf:
                for line in text:
                    if self.settings.get('require_password') is False:
                        # Enable automatic login
                        if '#autologin-user=' in line:
                            line = 'autologin-user=%s\n' % username
                        if '#autologin-user-timeout=0' in line:
                            line = 'autologin-user-timeout=0\n'
                    # Set correct DE session
                    if '#user-session=default' in line:
                        line = 'user-session=%s\n' % sessions[desktop]
                    lightdm_conf.write(line)

        if self.desktop_manager == 'gdm':
            # Systems with GDM as Desktop Manager
            gdm_conf_path = os.path.join(self.dest_dir, "etc/gdm/custom.conf")
            with open(gdm_conf_path, "w") as gdm_conf:
                gdm_conf.write('# Cnchi - Enable automatic login for user\n')
                gdm_conf.write('[daemon]\n')
                gdm_conf.write('AutomaticLogin=%s\n' % username)
                gdm_conf.write('AutomaticLoginEnable=True\n')
        
        if self.desktop_manager == 'kdm':
            # Systems with KDM as Desktop Manager
            kdm_conf_path = os.path.join(self.dest_dir, "usr/share/config/kdm/kdmrc")
            text = []
            with open(kdm_conf_path, "r") as kdm_conf:
                text = kdm_conf.readlines()
            with open(kdm_conf_path, "w") as kdm_conf:
                for line in text:
                    if '#AutoLoginEnable=true' in line:
                        line = 'AutoLoginEnable=true\n'
                    if 'AutoLoginUser=' in line:
                        line = 'AutoLoginUser=%s\n' % username
                    kdm_conf.write(line)
        
        if self.desktop_manager == 'lxdm':
            # Systems with LXDM as Desktop Manager
            lxdm_conf_path = os.path.join(self.dest_dir, "etc/lxdm/lxdm.conf")
            text = []
            with open(lxdm_conf_path, "r") as lxdm_conf:
                text = lxdm_conf.readlines()
            with open(lxdm_conf_path, "w") as lxdm_conf:
                for line in text:
                    if '# autologin=dgod' in line:
                        line = 'autologin=%s\n' % username
                    lxdm_conf.write(line)
        
        if self.desktop_manager == 'slim':
            # Systems with Slim as Desktop Manager
            slim_conf_path = os.path.join(self.dest_dir, "etc/slim.conf")
            text = []
            with open(slim_conf_path, "r") as slim_conf:
                text = slim_conf.readlines()
            with open(slim_conf_path, "w") as slim_conf:
                for line in text:
                    if 'auto_login' in line:
                        line = 'auto_login yes\n'
                    if 'default_user' in line:
                        line = 'default_user %s\n' % username
                    slim_conf.write(line)

    def configure_system(self):
        """ Final install steps
            Set clock, language, timezone
            Run mkinitcpio
            Populate pacman keyring
            Setup systemd services
            ... and more """
        
        # All downloading and installing has been done, so we hide progress bars
        # (they are 100% both so it makes no sense to still show them)
        self.queue_event('progress', 'hide_all')

        self.queue_event('action', _("Configuring your new system"))

        self.auto_fstab()
        self.queue_event('debug', _('fstab file generated.'))

        # Copy configured networks in Live medium to target system
        if self.network_manager == 'NetworkManager':
            self.copy_network_config()

        # TODO: Test copy profile. Code below is not finished.
        '''
        elif self.network_manager == 'netctl':
            if misc.is_wireless_enabled():
                profile = 'wireless-wpa'
            else:
                profile = 'ethernet-dhcp'

            self.queue_event('debug', _('Cnchi will configure netctl using the %s profile') % profile)

            src_path = os.path.join(self.dest_dir, 'etc/netctl/examples/%s' % profile)
            dst_path = os.path.join(self.dest_dir, 'etc/netctl/%s' % profile)
            shutil.copy(src_path, dst_path)
            self.chroot(['netctl', 'enable', profile])
        '''
        self.queue_event('debug', _('Network configuration copied.'))

        # Copy mirror list
        mirrorlist_path = os.path.join(self.dest_dir, 'etc/pacman.d/mirrorlist')
        try:
            shutil.copy2('/etc/pacman.d/mirrorlist', mirrorlist_path)
            self.queue_event('debug', _('Mirror list copied.'))
        except FileNotFoundError:
            logging.warning(_("Can't copy mirrorlist file"))
        except FileExistsError:
            pass

        # Copy important /etc config files to target system
        files = [ "/etc/pacman.conf", "/etc/yaourtrc" ]

        for path in files:
            try:
                shutil.copy2(path, os.path.join(self.dest_dir, 'etc/'))
            except FileNotFoundError:
                logging.error(_("Can't copy %s file, file not found.") % path)
            except FileExistsError:
                logging.error(_("Can't copy %s file, file already exists.") % path)

        self.queue_event('debug', _('Important configuration files copied.'))

        desktop = self.settings.get('desktop')

        # Enable services
        if desktop != "nox":
            self.enable_services([ self.desktop_manager, "ModemManager" ])

        self.enable_services([ self.network_manager ])

        # Wait FOREVER until the user sets the timezone
        while self.settings.get('timezone_done') is False:
            # wait five seconds and try again
            time.sleep(5)

        if self.settings.get("use_ntp"):
            self.enable_services(["ntpd"])

        # Set timezone
        zoneinfo_path = os.path.join("/usr/share/zoneinfo", self.settings.get("timezone_zone"))
        self.chroot(['ln', '-s', zoneinfo_path, "/etc/localtime"])

        self.queue_event('debug', _('Timezone set.'))

        # Wait FOREVER until the user sets his params
        while self.settings.get('user_info_done') is False:
            # wait five seconds and try again
            time.sleep(5)

        # Set user parameters
        username = self.settings.get('username')
        fullname = self.settings.get('fullname')
        password = self.settings.get('password')
        hostname = self.settings.get('hostname')

        sudoers_path = os.path.join(self.dest_dir, "etc/sudoers.d/10-installer")

        with open(sudoers_path, "w") as sudoers:
            sudoers.write('%s ALL=(ALL) ALL\n' % username)

        subprocess.check_call(["chmod", "440", sudoers_path])

        self.queue_event('debug', _('Sudo configuration for user %s done.') % username)
        
        default_groups = 'lp,video,network,storage,wheel,audio'
        
        if self.settings.get('require_password') is False:
            default_groups += ',autologin'
        
        self.chroot(['useradd', '-m', '-s', '/bin/bash', '-g', 'users', '-G', default_groups, username])

        self.queue_event('debug', _('User %s added.') % username)

        self.change_user_password(username, password)

        self.chroot(['chfn', '-f', fullname, username])

        self.chroot(['chown', '-R', '%s:users' % username, "/home/%s" % username])

        hostname_path = os.path.join(self.dest_dir, "etc/hostname")
        if not os.path.exists(hostname_path):
            with open(hostname_path, "w") as hostname_file:
                hostname_file.write(hostname)

        self.queue_event('debug', _('Hostname set to %s.') % hostname)

        # User password is the root password
        self.change_user_password('root', password)
        self.queue_event('debug', _('Set the same password to root.'))

        # Generate locales
        keyboard_layout = self.settings.get("keyboard_layout")
        keyboard_variant = self.settings.get("keyboard_variant")
        locale = self.settings.get("locale")
        self.queue_event('info', _("Generating locales..."))

        self.uncomment_locale_gen(locale)

        self.chroot(['locale-gen'])
        locale_conf_path = os.path.join(self.dest_dir, "etc/locale.conf")
        with open(locale_conf_path, "w") as locale_conf:
            locale_conf.write('LANG=%s\n' % locale)
            #locale_conf.write('LC_COLLATE=C\n')
            locale_conf.write('LC_COLLATE=%s\n' % locale)

        # Set /etc/vconsole.conf
        vconsole_conf_path = os.path.join(self.dest_dir, "etc/vconsole.conf")
        with open(vconsole_conf_path, "w") as vconsole_conf:
            vconsole_conf.write('KEYMAP=%s\n' % keyboard_layout)

        self.queue_event('info', _("Adjusting hardware clock..."))
        self.auto_timesetting()

        if desktop != "nox":
            # Set /etc/X11/xorg.conf.d/00-keyboard.conf for the xkblayout
            self.queue_event('debug', _("Set /etc/X11/xorg.conf.d/00-keyboard.conf for the xkblayout"))
            xorg_conf_xkb_path = os.path.join(self.dest_dir, "etc/X11/xorg.conf.d/00-keyboard.conf")
            with open(xorg_conf_xkb_path, "w") as xorg_conf_xkb:
                xorg_conf_xkb.write("# Read and parsed by systemd-localed. It's probably wise not to edit this file\n")
                xorg_conf_xkb.write('# manually too freely.\n')
                xorg_conf_xkb.write('Section "InputClass"\n')
                xorg_conf_xkb.write('        Identifier "system-keyboard"\n')
                xorg_conf_xkb.write('        MatchIsKeyboard "on"\n')
                xorg_conf_xkb.write('        Option "XkbLayout" "%s"\n' % keyboard_layout)
                if keyboard_variant != '':
                    xorg_conf_xkb.write('        Option "XkbVariant" "%s"\n' % keyboard_variant)
                xorg_conf_xkb.write('EndSection\n')
            self.queue_event('debug', _("00-keyboard.conf written."))

        # Let's start without using hwdetect for mkinitcpio.conf.
        # I think it should work out of the box most of the time.
        # This way we don't have to fix deprecated hooks.
        # NOTE: With LUKS or LVM maybe we'll have to fix deprecated hooks.
        self.queue_event('info', _("Running mkinitcpio..."))
        self.run_mkinitcpio()

        self.queue_event('debug', _("Call Cnchi post-install script"))
        # Call post-install script to execute (g,k)settings commands or install openbox defaults
        script_path_postinstall = os.path.join(self.settings.get('cnchi'), "scripts", POSTINSTALL_SCRIPT)
        subprocess.check_call(["/usr/bin/bash", script_path_postinstall, \
            username, self.dest_dir, self.desktop, keyboard_layout, keyboard_variant])

        # Set lightdm config including autologin if selected
        # Warning: In openbox "desktop", the post-install script writes /etc/slim.conf
        # so we always have to call set_display_manger AFTER the post-install script call.
        self.set_display_manager()

        # Configure user features (third party software, libreoffice language pack, ...)
        self.setup_features()

        # Encrypt user's home directory if requested (NOT FINISHED YET)
        if self.settings.get('encrypt_home'):
            self.queue_event('debug', _("Encrypting user home dir..."))
            encfs.setup(username, self.dest_dir)
            self.queue_event('debug', _("User home dir encrypted"))

        # Install boot loader (always after running mkinitcpio)
        if self.settings.get('install_bootloader'):
            self.queue_event('debug', _('Installing bootloader...'))
            self.install_bootloader()

        # Copy Cnchi log to new installation
        datetime = time.strftime("%Y%m%d") + "-" + time.strftime("%H%M%S")
        dst = os.path.join(self.dest_dir, "var/log/cnchi-%s.log" % datetime)
        try:
            shutil.copy("/tmp/cnchi.log", dst)
        except FileNotFoundError:
            logging.warning(_("Can't copy Cnchi log to %s") % dst)
        except FileExistsError:
            pass
