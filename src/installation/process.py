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
from mako.template import Template
from mako.lookup import TemplateLookup

from installation import auto_partition
import desktop_environments as desktops
import parted3.fs_module as fs
import canonical.misc as misc
import pacman.pac as pac

try:
    import pyalpm
except ImportError:
    pass
    
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
    def __init__(self, settings, callback_queue, mount_devices,
                 fs_devices, ssd=None, alternate_package_list="", blvm=False):
        """ Initialize installation class """
        multiprocessing.Process.__init__(self)

        self.alternate_package_list = alternate_package_list

        self.callback_queue = callback_queue
        self.settings = settings

        # Save how we have been called
        # We need this in case we have to retry the installation
        parameters = {'mount_devices': mount_devices,
                      'fs_devices': fs_devices,
                      'ssd': ssd,
                      'alternate_package_list': alternate_package_list,
                      'blvm': blvm}
        self.settings.set('installer_thread_call', parameters)

        # This flag tells us if there is a lvm partition (from advanced install)
        # If it's true we'll have to add the 'lvm2' hook to mkinitcpio
        self.blvm = blvm

        self.method = self.settings.get('partition_mode')

        self.queue_event('info', _("Installing using the '%s' method. Please wait...") % self.method)

        self.ssd = ssd
        self.mount_devices = mount_devices

        # Check desktop selected to load packages needed
        self.desktop = self.settings.get('desktop')

        # Set defaults
        self.desktop_manager = 'lightdm'
        self.network_manager = 'NetworkManager'

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
        self.dest_dir = ""
        self.bootloader_ok = self.settings.get('bootloader_ok')
        self.vbox = False
        self.num_packages = {}

    def queue_fatal_event(self, txt):
        """ Queues the fatal event and exits process """
        self.error = True
        self.running = False
        self.queue_event('error', txt)
        self.callback_queue.join()
        # Is this really necessary?
        os._exit(0)

    def queue_event(self, event_type, event_text=""):
        try:
            self.callback_queue.put_nowait((event_type, event_text))
        except queue.Full:
            pass

    def wait_for_empty_queue(self, timeout):
        tries = 0
        if timeout < 1:
            timeout = 1
        while tries < timeout and not self.callback_queue.empty():
            time.sleep(1)
            tries += 1

    @misc.raise_privileges
    def run(self):
        """ Run installation """
        # Common vars
        self.packages = []

        self.dest_dir = "/install"

        if not os.path.exists(self.dest_dir):
            try:
                with misc.raised_privileges():
                    os.makedirs(self.dest_dir)
            except os.Error as err:
                # Already exists or can't create it
                logging.warning(err.strerror)
                if not os.path.exists(self.dest_dir):
                    txt = _("Can't create %s directory, Cnchi can't continue") % self.dest_dir
                    logging.error(txt)
                    raise InstallError(txt)
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

            logging.debug(_("Creating partitions and their filesystems in %s"), self.auto_device)

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
                txt = _("Error creating partitions and their filesystems")
                logging.error(txt)
                cmd = _("Command %s has failed.") % err.cmd
                logging.error(cmd)
                out = _("Output : %s") % err.output 
                logging.error(out)
                self.queue_fatal_event(txt)
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

            #if root_partition in self.fs_devices:
            #    root_fs = self.fs_devices[root_partition]
            #else:
            #    root_fs = "ext4"

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
                logging.debug(txt)
                subprocess.check_call(['mount', root_partition, self.dest_dir])
                # We also mount the boot partition if it's needed
                subprocess.check_call(['mkdir', '-p', '%s/boot' % self.dest_dir])
                if "/boot" in self.mount_devices:
                    txt = _("Mounting partition %s into %s/boot directory") % (boot_partition, self.dest_dir)
                    logging.debug(txt)
                    subprocess.check_call(['mount', boot_partition, "%s/boot" % self.dest_dir])
            except subprocess.CalledProcessError as err:
                txt = _("Couldn't mount root and boot partitions")
                logging.error(txt)
                cmd = _("Command %s has failed") % err.cmd
                logging.error(cmd)
                out = _("Output : %s") % err.output 
                logging.error(out)
                self.queue_fatal_event(txt)
                return False

        # In advanced mode, mount all partitions (root and boot are already mounted)
        if self.method == 'advanced':
            for path in self.mount_devices:
                # Ignore devices without a mount path (or they will be mounted at "self.dest_dir")
                if path == "":
                    continue
                mount_part = self.mount_devices[path]
                if mount_part != root_partition and mount_part != boot_partition and mount_part != swap_partition:
                    try:
                        mount_dir = self.dest_dir + path
                        if not os.path.exists(mount_dir):
                            os.makedirs(mount_dir)
                        txt = _("Mounting partition %s into %s directory") % (mount_part, mount_dir)
                        logging.debug(txt)
                        subprocess.check_call(['mount', mount_part, mount_dir])
                    except subprocess.CalledProcessError as err:
                        # We will continue as root and boot are already mounted
                        txt = _("Can't mount %s in %s") % (mount_part, mount_dir)
                        logging.warning(txt)
                        cmd = _("Command %s has failed.") % err.cmd
                        logging.warning(cmd)
                        out = _("Output : %s") % err.output 
                        logging.warning(out)

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
            txt = _("Can't create necessary directories on destination system")
            logging.error(txt)
            cmd = _("Command %s has failed") % err.cmd
            logging.error(cmd)
            out = _("Output : %s") % err.output 
            logging.error(out)
            self.queue_fatal_event(txt)
            return False

        # If kernel images exists in /boot they are most likely from a failed install attempt and need
        # to be removed otherwise pyalpm will raise a fatal exception later on.
        kernel_imgs = ("/install/boot/vmlinuz-linux", "/install/boot/initramfs-linux.img",
                       "/install/boot/initramfs-linux-fallback.img")
        for img in kernel_imgs:
            if os.path.exists(img):
                os.remove(img)

        all_ok = False

        try:
            logging.debug(_("Selecting packages..."))
            self.select_packages()
            logging.debug(_("Packages selected"))

            if self.settings.get("use_aria2"):
                logging.debug(_("Downloading packages using aria2..."))
                self.download_packages()
                logging.debug(_("Packages downloaded."))

            if self.settings.get('copy_cache'):
                self.copy_cache_files(self.settings.get('cache'))
            else:
                # Wait for all logs (logging and showing message to user is slower than just logging)
                # if we don't wait, logs get mixed up (when copying cache files waiting more makes no sense
                # as it is already a slow process)
                self.wait_for_empty_queue(timeout=10)

            logging.debug(_("Installing packages..."))
            self.install_packages()
            logging.debug(_("Packages installed."))

            logging.debug(_("Configuring system..."))
            self.configure_system()
            logging.debug(_("System configured."))
            
            all_ok = True
        except subprocess.CalledProcessError as err:
            cmd = _("Command %s has failed.") % err.cmd
            logging.error(cmd)
            out = _("Output : %s") % err.output 
            logging.error(out)
            self.queue_fatal_event(cmd)
        except InstallError as err:
            logging.error(err.value)
            self.queue_fatal_event(err.value)
        except pyalpm.error as err:
            logging.error(err)
            self.queue_fatal_event(err)
        except KeyboardInterrupt as err:
            logging.error(err)
            self.queue_fatal_event(err)
        except TypeError as err:
            logging.exception('TypeError: %s. Unable to continue.' % err)
            self.queue_fatal_event(err)
        except AttributeError as err:
            logging.exception('AttributeError: %s. Unable to continue.' % err)
        except Exception as err:
            # TODO: This is too broad and we may catch non-fatal errors and treat them as fatal
            logging.exception('Error: %s. Unable to continue.' % err)
            self.queue_fatal_event(err)

        self.running = False

        if all_ok is False:
            self.error = True
            return False
        else:
            # Installation finished successfully
            self.queue_event('finished', _("Installation finished"))
            self.error = False
            return True

    def copy_log(self):
        # Copy Cnchi log to new installation
        datetime = time.strftime("%Y%m%d") + "-" + time.strftime("%H%M%S")
        dst = os.path.join(self.dest_dir, "var/log/cnchi-%s.log" % datetime)
        try:
            shutil.copy("/tmp/cnchi.log", dst)
        except FileNotFoundError:
            logging.warning(_("Can't copy Cnchi log to %s"), dst)
        except FileExistsError:
            pass

    def download_packages(self):
        """ Downloads necessary packages using Aria2 """
        conf_file = "/tmp/pacman.conf"

        if len(self.settings.get('cache')) > 0:
            cache_dir = self.settings.get('cache')
        else:
            cache_dir = "%s/var/cache/pacman/pkg" % self.dest_dir

        download.DownloadPackages(self.packages, conf_file, cache_dir, self.callback_queue)

    def write_file(self, filecontents, filename):
        """ writes a string of data to disk """
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        try:
            with open(filename, "w") as fh:
                fh.write(filecontents)
        except IOError as e:
            logging.exception(e)

        return True

    def create_pacman_conf_file(self):
        """ Needs Mako (see http://www.makotemplates.org/) """
        self.queue_event('debug', "Creating a temporary pacman.conf for %s architecture" % self.arch)

        # Add template functionality ;-)
        template_file_name = os.path.join(self.settings.get('data'), 'pacman.tmpl')
        file_template = Template(filename=template_file_name)
        self.write_file(file_template.render(destDir=self.dest_dir, arch=self.arch), os.path.join("/tmp", "pacman.conf"))

    def create_pacman_conf(self):
        self.create_pacman_conf_file()

        ## Init pyalpm
        try:
            self.pac = pac.Pac("/tmp/pacman.conf", self.callback_queue)
        except:
            raise InstallError("Can't initialize pyalpm.")

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
        dirs = ["var/cache/pacman/pkg", "var/lib/pacman"]

        for pacman_dir in dirs:
            mydir = os.path.join(self.dest_dir, pacman_dir)
            if not os.path.exists(mydir):
                os.makedirs(mydir)

        self.prepare_pacman_keychain()

        alpm = self.init_alpm()        
        alpm.do_refresh()      
        del alpm

    def select_packages(self):
        """ Prepare pacman and get package list from Internet """
        self.create_pacman_conf()
        self.prepare_pacman()
        
        self.packages = []
        
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
                logging.debug(_("Can't retrieve remote package list, using a local file instead."))
                data_dir = self.settings.get("data")
                packages_xml = os.path.join(data_dir, 'packages.xml')

        tree = etree.parse(packages_xml)
        root = tree.getroot()
        
        # Add common packages
        logging.debug(_("Adding all desktops common packages"))

        for child in root.iter('common'):
            for pkg in child.iter('pkgname'):
                self.packages.append(pkg.text)

        # Add specific desktop packages
        if self.desktop != "nox":
            for child in root.iter('graphic'):
                for pkg in child.iter('pkgname'):
                    # If package is Desktop Manager, save the name to activate the correct service later
                    if pkg.attrib.get('dm'):
                        self.desktop_manager = pkg.attrib.get('name')
                    self.packages.append(pkg.text)

            logging.debug(_("Adding '%s' desktop packages"), self.desktop)

            for child in root.iter(self.desktop + '_desktop'):
                for pkg in child.iter('pkgname'):
                    # If package is Network Manager, save the name to activate the correct service later
                    if pkg.attrib.get('nm'):
                        self.network_manager = pkg.attrib.get('name')
                    if pkg.attrib.get('conflicts'):
                        self.conflicts.append(pkg.attrib.get('conflicts'))
                    self.packages.append(pkg.text)

            # Set KDE language pack
            if self.desktop == 'kde':
                pkg = ""
                base_name = 'kde-l10n-'
                lang_name = self.settings.get("language_name").lower()
                if lang_name == "english":
                    # There're some English variants available but not all of them.
                    lang_packs = ['en_gb']
                    locale = self.settings.get('locale').split('.')[0]
                    if locale in lang_packs:
                        pkg = base_name + locale
                else:
                    # All the other language packs use their language code
                    lang_code = self.settings.get('language_code')
                    pkg = base_name + lang_code
                if len(pkg) > 0:
                    logging.debug(_("Selected kde language pack: %s"), pkg)
                    self.packages.append(pkg)
        else:
            # Add specific NoX/Base packages
            for child in root.iter('nox'):
                for pkg in child.iter('pkgname'):
                    if pkg.attrib.get('nm'):
                        self.network_manager = pkg.attrib.get('name')
                    if pkg.attrib.get('conflicts'):
                        self.conflicts.append(pkg.attrib.get('conflicts'))
                    self.packages.append(pkg.text)

        # Add ntp package if user selected it in timezone screen
        if self.settings.get('use_ntp'):
            for child in root.iter('ntp'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        # Get packages needed for detected hardware
        try:
            import hardware.hardware as hardware
            hardware_install = hardware.HardwareInstall()
            hardware_pkgs = hardware_install.get_packages()
            if len(hardware_pkgs) > 0:
                txt = " ".join(hardware_pkgs)
                logging.debug(_("Hardware module added these packages : %s"), txt)
                if 'virtualbox-guest-utils' in hardware_pkgs:
                    self.vbox = True
                self.packages.extend(hardware_pkgs)
        except ImportError:
            logging.warning(_("Can't import hardware module."))
        except Exception as err:
            logging.warning(_("Unknown error in hardware module. Output: %s"), err)
            
        # By default, hardware module adds vesa driver but in a NoX install we don't want it
        if self.desktop == "nox":
            if "v86d" in self.packages:
                self.packages.remove("v86d")
            if "xf86-video-vesa" in self.packages:
                self.packages.remove("xf86-video-vesa")

        # Add filesystem packages

        logging.debug(_("Adding filesystem packages"))

        fs_types = subprocess.check_output(["blkid", "-c", "/dev/null", "-o", "value", "-s", "TYPE"]).decode()

        fs_lib = ('btrfs', 'ext', 'ext2', 'ext3', 'ext4', 'fat', 'fat32', 'f2fs', 'jfs', 'nfs', 'nilfs2', 'ntfs',
                  'reiserfs', 'vfat', 'xfs')

        for iii in self.fs_devices:
            fs_types += self.fs_devices[iii]

        for fsys in fs_lib:
            if fsys in fs_types:
                if fsys == 'ext2' or fsys == 'ext3' or fsys == 'ext4':
                    fsys = 'ext'
                if fsys == 'fat16' or fsys == 'fat32':
                    fsys ='vfat'
                for child in root.iter(fsys):
                    for pkg in child.iter('pkgname'):
                        self.packages.append(pkg.text)

        # Check for user desired features and add them to our installation
        logging.debug(_("Check for user desired features and add them to our installation"))
        self.add_features_packages(root)
        logging.debug(_("All features needed packages have been added"))

        # Add chinese fonts
        lang_code = self.settings.get("language_code")
        if lang_code == "zh_TW" or lang_code == "zh_CN":
            logging.debug(_("Selecting chinese fonts."))
            for child in root.iter('chinese'):
                for pkg in child.iter('pkgname'):
                    self.packages.append(pkg.text)

        # Add bootloader packages if needed
        logging.debug(_("Adding bootloader packages if needed"))
        if self.settings.get('install_bootloader'):
            btype = self.settings.get('bootloader_type')
            if btype == "GRUB2":
                for child in root.iter('grub'):
                    for pkg in child.iter('pkgname'):
                        uefi = pkg.attrib.get('uefi')
                        if not uefi:
                            self.packages.append(pkg.text)
            elif btype == "UEFI_x86_64":
                for child in root.iter('grub'):
                    for pkg in child.iter('pkgname'):
                        self.packages.append(pkg.text)
            elif btype == "UEFI_i386":
                for child in root.iter('grub'):
                    for pkg in child.iter('pkgname'):
                        self.packages.append(pkg.text)

    def add_features_packages(self, root):
        """ Selects packages based on user selected features """
        desktop = self.settings.get("desktop")
        lib = desktops.LIBS
        features = desktops.FEATURES
        
        for feature in features[desktop]:
            # Add necessary packages for user desired features to our install list
            if self.settings.get("feature_" + feature):
                logging.debug(_("Adding packages for '%s' feature."), feature)
                for child in root.iter(feature):
                    for pkg in child.iter('pkgname'):
                        # If it's a specific gtk or qt package we have to check it
                        # against our chosen desktop.
                        plib = pkg.attrib.get('lib')
                        if plib is None or (plib is not None and desktop in lib[plib]):
                            logging.debug(_("Selecting package %s for feature %s"), pkg.text, feature)
                            self.packages.append(pkg.text)
                        #else:
                        #    logging.debug(_("Skipping a %s lib package: %s for feature %s"), plib, pkg.text, feature)
                        
                        if pkg.attrib.get('conflicts'):
                            self.conflicts.append(pkg.attrib.get('conflicts'))

        # Add libreoffice language package
        if self.settings.get('feature_office'):
            logging.debug(_("Add libreoffice language package"))
            pkg = ""
            lang_name = self.settings.get("language_name").lower()
            if lang_name == "english":
                # There're some English variants available but not all of them.
                lang_packs = ['en-GB', 'en-US', 'en-ZA']
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
        process2 = subprocess.Popen(["grep", "Model:[[:space:]]"],
                                    stdin=process1.stdout, stdout=subprocess.PIPE)
        process1.stdout.close()
        out, err = process2.communicate()
        return out.decode().lower()

    def get_cpu(self):
        # Check if system is an intel system. Not sure if we want to move this to hardware module when its done.
        process1 = subprocess.Popen(["hwinfo", "--cpu"], stdout=subprocess.PIPE)
        process2 = subprocess.Popen(["grep", "Model:[[:space:]]"],
                                    stdin=process1.stdout, stdout=subprocess.PIPE)
        process1.stdout.close()
        out, err = process2.communicate()
        return out.decode().lower()

    def init_alpm(self):
        try:
            alpm = pac.Pac("/tmp/pacman.conf", self.callback_queue)
        except Exception as err:
            logging.error(err)
            raise InstallError("Can't initialize pyalpm: %s" % err)
        return alpm       

    def do_install(self, download_only=False):
        pacman_options = {}
        if download_only:
            pacman_options["downloadonly"] = True
            txt = _("Downloading packages...")
        else:
            pacman_options["needed"] = True
            txt = _("Installing packages...")
        logging.debug(txt)
        
        alpm = self.init_alpm()
        result = alpm.do_install(pkgs=self.packages, conflicts=self.conflicts, options=pacman_options)
        del alpm

        if result == 1:
            if download_only:
                txt = _("Can't download all necessary packages. Cnchi will continue and try again this download later.")
                logging.error(txt)
            else:
                raise InstallError(_("Can't install necessary packages. Cnchi can't continue."))

    def install_packages(self):
        """ Start pacman installation of packages """
        self.chroot_mount_special_dirs()

        # First try to download all necessary packages (download only)
        self.do_install(download_only=True)
        
        # Ok, now we can install all downloaded packages
        # (alpm will try to download again those that couldn't download before)
        self.do_install()

        self.chroot_umount_special_dirs()
        
        # All downloading and installing has been done, so we hide progress bar
        self.queue_event('progress_bar', 'hide')
        
    def chroot_mount_special_dirs(self):
        """ Mount special directories for our chroot """
        # Don't try to remount them
        if self.special_dirs_mounted:
            logging.debug(_("Special dirs already mounted."))
            return

        special_dirs = ["sys", "proc", "dev", "dev/pts", "sys/firmware/efi"]
        for s_dir in special_dirs:
            mydir = os.path.join(self.dest_dir, s_dir)
            if not os.path.exists(mydir):
                os.makedirs(mydir)

        mydir = os.path.join(self.dest_dir, "sys")
        subprocess.check_call(["mount", "-t", "sysfs", "/sys", mydir])
        subprocess.check_call(["chmod", "555", mydir])

        mydir = os.path.join(self.dest_dir, "proc")
        subprocess.check_call(["mount", "-t", "proc", "/proc", mydir])
        subprocess.check_call(["chmod", "555", mydir])

        mydir = os.path.join(self.dest_dir, "dev")
        subprocess.check_call(["mount", "-o", "bind", "/dev", mydir])

        mydir = os.path.join(self.dest_dir, "dev/pts")
        subprocess.check_call(["mount", "-t", "devpts", "/dev/pts", mydir])
        subprocess.check_call(["chmod", "555", mydir])

        efi = "/sys/firmware/efi"
        if os.path.exists(efi):
            mydir = os.path.join(self.dest_dir, efi[1:])
            subprocess.check_call(["mount", "-o", "bind", efi, mydir])

        self.special_dirs_mounted = True

    def chroot_umount_special_dirs(self):
        """ Umount special directories for our chroot """
        # Do not umount if they're not mounted
        if not self.special_dirs_mounted:
            logging.debug(_("Special dirs are not mounted. Skipping."))
            return
        efi = "/sys/firmware/efi"
        if os.path.exists(efi):
            special_dirs = ["dev/pts", "sys/firmware/efi", "sys", "proc", "dev"]
        else:
            special_dirs = ["dev/pts", "sys", "proc", "dev"]

        for s_dir in special_dirs:
            mydir = os.path.join(self.dest_dir, s_dir)
            try:
                subprocess.check_call(["umount", mydir])
            except subprocess.CalledProcessError as err:
                # Can't unmount. Try -l to force it.
                try:
                    subprocess.check_call(["umount", "-l", mydir])
                except subprocess.CalledProcessError as err:
                    logging.warning(_("Unable to umount %s") % mydir)
                    cmd = _("Command %s has failed.") % err.cmd
                    logging.warning(cmd)
                    out = _("Output : %s") % err.output 
                    logging.warning(out)
            except Exception as err:
                logging.warning(_("Unable to umount %s") % mydir)
                logging.error(err)

        self.special_dirs_mounted = False

    def chroot(self, cmd, timeout=None, stdin=None):
        """ Runs command inside the chroot """
        run = ['chroot', self.dest_dir]

        for element in cmd:
            run.append(element)

        try:
            proc = subprocess.Popen(run,
                                    stdin=stdin,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate(timeout=timeout)[0]
            txt = out.decode()
            if len(txt) > 0:
                logging.debug(txt)
        except OSError as err:
            logging.exception(_("Error running command: %s"), err.strerror)
            raise
        except subprocess.TimeoutExpired as err:
            logging.exception(_("Timeout running command: %s"), run)
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

                try:
                    shutil.copy(source_network, target_network)
                except FileNotFoundError:
                    logging.warning(_("Can't copy network configuration files"))
                except FileExistsError:
                    pass

    def auto_fstab(self):
        """ Create /etc/fstab file """

        all_lines = ["# /etc/fstab: static file system information.", "#",
                     "# Use 'blkid' to print the universally unique identifier for a",
                     "# device; this may be used with UUID= as a more robust way to name devices",
                     "# that works even if disks are added and removed. See fstab(5).", "#",
                     "# <file system> <mount point>   <type>  <options>       <dump>  <pass>", "#"]

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

            # Fix for home + luks, no lvm
            if "/home" in path and self.settings.get("use_luks") and not self.settings.get("use_lvm"):
                # Modify the crypttab file
                if self.settings.get("luks_key_pass") != "":
                    home_keyfile = "none"
                else:
                    home_keyfile = "/etc/luks-keys/home"
                subprocess.check_call(['chmod', '0777', '%s/etc/crypttab' % self.dest_dir])
                with open('%s/etc/crypttab' % self.dest_dir, 'a') as crypttab_file:
                    line = "cryptAntergosHome /dev/disk/by-uuid/%s %s luks\n" % (uuid, home_keyfile)
                    crypttab_file.write(line)
                    logging.debug(_("Added to crypttab : %s"), line)
                subprocess.check_call(['chmod', '0600', '%s/etc/crypttab' % self.dest_dir])

                all_lines.append("/dev/mapper/cryptAntergosHome %s %s %s 0 %s" % (path, myfmt, opts, chk))
                logging.debug(_("Added to fstab : /dev/mapper/cryptAntergosHome %s %s %s 0 %s"), path, myfmt, opts, chk)
                continue

            # fstab uses vfat to mount fat16 and fat32 partitions
            if "fat" in myfmt:
                myfmt = 'vfat'

            # Avoid adding a partition to fstab when
            # it has no mount point (swap has been checked before)
            if path == "":
                continue
            else:
                full_path = os.path.join(self.dest_dir, path)
                subprocess.check_call(["mkdir", "-p", full_path])

            if not self.ssd:
                if "btrfs" in myfmt:
                    chk = '0'
                    opts = 'rw,relatime,space_cache,autodefrag,inode_cache'
                elif "f2fs" in myfmt:
                    chk = '0'
                    opts = 'rw,noatime'
                elif "ext2" in myfmt:
                    chk = '0'
                    opts = 'rw,relatime'
                elif path == '/':
                    chk = '1'
                    opts = "rw,relatime,data=ordered"
                else:
                    chk = '0'
                    opts = "rw,relatime,data=ordered"

            else:
                for i in self.ssd:
                    if i in self.mount_devices[path] and self.ssd[i]:
                        opts = 'defaults,noatime'
                        # As of linux kernel version 3.7, the following
                        # filesystems support TRIM: ext4, btrfs, JFS, and XFS.
                        # If using a TRIM supported SSD, discard is a valid mount option for swap
                        if myfmt == 'ext4' or myfmt == 'jfs' or myfmt == 'xfs' or myfmt == 'swap':
                            opts += ',discard'
                        elif myfmt == 'btrfs':
                            opts = 'rw,noatime,compress=lzo,ssd,discard,space_cache,autodefrag,inode_cache'
                        elif myfmt == 'f2fs':
                            opts = 'rw,noatime'

            all_lines.append("UUID=%s %s %s %s 0 %s" % (uuid, path, myfmt, opts, chk))
            logging.debug(_("Added to fstab : UUID=%s %s %s %s 0 %s"), uuid, path, myfmt, opts, chk)

        # Create tmpfs line in fstab
        tmpfs = "tmpfs /tmp tmpfs defaults,noatime,mode=1777 0 0"
        all_lines.append(tmpfs)
        logging.debug(_("Added to fstab : %s"), tmpfs)

        full_text = '\n'.join(all_lines)
        full_text += '\n'

        fstab_path = '%s/etc/fstab' % self.dest_dir
        with open(fstab_path, 'w') as fstab_file:
            fstab_file.write(full_text)
            
        logging.debug(_("fstab written."))

    def install_bootloader(self):
        """ Installs bootloader """

        self.modify_grub_default()
        self.prepare_grub_d()
        
        # Freeze and unfreeze xfs filesystems to enable grub(2) installation on xfs filesystems
        self.freeze_xfs()
        
        bootloader = self.settings.get('bootloader_type')
        if bootloader == "GRUB2":
            self.install_bootloader_grub2_bios()
        else:
            self.install_bootloader_grub2_efi(bootloader)

    def modify_grub_default(self):
        """ If using LUKS, we need to modify GRUB_CMDLINE_LINUX to load our root encrypted partition
            This scheme can be used in the automatic installation option only (at this time) """

        default_dir = os.path.join(self.dest_dir, "etc/default")
        default_grub = os.path.join(default_dir, "grub")
        theme = 'GRUB_THEME="/boot/grub/themes/Antergos-Default/theme.txt"'
        
        if "swap" in self.mount_devices:
            swap_partition = self.mount_devices["swap"]
            swap_uuid = fs.get_info(swap_partition)['UUID']
            kernel_cmd = 'GRUB_CMDLINE_LINUX_DEFAULT="resume=UUID=%s quiet"' % swap_uuid
        else:
            kernel_cmd = 'GRUB_CMDLINE_LINUX_DEFAULT="quiet"'

        if not os.path.exists(default_dir):
            os.mkdir(default_dir)

        if self.method == 'automatic' and self.settings.get('use_luks'):
            root_device = self.mount_devices["/"]
            boot_device = self.mount_devices["/boot"]
            root_uuid = fs.get_info(root_device)['UUID']
            boot_uuid = fs.get_info(boot_device)['UUID']

            # Let GRUB automatically add the kernel parameters for root encryption
            if self.settings.get("luks_key_pass") == "":
                default_line = 'GRUB_CMDLINE_LINUX="cryptdevice=/dev/disk/by-uuid/%s:cryptAntergos ' \
                               'cryptkey=/dev/disk/by-uuid/%s:ext2:/.keyfile-root"' % (root_uuid, boot_uuid)
            else:
                default_line = 'GRUB_CMDLINE_LINUX="cryptdevice=/dev/disk/by-uuid/%s:cryptAntergos"' % root_uuid

            with open(default_grub) as grub_file:
                lines = [x.strip() for x in grub_file.readlines()]

            for i in range(len(lines)):
                if lines[i].startswith("#GRUB_CMDLINE_LINUX") or lines[i].startswith("GRUB_CMDLINE_LINUX"):
                    if not lines[i].startswith("#GRUB_CMDLINE_LINUX_DEFAULT"):
                        if not lines[i].startswith("GRUB_CMDLINE_LINUX_DEFAULT"):
                            lines[i] = default_line
                elif lines[i].startswith("#GRUB_THEME") or lines[i].startswith("GRUB_THEME"):
                    lines[i] = theme
                elif lines[i].startswith("#GRUB_CMDLINE_LINUX_DEFAULT") or \
                        lines[i].startswith("GRUB_CMDLINE_LINUX_DEFAULT"):
                    lines[i] = kernel_cmd
                elif lines[i].startswith("#GRUB_DISTRIBUTOR") or lines[i].startswith("GRUB_DISTRIBUTOR"):
                    lines[i] = "GRUB_DISTRIBUTOR=Antergos"

            with open(default_grub, 'w') as grub_file:
                grub_file.write("\n".join(lines) + "\n")
        else:
            with open(default_grub) as grub_file:
                lines = [x.strip() for x in grub_file.readlines()]

            for i in range(len(lines)):
                if lines[i].startswith("#GRUB_THEME") or lines[i].startswith("GRUB_THEME"):
                    lines[i] = theme
                elif lines[i].startswith("#GRUB_CMDLINE_LINUX_DEFAULT"):
                    lines[i] = kernel_cmd
                elif lines[i].startswith("GRUB_CMDLINE_LINUX_DEFAULT"):
                    lines[i] = kernel_cmd
                elif lines[i].startswith("#GRUB_DISTRIBUTOR") or lines[i].startswith("GRUB_DISTRIBUTOR"):
                    lines[i] = "GRUB_DISTRIBUTOR=Antergos"

            with open(default_grub, 'w') as grub_file:
                grub_file.write("\n".join(lines) + "\n")

        # Add GRUB_DISABLE_SUBMENU=y to avoid bug https://bugs.archlinux.org/task/37904
        #with open(default_grub, 'a') as grub_file:
        #    grub_file.write("\n# See bug https://bugs.archlinux.org/task/37904\n")
        #    grub_file.write("GRUB_DISABLE_SUBMENU=y\n\n")

        logging.debug(_("/etc/default/grub configuration completed successfully."))

    def prepare_grub_d(self):
        # Copy 01_antergos script into /etc/grub.d.
        grub_d_dir = os.path.join(self.dest_dir, "etc/grub.d")
        script_dir = os.path.join(self.settings.get("cnchi"), "scripts")
        script = "10_antergos"

        if not os.path.exists(grub_d_dir):
            os.makedirs(grub_d_dir)

        try:
            shutil.copy2(os.path.join(script_dir, script), grub_d_dir)
            os.chmod(os.path.join(grub_d_dir, script), 755)
        except FileNotFoundError:
            logging.debug(_("Could not copy %s to grub.d"), script)
        except FileExistsError:
            pass

    def install_bootloader_grub2_bios(self):
        """ Install bootloader in a BIOS system """
        grub_location = self.settings.get('bootloader_device')
        self.queue_event('info', _("Installing GRUB(2) BIOS boot loader in %s") % grub_location)

        self.chroot_mount_special_dirs()
        
        grub_install = ['grub-install', '--directory=/usr/lib/grub/i386-pc', '--target=i386-pc',
                        '--boot-directory=/boot', '--recheck']
        
        if len(grub_location) > 8:  # ex: /dev/sdXY > 8
            grub_install.append("--force")
        
        grub_install.append(grub_location)
        
        self.chroot(grub_install)

        self.install_bootloader_grub2_locales()

        self.copy_bootloader_theme_files()

        locale = self.settings.get("locale")
        try:
            self.chroot(['sh', '-c', 'LANG=%s grub-mkconfig -o /boot/grub/grub.cfg' % locale], 45)
        except subprocess.TimeoutExpired:
            logging.error(_("grub-mkconfig appears to be hung. Killing grub-mount and os-prober so we can continue."))
            os.system("killall grub-mount")
            os.system("killall os-prober")

        self.chroot_umount_special_dirs()

        core_path = os.path.join(self.dest_dir, "boot/grub/i386-pc/core.img")
        if os.path.exists(core_path):
            self.queue_event('info', _("GRUB(2) BIOS has been successfully installed."))
            self.settings.set('bootloader_ok', True)
        else:
            logging.warning(_("ERROR installing GRUB(2) BIOS."))
            self.settings.set('bootloader_ok', False)

    def install_bootloader_grub2_efi(self, arch):
        """ Install bootloader in a UEFI system """
        uefi_arch = "x86_64"
        spec_uefi_arch = "x64"
        spec_uefi_arch_caps = "X64"

        if arch == "UEFI_i386":
            uefi_arch = "i386"
            spec_uefi_arch = "ia32"
            spec_uefi_arch_caps = "IA32"

        self.queue_event('info', _("Installing GRUB(2) UEFI %s boot loader") % uefi_arch)

        try:
            subprocess.check_call(['grub-install --target=%s-efi --efi-directory=/install/boot '
                                   '--bootloader-id=antergos_grub --boot-directory=/install/boot '
                                   '--recheck' % uefi_arch], shell=True, timeout=45)
        except subprocess.CalledProcessError as err:
            logging.error('Command grub-install failed. Error output: %s' % err.output)
        except subprocess.TimeoutExpired:
            logging.error('Command grub-install timed out.')
        except Exception as err:
            logging.error('Command grub-install failed. Unknown Error: %s' % err)

        self.install_bootloader_grub2_locales()
        
        self.copy_bootloader_theme_files()

        # Copy grub into dirs known to be used as default by some OEMs if they are empty.
        defaults = [(os.path.join(self.dest_dir, "boot/EFI/BOOT/"), 'BOOT' + spec_uefi_arch_caps + '.efi'),
                    (os.path.join(self.dest_dir, "boot/EFI/Microsoft/Boot/"), 'bootmgfw.efi')]
        grub_dir_src = os.path.join(self.dest_dir, "boot/EFI/antergos_grub/")
        grub_efi_old = ('grub' + spec_uefi_arch + '.efi')
        
        for default in defaults:
            path, grub_efi_new = default
            if not os.path.exists(path):
                self.queue_event('info', _("No OEM loader found in %s. Copying Grub(2) into dir.") % path)
                os.makedirs(path)
                try:
                    shutil.copy(grub_dir_src + grub_efi_old, path + grub_efi_new)
                except FileNotFoundError:
                    logging.warning(_("Copying Grub(2) into OEM dir failed. File Not Found."))
                except FileExistsError:
                    logging.warning(_("Copying Grub(2) into OEM dir failed. File Exists."))
                except Exception as err:
                    logging.warning(_("Copying Grub(2) into OEM dir failed. Unknown Error."))
                    logging.warning(err)
        
        # Copy uefi shell if none exists in /boot/EFI
        shell_src = "/usr/share/cnchi/grub2-theme/shellx64_v2.efi"
        shell_dst = os.path.join(self.dest_dir, "boot/EFI/")
        try:
            shutil.copy2(shell_src, shell_dst)
        except FileNotFoundError:
            logging.warning(_("UEFI Shell drop-in not found at %s"), shell_src)
        except FileExistsError:
            pass
        except Exception as err:
            logging.warning(_("UEFI Shell drop-in could not be copied."))
            logging.warning(err)

        # Run grub-mkconfig last
        self.queue_event('info', _("Generating grub.cfg"))
        self.chroot_mount_special_dirs()

        locale = self.settings.get("locale")
        try:
            self.chroot(['sh', '-c', 'LANG=%s grub-mkconfig -o /boot/grub/grub.cfg' % locale], 45)
        except subprocess.TimeoutExpired:
            logging.error(_("grub-mkconfig appears to be hung. Killing grub-mount and os-prober so we can continue."))
            os.system("killall grub-mount")
            os.system("killall os-prober")

        self.chroot_umount_special_dirs()

        path = ((os.path.join(self.dest_dir, "boot/grub/x86_64-efi/core.efi")), (os.path.join(self.dest_dir,
               ("boot/EFI/antergos_grub/" + grub_efi_old))))
        exists = []
        for p in path:
            if os.path.exists(p):
                exists.append(p)
        if len(exists) == 0:
            logging.warning(_("GRUB(2) UEFI install may not have completed successfully."))
            self.settings.set('bootloader_ok', False)
        else:
            self.queue_event('info', _("GRUB(2) UEFI install completed successfully"))
            self.settings.set('bootloader_ok', True)

    def copy_bootloader_theme_files(self):
        self.queue_event('info', _("Copying GRUB(2) Theme Files"))
        theme_dir_src = "/usr/share/cnchi/grub2-theme/Antergos-Default"
        theme_dir_dst = os.path.join(self.dest_dir, "boot/grub/themes/Antergos-Default")
        try:
            shutil.copytree(theme_dir_src, theme_dir_dst)
        except FileNotFoundError:
            logging.warning(_("Grub2 theme files not found"))
        except FileExistsError:
            logging.warning(_("Grub2 theme files already exist."))

    def install_bootloader_grub2_locales(self):
        """ Install Grub2 locales """
        self.queue_event('info', _("Installing Grub2 locales."))
        dest_locale_dir = os.path.join(self.dest_dir, "boot/grub/locale")

        if not os.path.exists(dest_locale_dir):
            os.makedirs(dest_locale_dir)

        grub_mo = os.path.join(self.dest_dir, "usr/share/locale/en@quot/LC_MESSAGES/grub.mo")

        try:
            shutil.copy2(grub_mo, os.path.join(dest_locale_dir, "en.mo"))
        except FileNotFoundError:
            logging.warning(_("Can't install GRUB(2) locale."))
        except FileExistsError:
            # Ignore if already exists
            pass
    
    def freeze_xfs(self):
        """ Freeze and unfreeze xfs, as hack for grub(2) installing """
        if not os.path.exists("/usr/bin/xfs_freeze"):
            return

        xfs_boot = False
        xfs_root = False

        try:
            subprocess.check_call(["sync"])
            with open("/proc/mounts", "r") as mounts_file:
                mounts = mounts_file.readlines()
            # We leave a blank space in the end as we want to search exactly for this mount points
            boot_mount_point = self.dest_dir + "/boot "
            root_mount_point = self.dest_dir + " "
            for line in mounts:
                if " xfs " in line:
                    if boot_mount_point in line:
                        xfs_boot = True
                    elif root_mount_point in line:
                        xfs_root = True
            if xfs_boot:
                boot_mount_point = boot_mount_point.rstrip()
                subprocess.check_call(["/usr/bin/xfs_freeze", "-f", boot_mount_point])
                subprocess.check_call(["/usr/bin/xfs_freeze", "-u", boot_mount_point])
            if xfs_root:
                subprocess.check_call(["/usr/bin/xfs_freeze", "-f", self.dest_dir])
                subprocess.check_call(["/usr/bin/xfs_freeze", "-u", self.dest_dir])
        except subprocess.CalledProcessError as err:
            logging.warning(_("Can't freeze/unfreeze xfs system"))

    def enable_services(self, services):
        """ Enables all services that are in the list 'services' """
        for name in services:
            self.chroot(['systemctl', 'enable', name + ".service"])
            logging.debug(_("Enabled %s service."), name)

    def change_user_password(self, user, new_password):
        """ Changes the user's password """
        try:
            shadow_password = crypt.crypt(new_password, "$6$%s$" % user)
        except:
            logging.warning(_("Error creating password hash for user %s"), user)
            return False

        try:
            self.chroot(['usermod', '-p', shadow_password, user])
        except:
            logging.warning(_("Error changing password for user %s"), user)
            return False

        return True

    def auto_timesetting(self):
        """ Set hardware clock """
        subprocess.check_call(["hwclock", "--systohc", "--utc"])
        shutil.copy2("/etc/adjtime", "%s/etc/" % self.dest_dir)

    def set_mkinitcpio_hooks_and_modules(self, hooks, modules):
        """ Set up mkinitcpio.conf """
        logging.debug(_("Setting hooks and modules in mkinitcpio.conf"))
        logging.debug('HOOKS="%s"', ' '.join(hooks))
        logging.debug('MODULES="%s"', ' '.join(modules))

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

        cpu = self.get_cpu()

        hooks = ["base", "udev", "autodetect", "modconf", "block", "keyboard", "keymap"]
        modules = []

        # It is important that the encrypt hook comes before the filesystems hook
        # (in case you are using LVM on LUKS, the order should be: encrypt lvm2 filesystems)

        if self.settings.get("use_luks"):
            hooks.append("encrypt")
            if self.arch == 'x86_64':
                modules.extend(["dm_mod", "dm_crypt", "ext4", "aes_x86_64", "sha256", "sha512"])
            else:
                modules.extend(["dm_mod", "dm_crypt", "ext4", "aes_i586", "sha256", "sha512"])

        if self.settings.get("f2fs"):
            modules.append("f2fs")

        if self.blvm or self.settings.get("use_lvm"):
            hooks.append("lvm2")

        if "swap" in self.mount_devices:
            hooks.append("resume")

        hooks.append("filesystems")

        if self.settings.get('btrfs') and cpu is not 'genuineintel':
            modules.append("crc32c")
        elif self.settings.get('btrfs') and cpu is 'genuineintel':
            modules.append("crc32c-intel")
        else:
            hooks.append("fsck")

        self.set_mkinitcpio_hooks_and_modules(hooks, modules)

        # Run mkinitcpio on the target system
        # Fix for bsdcpio error. See: http://forum.antergos.com/viewtopic.php?f=5&t=1378&start=20#p5450
        locale = self.settings.get('locale')
        self.chroot_mount_special_dirs()
        self.chroot(['sh', '-c', 'LANG=%s /usr/bin/mkinitcpio -p %s' % (locale, self.kernel_pkg)])
        self.chroot_umount_special_dirs()

    def generate_pacmanconf(self):
        with open("%s/etc/pacman.conf" % self.dest_dir, "a") as pacmanconf:
            pacmanconf.write("\n\n")
            pacmanconf.write("[antergos]\n")
            pacmanconf.write("SigLevel = PackageRequired\n")
            pacmanconf.write("Include = /etc/pacman.d/antergos-mirrorlist\n")

    def uncomment_locale_gen(self, locale):
        """ Uncomment selected locale in /etc/locale.gen """
        #self.chroot(['sed', '-i', '-r', '"s/#(.*%s)/\1/g"' % locale, "/etc/locale.gen"])

        text = []
        with open("%s/etc/locale.gen" % self.dest_dir) as gen:
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
        """ Copy all packages from specified directory to install's target """
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
            self.queue_event('percent', percent)
            source = os.path.join(src, item)
            destination = os.path.join(dst, item)
            try:
                shutil.copy2(source, destination)
            except (FileExistsError, shutil.Error) as err:
                logging.warning(err)
            percent += step

    def setup_features(self):
        """ Do all set up needed by the user's selected features """
        #if self.settings.get("feature_aur"):
        #    logging.debug(_("Configuring AUR..."))

        if self.settings.get("feature_bluetooth"):
            logging.debug(_("Configuring bluetooth..."))
            service = os.path.join(self.dest_dir, "usr/lib/systemd/system/bluetooth.service")
            if os.path.exists(service):
                self.enable_services(['bluetooth'])

        if self.settings.get("feature_cups"):
            logging.debug(_("Configuring CUPS..."))
            service = os.path.join(self.dest_dir, "usr/lib/systemd/system/cups.service")
            if os.path.exists(service):
                self.enable_services(['cups'])

        #if self.settings.get("feature_office"):
        #    logging.debug(_("Configuring libreoffice..."))

        #if self.settings.get("feature_visual"):
        #    logging.debug(_("Configuring Compositing manager..."))

        if self.settings.get("feature_firewall"):
            logging.debug(_("Configuring firewall..."))
            self.chroot_mount_special_dirs()
            # This won't work if we're installing a new linux kernel
            try:
                self.chroot(["ufw", "default", "deny"])
                toallow = misc.get_network()
                if toallow:
                    self.chroot(["ufw", "allow", "from", toallow])
                self.chroot(["ufw", "allow", "Transmission"])
                self.chroot(["ufw", "allow", "SSH"])
                self.chroot(["ufw", "enable"])
            except OSError as err:
                logging.warning(_("Couldn't configure the firewall: %s") % err)
            finally:
                self.chroot_umount_special_dirs()

            service = os.path.join(self.dest_dir, "usr/lib/systemd/system/ufw.service")
            if os.path.exists(service):
                self.enable_services(['ufw'])

    def set_display_manager(self):
        """ Configures the installed desktop manager, including autologin. """
        self.queue_event('info', _("%s: Configuring display manager.") % self.desktop_manager)

        sessions = {'gnome': 'gnome', 'cinnamon': 'cinnamon', 'razor': 'razor-session', 'openbox': 'openbox',
                    'xfce': 'xfce', 'kde': 'kde-plasma', 'mate': 'mate', 'enlightenment': 'enlightenment'}
        desktop = self.settings.get('desktop')
        username = self.settings.get('username')
        
        if desktop in sessions:
            session = sessions[desktop]
        else:
            session = "default"

        autologin = not self.settings.get('require_password')

        try:        
            if self.desktop_manager == 'lightdm':
                self.setup_lightdm(desktop, username, session, autologin)
            elif self.desktop_manager == 'gdm':
                self.setup_gdm(desktop, username, session, autologin)
            elif self.desktop_manager == 'kdm':
                self.setup_kdm(desktop, username, session, autologin)
            elif self.desktop_manager == 'lxdm':
                self.setup_lxdm(desktop, username, session, autologin)
            elif self.desktop_manager == 'slim':
                self.setup_slim(desktop, username, session, autologin)
                
            logging.debug(_("Completed %s display manager configuration."), self.desktop_manager)
        except FileNotFoundError:
            logging.debug(_("Error while trying to configure '%s' display manager"), self.desktop_manager)
    
    def setup_lightdm(self, desktop, username, session, autologin):
        # Systems with LightDM as Desktop Manager
        lightdm_conf_path = os.path.join(self.dest_dir, "etc/lightdm/lightdm.conf")
        text = []
        with open(lightdm_conf_path) as lightdm_conf:
            text = lightdm_conf.readlines()
        with open(lightdm_conf_path, "w") as lightdm_conf:
            for line in text:
                if autologin:
                    # Enable automatic login
                    if '#autologin-user=' in line:
                        line = 'autologin-user=%s\n' % username
                    if '#autologin-user-timeout=0' in line:
                        line = 'autologin-user-timeout=0\n'
                # Set correct DE session
                if '#user-session=default' in line:
                    line = 'user-session=%s\n' % session
                lightdm_conf.write(line)

    def setup_gdm(self, desktop, username, session, autologin):
        # Systems with GDM as Desktop Manager
        if autologin:
            gdm_conf_path = os.path.join(self.dest_dir, "etc/gdm/custom.conf")
            with open(gdm_conf_path, "w") as gdm_conf:
                gdm_conf.write('# Cnchi - Enable automatic login for user\n')
                gdm_conf.write('[daemon]\n')
                gdm_conf.write('AutomaticLogin=%s\n' % username)
                gdm_conf.write('AutomaticLoginEnable=True\n')

    def setup_kdm(self, desktop, username, session, autologin):
        # Systems with KDM as Desktop Manager
        if autologin:
            kdm_conf_path = os.path.join(self.dest_dir, "usr/share/config/kdm/kdmrc")
            text = []
            with open(kdm_conf_path) as kdm_conf:
                text = kdm_conf.readlines()
            with open(kdm_conf_path, "w") as kdm_conf:
                for line in text:
                    if '#AutoLoginEnable=true' in line:
                        line = 'AutoLoginEnable=true\n'
                    if 'AutoLoginUser=' in line:
                        line = 'AutoLoginUser=%s\n' % username
                    kdm_conf.write(line)

    def setup_lxdm(self, desktop, username, session, autologin):
        # Systems with LXDM as Desktop Manager
        if autologin:
            lxdm_conf_path = os.path.join(self.dest_dir, "etc/lxdm/lxdm.conf")
            text = []
            with open(lxdm_conf_path) as lxdm_conf:
                text = lxdm_conf.readlines()
            with open(lxdm_conf_path, "w") as lxdm_conf:
                for line in text:
                    if '# autologin=dgod' in line:
                        line = 'autologin=%s\n' % username
                    lxdm_conf.write(line)

    def setup_slim(self, desktop, username, session, autologin):
        # Systems with SLiM as Desktop Manager
        slim_conf_path = os.path.join(self.dest_dir, "etc/slim.conf")
        text = []
        with open(slim_conf_path) as slim_conf:
            text = slim_conf.readlines()
        with open(slim_conf_path, "w") as slim_conf:
            for line in text:
                if autologin and 'auto_login' in line:
                    line = 'auto_login yes\n'
                if 'default_user' in line:
                    line = 'default_user %s\n' % username
                if 'current_theme' in line:
                    line = 'current_theme antergos-slim\n'
                slim_conf.write(line)

    def configure_system(self):
        """ Final install steps
            Set clock, language, timezone
            Run mkinitcpio
            Populate pacman keyring
            Setup systemd services
            ... and more """

        self.queue_event('pulse', 'start')
        self.queue_event('info', _("Configuring your new system"))

        self.auto_fstab()
        logging.debug(_("fstab file generated."))

        # Copy configured networks in Live medium to target system
        if self.network_manager == 'NetworkManager':
            self.copy_network_config()

        # Copy network profile when using netctl (and not networkmanager)
        # netctl is used in the noX desktop option
        elif self.network_manager == 'netctl':
            # Nowadays nearly everybody uses dhcp. If user wants to use a fixed IP the profile must be
            # edited by himself. Maybe we could ease this process?
            profile = 'ethernet-dhcp'
            if misc.is_wireless_enabled():
                # TODO: We should port wifi-menu from netctl package here.
                profile = 'wireless-wpa'

            # TODO: Just copying the default profile is NOT an elegant solution
            logging.debug(_("Cnchi will configure netctl using the %s profile"), profile)
            src_path = os.path.join(self.dest_dir, 'etc/netctl/examples/%s' % profile)
            dst_path = os.path.join(self.dest_dir, 'etc/netctl/%s' % profile)

            try:
                shutil.copy(src_path, dst_path)
            except FileNotFoundError:
                logging.warning(_("Can't copy network configuration profiles"))
            except FileExistsError:
                pass
            # Enable our profile
            self.chroot(['netctl', 'enable', profile])
            #logging.warning(_('Netctl is installed. Please edit %s to finish your network configuration.') % dst_path)

        logging.debug(_("Network configuration copied."))

        # Copy mirror list
        mirrorlist_path = os.path.join(self.dest_dir, 'etc/pacman.d/mirrorlist')
        try:
            shutil.copy2('/etc/pacman.d/mirrorlist', mirrorlist_path)
            logging.debug(_("Mirror list copied."))
        except FileNotFoundError:
            logging.warning(_("Can't copy mirrorlist file"))
        except FileExistsError:
            pass

        # Generate /etc/pacman.conf
        self.generate_pacmanconf()

        logging.debug(_("Generated /etc/pacman.conf"))

        desktop = self.settings.get('desktop')

        # Enable services
        if desktop != "nox":
            self.enable_services([self.desktop_manager, "ModemManager"])

        self.enable_services([self.network_manager])

        # Enable ntp service
        if self.settings.get("use_ntp"):
            self.enable_services(["ntpd"])

        # Set timezone
        zoneinfo_path = os.path.join("/usr/share/zoneinfo", self.settings.get("timezone_zone"))
        self.chroot(['ln', '-s', zoneinfo_path, "/etc/localtime"])

        logging.debug(_("Timezone set."))

        # Wait FOREVER until the user sets his params
        while self.settings.get('user_info_done') is False:
            # Wait five seconds and try again
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
        logging.debug(_("Sudo configuration for user %s done."), username)

        # Configure detected hardware
        try:
            import hardware.hardware as hardware
            hardware_install = hardware.HardwareInstall()
            logging.debug(_("Running post-install scripts from hardware module..."))
            hardware_install.post_install(self.dest_dir)
        except ImportError:
            logging.warning(_("Can't import hardware module."))
        except Exception as err:
            logging.warning(_("Unknown error in hardware module. Output: %s") % err)
            
        # Setup user

        default_groups = 'lp,video,network,storage,wheel,audio'
        
        if self.vbox:
            # Why there is no vboxusers group?
            self.chroot(['groupadd', 'vboxusers'])
            default_groups += ',vboxusers'

        if self.settings.get('require_password') is False:
            self.chroot(['groupadd', 'autologin'])
            default_groups += ',autologin'

        self.chroot(['useradd', '-m', '-s', '/bin/bash', '-g', 'users', '-G', default_groups, username])

        logging.debug(_("User %s added."), username)

        self.change_user_password(username, password)

        self.chroot(['chfn', '-f', fullname, username])

        self.chroot(['chown', '-R', '%s:users' % username, "/home/%s" % username])

        hostname_path = os.path.join(self.dest_dir, "etc/hostname")
        if not os.path.exists(hostname_path):
            with open(hostname_path, "w") as hostname_file:
                hostname_file.write(hostname)

        logging.debug(_("Hostname set to %s."), hostname)

        # User password is the root password
        self.change_user_password('root', password)
        logging.debug(_("Set the same password to root."))

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
            logging.debug(_("Set /etc/X11/xorg.conf.d/00-keyboard.conf for the xkblayout"))
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
            logging.debug(_("00-keyboard.conf written."))

        # Let's start without using hwdetect for mkinitcpio.conf.
        # I think it should work out of the box most of the time.
        # This way we don't have to fix deprecated hooks.
        # NOTE: With LUKS or LVM maybe we'll have to fix deprecated hooks.
        self.queue_event('info', _("Configuring System Startup..."))
        self.run_mkinitcpio()

        logging.debug(_("Call Cnchi post-install script"))
        # Call post-install script to execute (g,k)settings commands or install openbox defaults
        script_path_postinstall = os.path.join(self.settings.get('cnchi'), "scripts", POSTINSTALL_SCRIPT)
        try:
            subprocess.check_call(["/usr/bin/bash", script_path_postinstall, username, self.dest_dir, self.desktop,
                                   keyboard_layout, keyboard_variant], timeout=300)
            logging.debug(_("Post install script completed successfully."))
        except subprocess.CalledProcessError as err:
            logging.error(err.output)
        except subprocess.TimeoutExpired as err:
            logging.error(err)

        if desktop != "nox":
            # Set lightdm config including autologin if selected
            self.set_display_manager()

        # Configure user features (third party software, libreoffice language pack, ...)
        self.setup_features()

        # Encrypt user's home directory if requested
        # TODO: Test this!
        if self.settings.get('encrypt_home'):
            logging.debug(_("Encrypting user home dir..."))
            encfs.setup(username, self.dest_dir)
            logging.debug(_("User home dir encrypted"))

        # Install boot loader (always after running mkinitcpio)
        if self.settings.get('install_bootloader'):
            logging.debug(_("Installing bootloader..."))
            self.install_bootloader()

        # Copy installer log to the new installation (just in case something goes wrong)
        logging.debug(_("Copying install log to /var/log."))
        self.copy_log()

        self.queue_event('pulse', 'stop')

