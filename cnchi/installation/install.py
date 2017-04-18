#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# installation.py
#
# Copyright © 2013-2016 Antergos
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

import crypt
import glob
import logging
import os
import queue
import shutil
import sys
import time
import re
import tempfile

import desktop_info
import encfs

from download import download

from installation import auto_partition
from installation import special_dirs
from installation import mkinitcpio
from installation import firewall

from misc.extra import InstallError
from misc.run_cmd import call, chroot_call

import parted3.fs_module as fs
import misc.extra as misc
import pacman.pac as pac

from mako.template import Template

import hardware.hardware as hardware

from installation.boot import loader

POSTINSTALL_SCRIPT = 'postinstall.sh'
DEST_DIR = "/install"

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


def write_file(filecontents, filename):
    """ writes a string of data to disk """
    os.makedirs(os.path.dirname(filename), mode=0o755, exist_ok=True)

    with open(filename, "w") as my_file:
        my_file.write(filecontents)


class Installation(object):
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
        self.vbox = self.settings.get('is_vbox')
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
            txt = "Mounting root partition {0} into {1} directory".format(root_partition, DEST_DIR)
            logging.debug(txt)
            cmd = ['mount', root_partition, DEST_DIR]
            call(cmd, fatal=True)

        # We also mount the boot partition if it's needed
        boot_path = os.path.join(DEST_DIR, "boot")
        os.makedirs(boot_path, mode=0o755, exist_ok=True)
        if boot_partition:
            txt = _("Mounting boot partition {0} into {1} directory").format(boot_partition, boot_path)
            logging.debug(txt)
            cmd = ['mount', boot_partition, boot_path]
            call(cmd, fatal=True)

        if self.method == "zfs" and efi_partition:
            # In automatic zfs mode, it could be that we have a specific EFI
            # partition (different from /boot partition). This happens if using
            # EFI and grub2 bootloader
            efi_path = os.path.join(DEST_DIR, "boot", "efi")
            os.makedirs(efi_path, mode=0o755, exist_ok=True)
            txt = _("Mounting EFI partition {0} into {1} directory").format(efi_partition, efi_path)
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
                        logging.warning("Could not create %s directory", mount_dir)
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

        logging.debug("Preparing pacman...")
        self.prepare_pacman()
        logging.debug("Pacman ready")

        # Run pre-install scripts (only catalyst does something here atm)
        # Note: Catalyst is disabled in catalyst.py
        try:
            logging.debug("Running hardware drivers pre-install jobs...")
            proprietary = self.settings.get('feature_graphic_drivers')
            self.hardware_install = hardware.HardwareInstall(
                use_proprietary_graphic_drivers=proprietary)
            self.hardware_install.pre_install(DEST_DIR)
        except Exception as ex:
            template = "Error in hardware module. An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)

        logging.debug("Downloading packages...")
        self.download_packages()

        # This mounts (binds) /dev and others to /DEST_DIR/dev and others
        special_dirs.mount(DEST_DIR)

        logging.debug("Installing packages...")
        self.install_packages()

        logging.debug("Configuring system...")
        self.configure_system()

        # This unmounts (unbinds) /dev and others to /DEST_DIR/dev and others
        special_dirs.umount(DEST_DIR)

        # Run postinstall script (we need special dirs unmounted but dest_dir mounted!)
        logging.debug("Running postinstall.sh script...")
        self.set_desktop_settings()

        # Copy installer log to the new installation
        logging.debug("Copying install log to /var/log.")
        self.copy_log()

        self.queue_event('pulse', 'stop')
        self.queue_event('progress_bar', 'hide')

        # Finally, try to unmount DEST_DIR
        auto_partition.unmount_all_in_directory(DEST_DIR)

        self.running = False

        # Installation finished successfully
        self.queue_event('finished', _("Installation finished"))
        self.error = False
        return True

    def copy_log(self):
        """ Copy Cnchi logs to new installation """
        log_dest_dir = os.path.join(DEST_DIR, "var/log/cnchi")
        os.makedirs(log_dest_dir, mode=0o755, exist_ok=True)

        datetime = "{0}-{1}".format(time.strftime("%Y%m%d"), time.strftime("%H%M%S"))

        file_names = ["cnchi", "postinstall", "pacman"]

        for name in file_names:
            src = os.path.join("/tmp", "{0}.log".format(name))
            dst = os.path.join(log_dest_dir, "{0}-{1}.log".format(name, datetime))
            try:
                shutil.copy(src, dst)
            except FileNotFoundError:
                logging.warning("Can't copy %s log to %s", src, dst)
            except FileExistsError:
                pass

        # Store install id for later use by antergos-pkgstats
        with open(os.path.join(log_dest_dir, 'install_id'), 'w') as install_record:
            install_id = self.settings.get('install_id')
            if not install_id:
                install_id = '0'
            install_record.write(install_id)

    def download_packages(self):
        """ Downloads necessary packages """

        self.pacman_cache_dir = os.path.join(DEST_DIR, 'var/cache/pacman/pkg')

        download_packages = download.DownloadPackages(
            package_names=self.packages,
            pacman_conf_file='/tmp/pacman.conf',
            pacman_cache_dir=self.pacman_cache_dir,
            settings=self.settings,
            callback_queue=self.callback_queue)

        # Metalinks have already been calculated before,
        # When downloadpackages class has been called in process.py to test
        # that Cnchi was able to create it before partitioning/formatting
        download_packages.start(self.metalinks)

    def create_pacman_conf_file(self):
        """ Creates a temporary pacman.conf """
        myarch = os.uname()[-1]
        msg = _("Creating a temporary pacman.conf for {0} architecture").format(myarch)
        logging.debug(msg)

        # Template functionality. Needs Mako (see http://www.makotemplates.org/)
        template_file_name = os.path.join(self.settings.get('data'), 'pacman.tmpl')
        file_template = Template(filename=template_file_name)
        file_rendered = file_template.render(
            destDir=DEST_DIR,
            arch=myarch,
            desktop=self.desktop)
        write_file(file_rendered, os.path.join("/tmp", "pacman.conf"))

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
            template = "Can't initialize pyalpm. An exception of type {0} occured. Arguments:\n{1!r}"
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
        cmd = ["pacman-key", "--populate", "--gpgdir", dest_path, "archlinux", "antergos"]
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
            result = self.pacman.install(pkgs=self.packages, conflicts=None, options=None)
        except pac.pyalpm.error:
            pass

        stale_pkgs = self.settings.get('cache_pkgs_md5_check_failed')

        if not result and stale_pkgs and len(stale_pkgs) > 0:
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

    @staticmethod
    def copy_network_config():
        """ Copies Network Manager configuration """
        source_nm = "/etc/NetworkManager/system-connections/"
        target_nm = os.path.join(DEST_DIR, "etc/NetworkManager/system-connections")

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
                    logging.warning("Can't copy network configuration files, file %s not found", source_network)
                except FileExistsError:
                    pass

    def auto_fstab(self):
        """ Create /etc/fstab file """

        all_lines = [
            "# /etc/fstab: static file system information.",
            "#",
            "# Use 'blkid' to print the universally unique identifier for a",
            "# device; this may be used with UUID= as a more robust way to name devices",
            "# that works even if disks are added and removed. See fstab(5).",
            "#",
            "# <file system> <mount point>   <type>  <options>       <dump>  <pass>",
            "#"]

        use_luks = self.settings.get("use_luks")
        use_lvm = self.settings.get("use_lvm")

        # Use lsblk to be able to match LUKS UUID with mapper UUID
        pknames = fs.get_pknames()

        for mount_point in self.mount_devices:
            partition_path = self.mount_devices[mount_point]
            uuid = fs.get_uuid(partition_path)
            if uuid == "":
                logging.warning(
                    "Can't get %s partition UUID. It won't be added to fstab",
                    partition_path)
                continue

            if partition_path in self.fs_devices:
                myfmt = self.fs_devices[partition_path]
            else:
                # It hasn't any filesystem defined, skip it.
                continue

            # Take care of swap partitions
            if "swap" in myfmt:
                # If using a TRIM supported SSD, discard is a valid mount
                # option for swap
                if partition_path in self.ssd:
                    opts = "defaults,discard"
                else:
                    opts = "defaults"

                if self.settings.get("zfs"):
                    # We can't use UUID with zfs, so we will use device name
                    txt = "{0} swap swap {1} 0 0".format(partition_path, opts)
                else:
                    txt = "UUID={0} swap swap {1} 0 0".format(uuid, opts)

                all_lines.append(txt)
                logging.debug("Added %s to fstab", txt)
                continue

            crypttab_path = os.path.join(DEST_DIR, 'etc/crypttab')

            # Fix for home + luks, no lvm (from Automatic Install)
            if ("/home" in mount_point and
                    self.method == "automatic" and
                    use_luks and
                    not use_lvm):
                # Modify the crypttab file
                luks_root_password = self.settings.get("luks_root_password")
                if luks_root_password and len(luks_root_password) > 0:
                    # Use password and not a keyfile
                    home_keyfile = "none"
                else:
                    # Use a keyfile
                    home_keyfile = "/etc/luks-keys/home"

                os.chmod(crypttab_path, 0o666)
                with open(crypttab_path, 'a') as crypttab_file:
                    line = "cryptAntergosHome /dev/disk/by-uuid/{0} {1} luks\n".format(uuid, home_keyfile)
                    crypttab_file.write(line)
                    logging.debug("Added %s to crypttab", line)
                os.chmod(crypttab_path, 0o600)

                # Add line to fstab
                txt = "/dev/mapper/cryptAntergosHome {0} {1} defaults 0 0".format(mount_point, myfmt)
                all_lines.append(txt)
                logging.debug("Added %s to fstab", txt)
                continue

            # Add all LUKS partitions from Advanced Install (except root).
            if (self.method == "advanced" and
                    mount_point is not "/" and
                    use_luks and
                    "/dev/mapper" in partition_path):
                # As the mapper with the filesystem will have a different UUID
                # than the partition it is encrypted in, we have to take care
                # of this here. Then we will be able to add it to crypttab

                vol_name = partition_path[len("/dev/mapper/"):]
                try:
                    luks_partition_path = "/dev/" + pknames[vol_name]
                except KeyError:
                    logging.error(
                        "Can't find the PKNAME value of %s",
                        partition_path)
                    continue

                luks_uuid = fs.get_uuid(luks_partition_path)

                if len(luks_uuid) > 0:
                    # OK, add it to crypttab with the correct uuid
                    os.chmod(crypttab_path, 0o666)
                    with open(crypttab_path, 'a') as crypttab_file:
                        line = "{0} /dev/disk/by-uuid/{1} none luks\n"
                        line = line.format(vol_name, luks_uuid)
                        crypttab_file.write(line)
                        logging.debug("Added %s to crypttab", line)
                    os.chmod(crypttab_path, 0o600)
                else:
                    logging.error(
                        "Can't add luks uuid to crypttab for %s partition",
                        luks_partition_path)
                    continue

                # Finally, the fstab line to mount the unencrypted file system
                # if a mount point has been specified by the user
                if len(mount_point) > 0:
                    txt = "{0} {1} {2} defaults 0 0"
                    txt = txt.format(partition_path, mount_point, myfmt)
                    all_lines.append(txt)
                    logging.debug("Added %s to fstab", txt)
                continue

            # fstab uses vfat to mount fat16 and fat32 partitions
            if "fat" in myfmt:
                myfmt = 'vfat'

            if "btrfs" in myfmt:
                self.settings.set('btrfs', True)

            # Avoid adding a partition to fstab when it has no mount point
            # (swap has been checked above)
            if mount_point == "":
                continue

            # Create mount point on destination system if it yet doesn't exist
            full_path = os.path.join(DEST_DIR, mount_point)
            os.makedirs(full_path, mode=0o755, exist_ok=True)

            # Is ssd ?
            # Device list example: {'/dev/sdb': False, '/dev/sda': True}

            txt = "Device list : {0}".format(self.ssd)
            logging.debug(txt)
            device = re.sub("[0-9]+$", "", partition_path)
            is_ssd = self.ssd.get(device)
            txt = "Device: {0}, SSD: {1}".format(device, is_ssd)
            logging.debug(txt)

            # Add mount options parameters
            if not is_ssd:
                if "btrfs" in myfmt:
                    opts = "defaults,relatime,space_cache,autodefrag,inode_cache"
                elif "f2fs" in myfmt:
                    opts = "defaults,noatime"
                elif "ext3" in myfmt or "ext4" in myfmt:
                    opts = "defaults,relatime,data=ordered"
                else:
                    opts = "defaults,relatime"
            else:
                # As of linux kernel version 3.7, the following
                # filesystems support TRIM: ext4, btrfs, JFS, and XFS.
                if myfmt in ["ext4", "jfs", "xfs"]:
                    opts = "defaults,noatime,discard"
                elif myfmt == "btrfs":
                    opts = ("defaults,noatime,compress=lzo,ssd,discard,"
                            "space_cache,autodefrag,inode_cache")
                else:
                    opts = "defaults,noatime"

            if mount_point == "/" and myfmt not in ["btrfs", "f2fs"]:
                chk = '1'
            else:
                chk = '0'

            if mount_point == "/":
                self.settings.set('ruuid', uuid)

            txt = "UUID={0} {1} {2} {3} 0 {4}"
            txt = txt.format(uuid, mount_point, myfmt, opts, chk)
            all_lines.append(txt)
            logging.debug("Added %s to fstab", txt)

        full_text = '\n'.join(all_lines) + '\n'

        fstab_path = os.path.join(DEST_DIR, 'etc/fstab')
        with open(fstab_path, 'w') as fstab_file:
            fstab_file.write(full_text)

        logging.debug("fstab written.")

    def set_scheduler(self):
        rule_src = os.path.join(
            self.settings.get('cnchi'),
            'scripts/60-schedulers.rules')
        rule_dst = os.path.join(
            DEST_DIR,
            "etc/udev/rules.d/60-schedulers.rules")
        try:
            shutil.copy2(rule_src, rule_dst)
            os.chmod(rule_dst, 0o755)
        except FileNotFoundError:
            logging.warning(
                "Cannot copy udev rule for SSDs, file %s not found.",
                rule_src)
        except FileExistsError:
            pass

    @staticmethod
    def enable_services(services):
        """ Enables all services that are in the list 'services' """
        for name in services:
            path = os.path.join(
                DEST_DIR,
                "usr/lib/systemd/system/{0}.service".format(name))
            if os.path.exists(path):
                chroot_call(['systemctl', '-fq', 'enable', name])
                logging.debug("Service '%s' has been enabled.", name)
            else:
                logging.warning("Can't find service %s", name)

    @staticmethod
    def change_user_password(user, new_password):
        """ Changes the user's password """
        shadow_password = crypt.crypt(new_password, "$6${0}$".format(user))
        chroot_call(['usermod', '-p', shadow_password, user])

    @staticmethod
    def auto_timesetting():
        """ Set hardware clock """
        cmd = ["hwclock", "--systohc", "--utc"]
        call(cmd)
        shutil.copy2("/etc/adjtime", os.path.join(DEST_DIR, "etc/"))

    @staticmethod
    def update_pacman_conf():
        """ Add Antergos and multilib repos """
        path = os.path.join(DEST_DIR, "etc/pacman.conf")
        if os.path.exists(path):
            with open(path) as pacman_file:
                paclines = pacman_file.readlines()

            mode = os.uname()[-1]
            multilib_open = False

            with open(path, 'w') as pacman_file:
                for pacline in paclines:
                    if mode == "x86_64" and pacline == '#[multilib]\n':
                        multilib_open = True
                        pacline = '[multilib]\n'
                    elif mode == 'x86_64' and multilib_open and pacline.startswith('#Include ='):
                        pacline = pacline[1:]
                        multilib_open = False
                    elif pacline == '#[testing]\n':
                        antlines = '\n#[antergos-staging]\n'
                        antlines += '#SigLevel = PackageRequired\n'
                        antlines += '#Server = http://mirrors.antergos.com/$repo/$arch/\n\n'
                        antlines += '[antergos]\n'
                        antlines += 'SigLevel = PackageRequired\n'
                        antlines += 'Include = /etc/pacman.d/antergos-mirrorlist\n\n'

                        pacman_file.write(antlines)

                    pacman_file.write(pacline)
        else:
            logging.warning("Can't find pacman configuration file")

    @staticmethod
    def uncomment_locale_gen(locale):
        """ Uncomment selected locale in /etc/locale.gen """

        path = os.path.join(DEST_DIR, "etc/locale.gen")

        if os.path.exists(path):
            with open(path) as gen:
                text = gen.readlines()

            with open(path, "w") as gen:
                for line in text:
                    if locale in line and line[0] == "#":
                        # remove trailing '#'
                        line = line[1:]
                    gen.write(line)
        else:
            logging.error("Can't find locale.gen file")


    def enable_aur_in_pamac(self):
        pamac_conf = "/etc/pamac.conf"
        if os.path.exists(pamac_conf):
            fd, name = tempfile.mkstemp()
            fout = open(name, 'w')
            with open(pamac_conf) as fin:
                for line in fin:
                    if line.startswith("#"):
                        if "EnableAUR" in line:
                            line = "EnableAUR\n"
                        elif "SearchInAURByDefault" in line:
                            line = "SearchInAURByDefault\n"
                        elif "CheckAURUpdates" in line:
                            line = "CheckAURUpdates\n"
                    fout.write(line)
            fout.close()
            shutil.move(name, pamac_conf)
            logging.debug("Enabled AUR in %s file", pamac_conf)
        else:
            logging.warning("Cannot find %s file", pamac_conf)

    def setup_features(self):
        """ Do all set up needed by the user's selected features """
        services = []

        if self.settings.get("feature_aur"):
            self.enable_aur_in_pamac()

        if self.settings.get("feature_bluetooth"):
            services.append('bluetooth')

        if self.settings.get("feature_cups"):
            services.append('org.cups.cupsd')
            services.append('avahi-daemon')

        if self.settings.get("feature_firewall"):
            logging.debug("Configuring firewall...")
            # Set firewall rules
            firewall.run(["default", "deny"])
            toallow = misc.get_network()
            if toallow:
                firewall.run(["allow", "from", toallow])
            firewall.run(["allow", "Transmission"])
            firewall.run(["allow", "SSH"])
            firewall.run(["enable"])
            services.append('ufw')

        if (self.settings.get("feature_lamp") and
                not self.settings.get("feature_lemp")):
            try:
                from installation import lamp
                logging.debug("Configuring LAMP...")
                lamp.setup()
                services.extend(["httpd", "mysqld"])
            except ImportError as import_error:
                logging.warning(
                    "Unable to import LAMP module: %s",
                    str(import_error))
        elif self.settings.get("feature_lemp"):
            try:
                from installation import lemp
                logging.debug("Configuring LEMP...")
                lemp.setup()
                services.extend(["nginx", "mysqld", "php-fpm"])
            except ImportError as import_error:
                logging.warning(
                    "Unable to import LEMP module: %s",
                    str(import_error))

        self.enable_services(services)

    def setup_display_manager(self):
        """ Configures LightDM desktop manager, including autologin. """
        txt = _("Configuring LightDM desktop manager...")
        self.queue_event('info', txt)

        if self.desktop in desktop_info.SESSIONS:
            session = desktop_info.SESSIONS[self.desktop]
        else:
            session = "default"

        username = self.settings.get('username')
        autologin = not self.settings.get('require_password')

        lightdm_greeter = "lightdm-webkit2-greeter"

        lightdm_conf_path = os.path.join(DEST_DIR, "etc/lightdm/lightdm.conf")
        try:
            # Setup LightDM as Desktop Manager
            with open(lightdm_conf_path) as lightdm_conf:
                text = lightdm_conf.readlines()

            with open(lightdm_conf_path, "w") as lightdm_conf:
                for line in text:
                    if autologin:
                        # Enable automatic login
                        if '#autologin-user=' in line:
                            line = 'autologin-user={0}\n'.format(username)
                        if '#autologin-user-timeout=0' in line:
                            line = 'autologin-user-timeout=0\n'
                    # Set correct DE session
                    if '#user-session=default' in line:
                        line = 'user-session={0}\n'.format(session)
                    # Set correct greeter
                    if '#greeter-session=example-gtk-gnome' in line:
                        line = 'greeter-session={0}\n'.format(lightdm_greeter)
                    if 'session-wrapper' in line:
                        line = 'session-wrapper=/etc/lightdm/Xsession\n'
                    lightdm_conf.write(line)
            txt = _("LightDM display manager configuration completed.")
            logging.debug(txt)
        except FileNotFoundError:
            txt = _("Error while trying to configure the LightDM display manager")
            logging.warning(txt)

    @staticmethod
    def alsa_mixer_setup():
        """ Sets ALSA mixer settings """

        alsa_commands = [
            "Master 70% unmute",
            "Front 70% unmute"
            "Side 70% unmute"
            "Surround 70% unmute",
            "Center 70% unmute",
            "LFE 70% unmute",
            "Headphone 70% unmute",
            "Speaker 70% unmute",
            "PCM 70% unmute",
            "Line 70% unmute",
            "External 70% unmute",
            "FM 50% unmute",
            "Master Mono 70% unmute",
            "Master Digital 70% unmute",
            "Analog Mix 70% unmute",
            "Aux 70% unmute",
            "Aux2 70% unmute",
            "PCM Center 70% unmute",
            "PCM Front 70% unmute",
            "PCM LFE 70% unmute",
            "PCM Side 70% unmute",
            "PCM Surround 70% unmute",
            "Playback 70% unmute",
            "PCM,1 70% unmute",
            "DAC 70% unmute",
            "DAC,0 70% unmute",
            "DAC,1 70% unmute",
            "Synth 70% unmute",
            "CD 70% unmute",
            "Wave 70% unmute",
            "Music 70% unmute",
            "AC97 70% unmute",
            "Analog Front 70% unmute",
            "VIA DXS,0 70% unmute",
            "VIA DXS,1 70% unmute",
            "VIA DXS,2 70% unmute",
            "VIA DXS,3 70% unmute",
            "Mic 70% mute",
            "IEC958 70% mute",
            "Master Playback Switch on",
            "Master Surround on",
            "SB Live Analog/Digital Output Jack off",
            "Audigy Analog/Digital Output Jack off"]

        for alsa_command in alsa_commands:
            cmd = ["amixer", "-q", "-c", "0", "sset"]
            cmd.extend(alsa_command.split())
            chroot_call(cmd)

        # Save settings
        logging.debug("Saving ALSA settings...")
        chroot_call(['alsactl', 'store'])
        logging.debug("ALSA settings saved.")

    @staticmethod
    def set_fluidsynth():
        """ Sets fluidsynth configuration file """

        fluid_path = os.path.join(DEST_DIR, "etc/conf.d/fluidsynth")

        if not os.path.exists(fluid_path):
            return

        audio_system = "alsa"

        pulseaudio_path = os.path.join(DEST_DIR, "usr/bin/pulseaudio")
        if os.path.exists(pulseaudio_path):
            audio_system = "pulse"

        with open(fluid_path, "w") as fluid_conf:
            fluid_conf.write('# Created by Cnchi, Antergos installer\n')
            txt = 'SYNTHOPTS="-is -a {0} -m alsa_seq -r 48000"\n\n'
            txt = txt.format(audio_system)
            fluid_conf.write(txt)

    @staticmethod
    def patch_user_dirs_update_gtk():
        """ Patches user-dirs-update-gtk.desktop so it is run in
            XFCE, MATE and Cinnamon """
        path = os.path.join(
            DEST_DIR,
            "etc/xdg/autostart/user-dirs-update-gtk.desktop")

        if os.path.exists(path):
            with open(path, 'r') as user_dirs:
                lines = user_dirs.readlines()

            with open(path, 'w') as user_dirs:
                for line in lines:
                    if "OnlyShowIn=" in line:
                        line = "OnlyShowIn=GNOME;LXDE;Unity;XFCE;MATE;Cinnamon\n"
                    user_dirs.write(line)

    def set_keymap(self):
        """ Set X11 and console keymap """
        keyboard_layout = self.settings.get("keyboard_layout")
        keyboard_variant = self.settings.get("keyboard_variant")
        #localectl set-x11-keymap es cat
        cmd = ['localectl', 'set-x11-keymap', keyboard_layout]
        if keyboard_variant:
            cmd.append(keyboard_variant)
        # Systemd based tools like localectl do not work inside a chroot
        # This will set correct keymap to live media, we will copy
        # the created files to destination
        call(cmd)
        # Copy 00-keyboard.conf and vconsole.conf files to destination
        path = os.path.join(DEST_DIR, "etc/X11/xorg.conf.d")
        os.makedirs(path, mode=0o755, exist_ok=True)
        files = [ "/etc/X11/xorg.conf.d/00-keyboard.conf", "/etc/vconsole.conf"]
        for src in files:
            try:
                dst = os.path.join(DEST_DIR, src[1:])
                shutil.copy(src, dst)
                logging.debug("%s copied.", src)
            except FileNotFoundError:
                logging.error("File %s not found", src)
            except FileExistsError:
                logging.warning("File %s already exists.", dst)

    def get_installed_zfs_version(self):
        """ Get installed zfs version """
        zfs_version = "0.6.5.4"
        path = "/install/usr/src"
        for file_name in os.listdir(path):
            if file_name.startswith("zfs") and not file_name.startswith("zfs-utils"):
                try:
                    zfs_version = file_name.split("-")[1]
                    logging.info("Installed zfs module's version: %s", zfs_version)
                except KeyError:
                    logging.warning("Can't get zfs version from %s", file_name)
        return zfs_version

    def get_installed_kernel_versions(self):
        """ Get installed kernel versions """
        kernel_versions = []
        path = "/install/usr/lib/modules"
        for file_name in os.listdir(path):
            if not file_name.startswith("extramodules"):
                kernel_versions.append(file_name)
        return kernel_versions

    def set_desktop_settings(self):
        """ Runs postinstall.sh that sets DE settings
            Postinstall script uses arch-chroot, so we don't have to worry
            about /proc, /dev, ... """
        logging.debug("Running Cnchi post-install script")
        keyboard_layout = self.settings.get("keyboard_layout")
        keyboard_variant = self.settings.get("keyboard_variant")
        # Call post-install script to fine tune our setup
        script_path_postinstall = os.path.join(
            self.settings.get('cnchi'),
            "scripts",
            POSTINSTALL_SCRIPT)
        cmd = [
            "/usr/bin/bash",
            script_path_postinstall,
            self.settings.get('username'),
            DEST_DIR,
            self.desktop,
            self.settings.get("locale"),
            str(self.vbox),
            keyboard_layout]

        # Keyboard variant is optional
        if keyboard_variant:
            cmd.append(keyboard_variant)

        call(cmd, timeout=300)
        logging.debug("Post install script completed successfully.")

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
        logging.debug("fstab file generated.")

        # If SSD was detected copy udev rule for deadline scheduler
        if self.ssd:
            self.set_scheduler()
            logging.debug("SSD udev rule copied successfully")

        # Copy configured networks in Live medium to target system
        if self.settings.get("network_manager") == "NetworkManager":
            self.copy_network_config()

        if self.desktop == "base":
            # Setup systemd-networkd for systems that won't use the
            # networkmanager or connman daemons (atm it's just base install)
            # Enable systemd_networkd services
            # https://github.com/Antergos/Cnchi/issues/332#issuecomment-108745026
            self.enable_services(["systemd-networkd", "systemd-resolved"])
            # Setup systemd_networkd
            # TODO: Ask user for SSID and passphrase if a wireless link is
            # found (here or inside systemd_networkd.setup() ?)
            from installation import systemd_networkd
            systemd_networkd.setup()

        logging.debug("Network configuration done.")

        # Copy mirror list
        mirrorlist_src_path = '/etc/pacman.d/mirrorlist'
        mirrorlist_dst_path = os.path.join(DEST_DIR, 'etc/pacman.d/mirrorlist')
        try:
            shutil.copy2(mirrorlist_src_path, mirrorlist_dst_path)
            logging.debug("Mirror list copied.")
        except FileNotFoundError:
            logging.error(
                "Can't copy mirrorlist file. File %s not found",
                mirrorlist_src_path)
        except FileExistsError:
            logging.warning("File %s already exists.", mirrorlist_dst_path)

        # Add Antergos repo to /etc/pacman.conf
        self.update_pacman_conf()

        logging.debug("pacman.conf has been created successfully")

        # Enable some useful services
        services = []

        if self.desktop != "base":
            # In base there's no desktop manager ;)
            services.append(self.settings.get("desktop_manager"))
            # In base we use systemd-networkd (setup already done above)
            services.append(self.settings.get("network_manager"))
            # If bumblebee (optimus cards) is installed, enable it
            if os.path.exists(os.path.join(DEST_DIR, "usr/lib/systemd/system/bumblebeed.service")):
                services.extend(["bumblebee"])


        services.extend(["ModemManager", "haveged"])

        if self.method == "zfs":
            # Beginning with ZOL version 0.6.5.8 the ZFS service unit files have
            # been changed so that you need to explicitly enable any ZFS services
            # you want to run.
            services.extend(["zfs.target", "zfs-import-cache", "zfs-mount"])

        self.enable_services(services)

        # Enable timesyncd service
        if self.settings.get("use_timesyncd"):
            timesyncd_path = os.path.join(
                DEST_DIR,
                "etc/systemd/timesyncd.conf")
            try:
                with open(timesyncd_path, 'w') as timesyncd:
                    timesyncd.write("[Time]\n")
                    timesyncd.write("NTP=0.arch.pool.ntp.org 1.arch.pool.ntp.org "
                                    "2.arch.pool.ntp.org 3.arch.pool.ntp.org\n")
                    timesyncd.write("FallbackNTP=0.pool.ntp.org 1.pool.ntp.org "
                                    "0.fr.pool.ntp.org\n")
            except FileNotFoundError as err:
                logging.warning("Can't find %s file.", timesyncd_path)
            chroot_call(['systemctl', '-fq', 'enable', 'systemd-timesyncd.service'])

        # Set timezone
        zone = self.settings.get("timezone_zone")
        if zone:
            localtime_path = "/etc/localtime"
            if os.path.exists(localtime_path):
                os.remove(localtime_path)
            zoneinfo_path = os.path.join("/usr/share/zoneinfo", zone)
            chroot_call(['ln', '-s', zoneinfo_path, localtime_path])
            logging.debug("Timezone set to %s", zoneinfo_path)
        else:
            logging.warning("Can't read selected timezone! Will leave it to UTC.")

        # Wait FOREVER until the user sets his params
        # FIXME: We can wait here forever!
        while self.settings.get('user_info_done') is False:
            # Wait five seconds and try again
            time.sleep(5)

        # Set user parameters
        username = self.settings.get('username')
        fullname = self.settings.get('fullname')
        password = self.settings.get('password')
        hostname = self.settings.get('hostname')

        sudoers_dir = os.path.join(DEST_DIR, "etc/sudoers.d")
        if not os.path.exists(sudoers_dir):
            os.mkdir(sudoers_dir, 0o710)
        sudoers_path = os.path.join(sudoers_dir, "10-installer")
        try:
            with open(sudoers_path, "w") as sudoers:
                sudoers.write('{0} ALL=(ALL) ALL\n'.format(username))
            os.chmod(sudoers_path, 0o440)
            logging.debug("Sudo configuration for user %s done.", username)
        except IOError as io_error:
            # Do not fail if can't write 10-installer file.
            # Something bad must be happening, though.
            logging.error(io_error)

        # Configure detected hardware
        # NOTE: Because hardware can need extra repos, this code must run
        # always after having called the update_pacman_conf method
        if self.hardware_install:
            try:
                logging.debug("Running hardware drivers post-install jobs...")
                self.hardware_install.post_install(DEST_DIR)
            except Exception as ex:
                template = "Error in hardware module. An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                logging.error(message)

        # Setup user

        default_groups = 'wheel'

        if self.vbox:
            # Why there is no vboxusers group? Add it ourselves.
            chroot_call(['groupadd', 'vboxusers'])
            default_groups += ',vboxusers,vboxsf'
            self.enable_services(["vboxservice"])

        if self.settings.get('require_password') is False:
            # Prepare system for autologin.
            # LightDM needs the user to be in the autologin group.
            chroot_call(['groupadd', 'autologin'])
            default_groups += ',autologin'

        cmd = [
            'useradd',
            '-m',
            '-s', '/bin/bash',
            '-g', 'users',
            '-G', default_groups,
            username]
        chroot_call(cmd)
        logging.debug("User %s added.", username)

        self.change_user_password(username, password)

        chroot_call(['chfn', '-f', fullname, username])
        home_dir = os.path.join("/home", username)
        cmd = ['chown', '-R', '{0}:users'.format(username), home_dir]
        chroot_call(cmd)

        # Set hostname
        hostname_path = os.path.join(DEST_DIR, "etc/hostname")
        if not os.path.exists(hostname_path):
            with open(hostname_path, "w") as hostname_file:
                hostname_file.write(hostname)

        logging.debug("Hostname set to %s", hostname)

        # User password is the root password
        self.change_user_password('root', password)
        logging.debug("Set the same password to root.")

        # Generate locales
        locale = self.settings.get("locale")
        self.queue_event('info', _("Generating locales..."))
        self.uncomment_locale_gen(locale)
        chroot_call(['locale-gen'])
        locale_conf_path = os.path.join(DEST_DIR, "etc/locale.conf")
        with open(locale_conf_path, "w") as locale_conf:
            locale_conf.write('LANG={0}\n'.format(locale))
            locale_conf.write('LC_COLLATE={0}\n'.format(locale))

        # environment_path = os.path.join(DEST_DIR, "etc/environment")
        # with open(environment_path, "w") as environment:
        #    environment.write('LANG={0}\n'.format(locale))

        self.queue_event('info', _("Adjusting hardware clock..."))
        self.auto_timesetting()

        self.queue_event('info', _("Configuring keymap..."))
        self.set_keymap()

        # Install configs for root
        chroot_call(['cp', '-av', '/etc/skel/.', '/root/'])

        self.queue_event('info', _("Configuring hardware..."))

        # Copy generated xorg.conf to target
        if os.path.exists("/etc/X11/xorg.conf"):
            src = "/etc/X11/xorg.conf"
            dst = os.path.join(DEST_DIR, 'etc/X11/xorg.conf')
            shutil.copy2(src, dst)

        # Configure ALSA
        #self.alsa_mixer_setup()
        #logging.debug("Updated Alsa mixer settings")

        # Set pulse
        #if os.path.exists(os.path.join(DEST_DIR, "usr/bin/pulseaudio-ctl")):
        #    chroot_run(['pulseaudio-ctl', 'normal'])

        # Set fluidsynth audio system (in our case, pulseaudio)
        self.set_fluidsynth()
        logging.debug("Updated fluidsynth configuration file")

        # Workaround for pacman-key bug FS#45351
        # https://bugs.archlinux.org/task/45351
        # We have to kill gpg-agent because if it stays around we can't
        # reliably unmount the target partition.
        logging.debug("Stopping gpg agent...")
        chroot_call(['killall', '-9', 'gpg-agent'])

        # FIXME: Temporary workaround for spl and zfs packages
        if self.method == "zfs":
            self.queue_event('info', _("Building zfs modules..."))
            zfs_version = self.get_installed_zfs_version()
            spl_module = 'spl/{}'.format(zfs_version)
            zfs_module = 'zfs/{}'.format(zfs_version)
            kernel_versions = self.get_installed_kernel_versions()
            if kernel_versions:
                for kernel_version in kernel_versions:
                    logging.debug("Installing zfs v%s modules for kernel %s", zfs_version, kernel_version)
                    chroot_call(['dkms', 'install', spl_module, '-k', kernel_version])
                    chroot_call(['dkms', 'install', zfs_module, '-k', kernel_version])
            else:
                # No kernel version found, try to install for current kernel
                logging.debug("Installing zfs v%s modules for current kernel.", zfs_version)
                chroot_call(['dkms', 'install', spl_module])
                chroot_call(['dkms', 'install', zfs_module])

        # Let's start without using hwdetect for mkinitcpio.conf.
        # It should work out of the box most of the time.
        # This way we don't have to fix deprecated hooks.
        # NOTE: With LUKS or LVM maybe we'll have to fix deprecated hooks.
        self.queue_event('info', _("Configuring System Startup..."))
        mkinitcpio.run(DEST_DIR, self.settings, self.mount_devices, self.blvm)

        # Patch user-dirs-update-gtk.desktop
        self.patch_user_dirs_update_gtk()
        logging.debug("File user-dirs-update-gtk.desktop patched.")

        # Set lightdm config including autologin if selected
        if self.desktop != "base":
            self.setup_display_manager()

        # Configure user features (firewall, libreoffice language pack, ...)
        self.setup_features()

        # Encrypt user's home directory if requested
        # FIXME: This is not working atm
        if self.settings.get('encrypt_home'):
            self.queue_event('info', _("Encrypting user home dir..."))
            encfs.setup(username, DEST_DIR)
            logging.debug("User home dir encrypted")

        # Install boot loader (always after running mkinitcpio)
        if self.settings.get('bootloader_install'):
            try:
                self.queue_event('info', _("Installing bootloader..."))
                from installation.boot import loader
                boot_loader = loader.Bootloader(
                    DEST_DIR,
                    self.settings,
                    self.mount_devices)
                boot_loader.install()
            except Exception as ex:
                template = "Cannot install bootloader. An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                logging.error(message)

        # Create an initial database for mandb
        #self.queue_event('info', _("Updating man pages..."))
        #chroot_call(["mandb", "--quiet"])

        # Initialise pkgfile (pacman .files metadata explorer) database
        logging.debug("Updating pkgfile database")
        chroot_call(["pkgfile", "--update"])

        if self.desktop != "base":
            # avahi package seems to fail to create its user and group in some cases (¿?)
            cmd = ["groupadd", "-r", "-g", "84", "avahi"]
            chroot_call(cmd)
            cmd = ["useradd", "-r", "-u", "84", "-g", "avahi", "-d", "/", "-s",
                "/bin/nologin", "-c", "avahi", "avahi"]
            chroot_call(cmd)

        # Enable AUR in pamac if AUR feature selected
        pamac_conf = os.path.join(DEST_DIR, 'etc/pamac.conf')
        if os.path.exists(pamac_conf) and self.settings.get('feature_aur'):
            logging.debug("Enabling AUR options in pamac")
            with open(pamac_conf, 'r') as f:
                file_data = f.read()
            file_data = file_data.replace("#EnableAUR", "EnableAUR")
            file_data = file_data.replace("#SearchInAURByDefault", "SearchInAURByDefault")
            file_data = file_data.replace("#CheckAURUpdates", "CheckAURUpdates")
            with open(pamac_conf, 'w') as f:
                f.write(file_data)
