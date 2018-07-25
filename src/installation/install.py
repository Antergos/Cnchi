#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# install.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

""" Installation process module. """

import glob
import logging
import os
import queue
import shutil
import sys

from mako.template import Template

from download import download

from installation import auto_partition
from installation import special_dirs

from installation import post_install

import misc.extra as misc
from misc.extra import InstallError
from misc.run_cmd import call

import pacman.pac as pac

import hardware.hardware as hardware

DEST_DIR = "/install"

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

class Installation():
    """ Installation process thread class """

    def __init__(self, settings, callback_queue, packages, metalinks,
                 mount_devices, fs_devices, ssd=None, blvm=False):
        """ Initialize installation class """

        self.settings = settings
        self.callback_queue = callback_queue
        self.packages = packages
        self.metalinks = metalinks

        self.method = self.settings.get('partition_mode')

        self.desktop = self.settings.get('desktop').lower()

        # This flag tells us if there is a lvm partition (from advanced install)
        # If it's true we'll have to add the 'lvm2' hook to mkinitcpio
        self.blvm = blvm

        if ssd is not None:
            self.ssd = ssd
        else:
            self.ssd = {}

        self.mount_devices = mount_devices

        self.fs_devices = fs_devices

        self.running = True
        self.error = False

        self.auto_device = ""
        self.packages = packages
        self.pacman = None

        self.pacman_cache_dir = ''

        # Cnchi will store here info (packages needed, post install actions, ...)
        # for the detected hardware
        self.hardware_install = None

    def queue_fatal_event(self, txt):
        """ Queues the fatal event and exits process """
        self.error = True
        self.running = False
        self.queue_event('error', txt)
        # self.callback_queue.join()
        sys.exit(0)

    def queue_event(self, event_type, event_text=""):
        """ Enqueue a new event """
        if self.callback_queue:
            try:
                self.callback_queue.put_nowait((event_type, event_text))
            except queue.Full:
                pass

    def mount_partitions(self):
        """ Do not call this in automatic mode as AutoPartition class mounts
        the root and boot devices itself. (We call it if using ZFS, though) """

        if os.path.exists(DEST_DIR) and not self.method == "zfs":
            # If we're recovering from a failed/stoped install, there'll be
            # some mounted directories. Try to unmount them first.
            # We use unmount_all_in_directory from auto_partition to do this.
            # ZFS already mounts everything automagically (except /boot that
            # is not in zfs)
            auto_partition.unmount_all_in_directory(DEST_DIR)

        # NOTE: Advanced method formats root by default in advanced.py
        if "/" in self.mount_devices:
            root_partition = self.mount_devices["/"]
        else:
            root_partition = ""

        # Boot partition
        if "/boot" in self.mount_devices:
            boot_partition = self.mount_devices["/boot"]
        else:
            boot_partition = ""

        # EFI partition
        if "/boot/efi" in self.mount_devices:
            efi_partition = self.mount_devices["/boot/efi"]
        else:
            efi_partition = ""

        # Swap partition
        if "swap" in self.mount_devices:
            swap_partition = self.mount_devices["swap"]
        else:
            swap_partition = ""

        # Mount root partition
        if self.method == "zfs":
            # Mount /
            logging.debug("ZFS: Mounting root")
            cmd = ["zfs", "mount", "-a"]
            call(cmd)
        elif root_partition:
            txt = "Mounting root partition {0} into {1} directory".format(
                root_partition, DEST_DIR)
            logging.debug(txt)
            cmd = ['mount', root_partition, DEST_DIR]
            call(cmd, fatal=True)

        # We also mount the boot partition if it's needed
        boot_path = os.path.join(DEST_DIR, "boot")
        os.makedirs(boot_path, mode=0o755, exist_ok=True)
        if boot_partition:
            txt = _("Mounting boot partition {0} into {1} directory").format(
                boot_partition, boot_path)
            logging.debug(txt)
            cmd = ['mount', boot_partition, boot_path]
            call(cmd, fatal=True)

        if self.method == "zfs" and efi_partition:
            # In automatic zfs mode, it could be that we have a specific EFI
            # partition (different from /boot partition). This happens if using
            # EFI and grub2 bootloader
            efi_path = os.path.join(DEST_DIR, "boot", "efi")
            os.makedirs(efi_path, mode=0o755, exist_ok=True)
            txt = _("Mounting EFI partition {0} into {1} directory").format(
                efi_partition, efi_path)
            logging.debug(txt)
            cmd = ['mount', efi_partition, efi_path]
            call(cmd, fatal=True)

        # In advanced mode, mount all partitions (root and boot are already mounted)
        if self.method == 'advanced':
            for path in self.mount_devices:
                if path == "":
                    # Ignore devices without a mount path
                    continue

                mount_part = self.mount_devices[path]

                if mount_part not in [root_partition, boot_partition, swap_partition]:
                    if path[0] == '/':
                        path = path[1:]
                    mount_dir = os.path.join(DEST_DIR, path)
                    try:
                        os.makedirs(mount_dir, mode=0o755, exist_ok=True)
                        txt = _("Mounting partition {0} into {1} directory")
                        txt = txt.format(mount_part, mount_dir)
                        logging.debug(txt)
                        cmd = ['mount', mount_part, mount_dir]
                        call(cmd)
                    except OSError:
                        logging.warning(
                            "Could not create %s directory", mount_dir)
                elif mount_part == swap_partition:
                    logging.debug("Activating swap in %s", mount_part)
                    cmd = ['swapon', swap_partition]
                    call(cmd)

    @misc.raise_privileges
    def start(self):
        """ Run installation """

        # From this point, on a warning situation, Cnchi should try to continue,
        # so we need to catch the exception here. If we don't catch the exception
        # here, it will be catched in run() and managed as a fatal error.
        # On the other hand, if we want to clarify the exception message we can
        # catch it here and then raise an InstallError exception.

        if not os.path.exists(DEST_DIR):
            os.makedirs(DEST_DIR, mode=0o755, exist_ok=True)

        # Make sure the antergos-repo-priority package's alpm hook doesn't run.
        if not os.environ.get('CNCHI_RUNNING', False):
            os.environ['CNCHI_RUNNING'] = 'True'

        msg = _("Installing using the '{0}' method").format(self.method)
        self.queue_event('info', msg)

        # Mount needed partitions (in automatic it's already done)
        if self.method in ['alongside', 'advanced', 'zfs']:
            self.mount_partitions()

        # Nasty workaround:
        # If pacman was stoped and /var is in another partition than root
        # (so as to be able to resume install), database lock file will still
        # be in place. We must delete it or this new installation will fail
        db_lock = os.path.join(DEST_DIR, "var/lib/pacman/db.lck")
        if os.path.exists(db_lock):
            os.remove(db_lock)
            logging.debug("%s deleted", db_lock)

        # Create some needed folders
        folders = [
            os.path.join(DEST_DIR, 'var/lib/pacman'),
            os.path.join(DEST_DIR, 'etc/pacman.d/gnupg'),
            os.path.join(DEST_DIR, 'var/log')]

        for folder in folders:
            os.makedirs(folder, mode=0o755, exist_ok=True)

        # If kernel images exists in /boot they are most likely from a failed
        # install attempt and need to be removed otherwise pyalpm will raise a
        # fatal exception later on.
        kernel_imgs = (
            "/install/boot/vmlinuz-linux",
            "/install/boot/vmlinuz-linux-lts",
            "/install/boot/initramfs-linux.img",
            "/install/boot/initramfs-linux-fallback.img",
            "/install/boot/initramfs-linux-lts.img",
            "/install/boot/initramfs-linux-lts-fallback.img")

        for img in kernel_imgs:
            if os.path.exists(img):
                os.remove(img)

        # If intel-ucode or grub2-theme-antergos files exist in /boot they are
        # most likely either from another linux installation or from a failed
        # install attempt and need to be removed otherwise pyalpm will refuse
        # to install those packages (like above)
        if os.path.exists('/install/boot/intel-ucode.img'):
            logging.debug("Removing previous intel-ucode.img file found in /boot")
            os.remove('/install/boot/intel-ucode.img')
        if os.path.exists('/install/boot/grub/themes/Antergos-Default'):
            logging.debug("Removing previous Antergos-Default grub2 theme found in /boot")
            shutil.rmtree('/install/boot/grub/themes/Antergos-Default')

        logging.debug("Preparing pacman...")
        self.prepare_pacman()
        logging.debug("Pacman ready")

        # Run driver's pre-install scripts
        try:
            logging.debug("Running hardware drivers pre-install jobs...")
            proprietary = self.settings.get('feature_graphic_drivers')
            self.hardware_install = hardware.HardwareInstall(
                self.settings.get("cnchi"),
                use_proprietary_graphic_drivers=proprietary)
            self.hardware_install.pre_install(DEST_DIR)
        except Exception as ex:
            template = "Error in hardware module. " \
                       "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)

        logging.debug("Downloading packages...")
        self.download_packages()

        # This mounts (binds) /dev and others to /DEST_DIR/dev and others
        special_dirs.mount(DEST_DIR)

        logging.debug("Installing packages...")
        self.install_packages()

        logging.debug("Configuring system...")
        post = post_install.PostInstallation(
            self.settings,
            self.callback_queue,
            self.mount_devices,
            self.fs_devices,
            self.ssd,
            self.blvm)
        post.configure_system(self.hardware_install)

        # This unmounts (unbinds) /dev and others to /DEST_DIR/dev and others
        special_dirs.umount(DEST_DIR)

        # Run postinstall script (we need special dirs unmounted but dest_dir mounted!)
        logging.debug("Running postinstall.sh script...")
        post.set_desktop_settings()

        # Copy installer log to the new installation
        logging.debug("Copying install log to /var/log.")
        post.copy_logs()

        self.queue_event('pulse', 'stop')
        self.queue_event('progress_bar', 'hide')

        # Finally, try to unmount DEST_DIR
        auto_partition.unmount_all_in_directory(DEST_DIR)

        self.running = False

        # Installation finished successfully
        self.queue_event('finished', _("Installation finished"))
        self.error = False
        return True

    def download_packages(self):
        """ Downloads necessary packages """

        self.pacman_cache_dir = os.path.join(DEST_DIR, 'var/cache/pacman/pkg')

        pacman_conf = {}
        pacman_conf['file'] = '/tmp/pacman.conf'
        pacman_conf['cache'] = self.pacman_cache_dir

        download_packages = download.DownloadPackages(
            package_names=self.packages,
            pacman_conf=pacman_conf,
            settings=self.settings,
            callback_queue=self.callback_queue)

        # Metalinks have already been calculated before,
        # When downloadpackages class has been called in process.py to test
        # that Cnchi was able to create it before partitioning/formatting
        download_packages.start(self.metalinks)

    def create_pacman_conf_file(self):
        """ Creates a temporary pacman.conf """
        myarch = os.uname()[-1]
        msg = _("Creating a temporary pacman.conf for {0} architecture").format(
            myarch)
        logging.debug(msg)

        # Template functionality. Needs Mako (see http://www.makotemplates.org/)
        template_file_name = os.path.join(
            self.settings.get('data'), 'pacman.tmpl')
        file_template = Template(filename=template_file_name)
        file_rendered = file_template.render(
            destDir=DEST_DIR,
            arch=myarch,
            desktop=self.desktop)
        filename = os.path.join("/tmp", "pacman.conf")
        os.makedirs(os.path.dirname(filename), mode=0o755, exist_ok=True)
        with open(filename, "w") as my_file:
            my_file.write(file_rendered)


    def prepare_pacman(self):
        """ Configures pacman and syncs db on destination system """

        self.create_pacman_conf_file()

        msg = _("Updating package manager security. Please wait...")
        self.queue_event('info', msg)
        self.prepare_pacman_keyring()

        # Init pyalpm
        try:
            self.pacman = pac.Pac("/tmp/pacman.conf", self.callback_queue)
        except Exception as ex:
            self.pacman = None
            template = ("Can't initialize pyalpm. "
                        "An exception of type {0} occured. Arguments:\n{1!r}")
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            raise InstallError(message)

        # Refresh pacman databases
        if not self.pacman.refresh():
            logging.error("Can't refresh pacman databases.")
            raise InstallError(_("Can't refresh pacman databases."))

    @staticmethod
    def prepare_pacman_keyring():
        """ Add gnupg pacman files to installed system """

        dirs = ["var/cache/pacman/pkg", "var/lib/pacman"]
        for pacman_dir in dirs:
            mydir = os.path.join(DEST_DIR, pacman_dir)
            os.makedirs(mydir, mode=0o755, exist_ok=True)

        # Be sure that haveged is running (liveCD)
        # haveged is a daemon that generates system entropy; this speeds up
        # critical operations in cryptographic programs such as gnupg
        # (including the generation of new keyrings)
        cmd = ["systemctl", "start", "haveged"]
        call(cmd)

        # Delete old gnupg files
        dest_path = os.path.join(DEST_DIR, "etc/pacman.d/gnupg")
        cmd = ["rm", "-rf", dest_path]
        call(cmd)
        os.mkdir(dest_path)

        # Tell pacman-key to regenerate gnupg files
        # Initialize the pacman keyring
        cmd = ["pacman-key", "--init", "--gpgdir", dest_path]
        call(cmd)

        # Load the signature keys
        cmd = ["pacman-key", "--populate", "--gpgdir",
               dest_path, "archlinux", "antergos"]
        call(cmd)

        # path = os.path.join(DEST_DIR, "root/.gnupg/dirmngr_ldapservers.conf")
        # Run dirmngr
        # https://bbs.archlinux.org/viewtopic.php?id=190380
        with open(os.devnull, 'r') as dev_null:
            cmd = ["dirmngr"]
            call(cmd, stdin=dev_null)

        # Refresh and update the signature keys
        # cmd = ["pacman-key", "--refresh-keys", "--gpgdir", dest_path]
        # call(cmd)

    def install_packages(self):
        """ Start pacman installation of packages """
        result = False
        # This shouldn't be necessary if download.py really downloaded all
        # needed packages, but it does not do it (why?)
        for cache_dir in self.settings.get('xz_cache'):
            self.pacman.handle.add_cachedir(cache_dir)

        logging.debug("Installing packages...")

        try:
            result = self.pacman.install(
                pkgs=self.packages, conflicts=None, options=None)
        except pac.pyalpm.error:
            pass

        stale_pkgs = self.settings.get('cache_pkgs_md5_check_failed')

        if not result and stale_pkgs:
            # Failure might be due to stale cached packages. Delete them and try again.
            if os.path.exists(self.pacman_cache_dir):
                for stale_pkg in stale_pkgs:
                    filepath = os.path.join(self.pacman_cache_dir, stale_pkg)
                    to_delete = glob.glob(filepath + '***') if filepath else []
                    if to_delete and len(to_delete) <= 20:
                        for fpath in to_delete:
                            try:
                                os.remove(fpath)
                            except Exception as err:
                                logging.error(err)

                self.pacman.refresh()

                result = self.pacman.install(pkgs=self.packages)

        elif not result and self.settings.get('desktop').lower() in ['cinnamon', 'mate']:
            # Failure might be due to antergos mirror issues. Try using build server repo.
            with open('/etc/pacman.conf', 'r') as pacman_conf:
                contents = pacman_conf.readlines()

            with open('/etc/pacman.conf', 'w') as new_pacman_conf:
                for line in contents:
                    if 'antergos-mirrorlist' in line:
                        line = 'Server = http://repo.antergos.info/$repo/$arch'
                    new_pacman_conf.write(line)

            self.pacman.refresh()

            result = self.pacman.install(pkgs=self.packages)

        if not result:
            txt = _("Can't install necessary packages. Cnchi can't continue.")
            raise InstallError(txt)

        # All downloading and installing has been done, so we hide progress bar
        self.queue_event('progress_bar', 'hide')

    def is_running(self):
        """ Checks if thread is running """
        return self.running

    def is_ok(self):
        """ Checks if an error has been issued """
        return not self.error
