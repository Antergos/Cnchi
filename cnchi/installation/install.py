#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  installation.py
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Installation process module. """

import crypt
import logging
import os
import queue
import shutil
import subprocess
import sys
import time
import re

from mako.template import Template

import desktop_info
import parted3.fs_module as fs
import misc.misc as misc
import pacman.pac as pac
import encfs

from download import download

from installation import auto_partition
from installation import chroot
from installation import mkinitcpio
from installation import firewall

from misc.misc import InstallError

try:
    import xml.etree.cElementTree as eTree
except ImportError as err:
    import xml.etree.ElementTree as eTree

try:
    import pyalpm
except ImportError as err:
    logging.error(err)

import hardware.hardware as hardware

POSTINSTALL_SCRIPT = 'postinstall.sh'
DEST_DIR = "/install"


def chroot_run(cmd):
    chroot.run(cmd, DEST_DIR)


def write_file(filecontents, filename):
    """ writes a string of data to disk """
    os.makedirs(os.path.dirname(filename), mode=0o755, exist_ok=True)

    with open(filename, "w") as fh:
        fh.write(filecontents)


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
        msg = _("Installing using the '{0}' method").format(self.method)
        self.queue_event('info', msg)

        self.desktop = self.settings.get('desktop')

        # This flag tells us if there is a lvm partition (from advanced install)
        # If it's true we'll have to add the 'lvm2' hook to mkinitcpio
        self.blvm = blvm

        if ssd is not None:
            self.ssd = ssd
        else:
            self.ssd = {}

        self.mount_devices = mount_devices

        self.desktop_manager = 'lightdm'
        # Set defaults
        self.network_manager = 'NetworkManager'

        self.fs_devices = fs_devices

        self.running = True
        self.error = False

        self.auto_device = ""
        self.packages = packages
        self.pacman = None
        self.vbox = self.settings.get('is_vbox')

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
        if self.callback_queue is not None:
            try:
                self.callback_queue.put_nowait((event_type, event_text))
            except queue.Full:
                pass
        else:
            print("{0}: {1}".format(event_type, event_text))

    def mount_partitions(self):
        """ Do not call this in automatic mode as AutoPartition class mounts
        the root and boot devices itself. """

        if os.path.exists(DEST_DIR):
            # If we're recovering from a failed/stoped install, there'll be
            # some mounted directories. Try to unmount them first.
            # We use unmount_all from auto_partition to do this.
            auto_partition.unmount_all(DEST_DIR)

        # NOTE: Advanced method formats root by default in advanced.py
        root_partition = self.mount_devices["/"]

        # Boot partition
        if "/boot" in self.mount_devices:
            boot_partition = self.mount_devices["/boot"]
        else:
            boot_partition = ""

        # Swap partition
        if "swap" in self.mount_devices:
            swap_partition = self.mount_devices["swap"]
        else:
            swap_partition = ""

        # Mount root and boot partitions (only if it's needed)
        # Not doing this in automatic mode as AutoPartition class mounts
        # the root and boot devices itself.
        txt = _("Mounting partition {0} into {1} directory").format(root_partition, DEST_DIR)
        logging.debug(txt)
        subprocess.check_call(['mount', root_partition, DEST_DIR])
        # We also mount the boot partition if it's needed
        boot_path = os.path.join(DEST_DIR, "boot")
        os.makedirs(boot_path, mode=0o755, exist_ok=True)
        if "/boot" in self.mount_devices:
            txt = _("Mounting partition {0} into {1}/boot directory")
            txt = txt.format(boot_partition, boot_path)
            logging.debug(txt)
            subprocess.check_call(['mount', boot_partition, boot_path])

        # In advanced mode, mount all partitions (root and boot are already mounted)
        if self.method == 'advanced':
            for path in self.mount_devices:
                if path == "":
                    # Ignore devices without a mount path (or they will be mounted at "DEST_DIR")
                    continue

                mount_part = self.mount_devices[path]

                if mount_part != root_partition and mount_part != boot_partition and mount_part != swap_partition:
                    if path[0] == '/':
                        path = path[1:]
                    mount_dir = os.path.join(DEST_DIR, path)
                    try:
                        os.makedirs(mount_dir, mode=0o755, exist_ok=True)
                        txt = _("Mounting partition {0} into {1} directory").format(mount_part, mount_dir)
                        logging.debug(txt)
                        subprocess.check_call(['mount', mount_part, mount_dir])
                    except subprocess.CalledProcessError as process_error:
                        # We will continue as root and boot are already mounted
                        txt = "Unable to mount {0}, command {1} failed: {2}".format(
                            mount_part, process_error.cmd, process_error.output)
                        logging.warning(txt)
                elif mount_part == swap_partition:
                    try:
                        logging.debug("Activating swap in %s", mount_part)
                        subprocess.check_call(['swapon', swap_partition])
                    except subprocess.CalledProcessError as process_error:
                        # We can continue even if no swap is on
                        txt = "Unable to activate swap {0}, command {1} failed: {2}".format(
                            mount_part, process_error.cmd, process_error.output)
                        logging.warning(txt)

    @misc.raise_privileges
    def start(self):
        """ Run installation """

        '''
        From this point, on a warning situation, Cnchi should try to continue,
        so we need to catch the exception here. If we don't catch the exception
        here, it will be catched in run() and managed as a fatal error.
        On the other hand, if we want to clarify the exception message we can
        catch it here and then raise an InstallError exception.
        '''

        if not os.path.exists(DEST_DIR):
            with misc.raised_privileges():
                os.makedirs(DEST_DIR, mode=0o755, exist_ok=True)

        # Mount needed partitions (in automatic it's already done)
        if self.method == 'alongside' or self.method == 'advanced':
            self.mount_partitions()

        # Nasty workaround:
        # If pacman was stoped and /var is in another partition than root
        # (so as to be able to resume install), database lock file will still be in place.
        # We must delete it or this new installation will fail
        db_lock = os.path.join(DEST_DIR, "var/lib/pacman/db.lck")
        if os.path.exists(db_lock):
            with misc.raised_privileges():
                os.remove(db_lock)
            logging.debug("%s deleted", db_lock)

        # Create some needed folders
        folders = [
            os.path.join(DEST_DIR, 'var/lib/pacman'),
            os.path.join(DEST_DIR, 'etc/pacman.d/gnupg'),
            os.path.join(DEST_DIR, 'var/log')]

        for folder in folders:
            os.makedirs(folder, mode=0o755, exist_ok=True)

        # If kernel images exists in /boot they are most likely from a failed install attempt and need
        # to be removed otherwise pyalpm will raise a fatal exception later on.
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

        logging.debug("Downloading packages...")
        self.download_packages()

        logging.debug("Installing packages...")
        self.install_packages()

        logging.debug("Configuring system...")
        self.configure_system()

        self.running = False

        # Installation finished successfully
        self.queue_event('finished', _("Installation finished"))
        self.error = False
        return True

    @staticmethod
    def copy_log():
        # Copy Cnchi log to new installation
        datetime = "{0}-{1}".format(time.strftime("%Y%m%d"), time.strftime("%H%M%S"))
        dst = os.path.join(DEST_DIR, "var/log/cnchi-{0}.log".format(datetime))
        pidst = os.path.join(DEST_DIR, "var/log/postinstall-{0}.log".format(datetime))
        try:
            shutil.copy("/tmp/cnchi.log", dst)
            shutil.copy("/tmp/postinstall.log", pidst)
        except FileNotFoundError:
            logging.warning("Can't copy Cnchi log to %s", dst)
        except FileExistsError:
            pass

    def download_packages(self):
        """ Downloads necessary packages """
        pacman_conf_file = "/tmp/pacman.conf"
        pacman_cache_dir = os.path.join(DEST_DIR, "var/cache/pacman/pkg")

        if self.settings.get("cache") != '':
            cache_dir = self.settings.get("cache")
        else:
            cache_dir = '/var/cache/pacman/pkg'

        if self.settings.get("download_module"):
            download_module = self.settings.get("download_module")
        else:
            download_module = 'requests'

        download_packages = download.DownloadPackages(
            self.packages,
            download_module,
            pacman_conf_file,
            pacman_cache_dir,
            cache_dir,
            self.settings,
            self.callback_queue)
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
        file_rendered = file_template.render(destDir=DEST_DIR, arch=myarch, desktop=self.desktop)
        write_file(file_rendered, os.path.join("/tmp", "pacman.conf"))

    def prepare_pacman(self):
        """ Configures pacman and syncs db on destination system """

        self.create_pacman_conf_file()
        self.prepare_pacman_keyring()

        # Init pyalpm
        try:
            self.pacman = pac.Pac("/tmp/pacman.conf", self.callback_queue)
        except Exception:
            self.pacman = None
            logging.error("Can't initialize pyalpm.")
            raise InstallError(_("Can't initialize pyalpm."))

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
        try:
            cmd = ["systemctl", "start", "haveged"]
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as process_error:
            txt = "Can't start haveged service, command {0} failed: {1}".format(process_error.cmd, process_error.output)
            logging.warning(txt)

        # Delete old gnupg files
        dest_path = os.path.join(DEST_DIR, "etc/pacman.d/gnupg")
        try:
            cmd = ["rm", "-rf", dest_path]
            subprocess.check_call(cmd)
            os.mkdir(dest_path)
        except subprocess.CalledProcessError as process_error:
            txt = "Error deleting old gnupg files, command {0} failed: {1}".format(
                process_error.cmd, process_error.output)
            logging.warning(txt)

        # Tell pacman-key to regenerate gnupg files
        try:
            cmd = ["pacman-key", "--init", "--gpgdir", dest_path]
            subprocess.check_call(cmd)
            cmd = ["pacman-key", "--populate", "--gpgdir", dest_path, "archlinux", "antergos"]
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as process_error:
            txt = "Error regenerating gnupg files with pacman-key, command {0} failed: {1}".format(
                process_error.cmd, process_error.output)
            logging.warning(txt)

    def install_packages(self):
        """ Start pacman installation of packages """

        logging.debug("Installing packages...")
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

        all_lines = ["# /etc/fstab: static file system information.",
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
                    _("Can't get {0} partition UUID. It won't be added to fstab"),
                    partition_path)
                continue

            if partition_path in self.fs_devices:
                myfmt = self.fs_devices[partition_path]
            else:
                # It hasn't any filesystem defined, skip it.
                continue

            # Take care of swap partitions
            if "swap" in myfmt:
                # If using a TRIM supported SSD, discard is a valid mount option for swap
                if partition_path in self.ssd:
                    opts = "defaults,discard"
                else:
                    opts = "defaults"
                txt = "UUID={0} swap swap {1} 0 0".format(uuid, opts)
                all_lines.append(txt)
                logging.debug("Added %s to fstab", txt)
                continue

            crypttab_path = os.path.join(DEST_DIR, 'etc/crypttab')

            # Fix for home + luks, no lvm (from Automatic Install)
            if "/home" in mount_point and self.method == "automatic" and use_luks and not use_lvm:
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
            if self.method == "advanced" and mount_point is not "/" and use_luks and "/dev/mapper" in partition_path:
                # As the mapper with the filesystem will have a different UUID than
                # the partition it is encrypted in, we have to take care of this here.
                # Then we will be able to add it to crypttab

                vol_name = partition_path[len("/dev/mapper/"):]
                try:
                    luks_partition_path = "/dev/" + pknames[vol_name]
                except KeyError:
                    logging.error("Can't find the PKNAME value of %s", partition_path)
                    continue

                luks_uuid = fs.get_uuid(luks_partition_path)

                if len(luks_uuid) > 0:
                    # OK, add it to crypttab with the correct uuid
                    os.chmod(crypttab_path, 0o666)
                    with open(crypttab_path, 'a') as crypttab_file:
                        line = "{0} /dev/disk/by-uuid/{1} none luks\n".format(vol_name, luks_uuid)
                        crypttab_file.write(line)
                        logging.debug("Added %s to crypttab", line)
                    os.chmod(crypttab_path, 0o600)
                else:
                    logging.error("Can't add luks uuid to crypttab for %s partition", luks_partition_path)
                    continue

                # Finally, the fstab line to mount the unencrypted file system
                # if a mount point has been specified by the user
                if len(mount_point) > 0:
                    txt = "{0} {1} {2} defaults 0 0".format(partition_path, mount_point, myfmt)
                    all_lines.append(txt)
                    logging.debug("Added %s to fstab", txt)
                continue

            # fstab uses vfat to mount fat16 and fat32 partitions
            if "fat" in myfmt:
                myfmt = 'vfat'

            if "btrfs" in myfmt:
                self.settings.set('btrfs', True)

            # Avoid adding a partition to fstab when it has no mount point (swap has been checked above)
            if mount_point == "":
                continue

            # Create mount point on destination system if it yet doesn't exist
            full_path = os.path.join(DEST_DIR, mount_point)
            os.makedirs(full_path, mode=0o755, exist_ok=True)

            # Is ssd ?
            # Device list example: {'/dev/sdb': False, '/dev/sda': True}

            logging.debug("Device list : {0}".format(self.ssd))
            device = re.sub("[0-9]+$", "", partition_path)
            is_ssd = self.ssd.get(device)
            logging.debug("Device: {0}, SSD: {1}".format(device, is_ssd))

            # Add mount options parameters
            if not is_ssd:
                if "btrfs" in myfmt:
                    opts = 'defaults,rw,relatime,space_cache,autodefrag,inode_cache'
                elif "f2fs" in myfmt:
                    opts = 'defaults,rw,noatime'
                elif "ext3" in myfmt or "ext4" in myfmt:
                    opts = 'defaults,rw,relatime,data=ordered'
                else:
                    opts = 'defaults,rw,relatime'
            else:
                # As of linux kernel version 3.7, the following
                # filesystems support TRIM: ext4, btrfs, JFS, and XFS.
                if myfmt == 'ext4' or myfmt == 'jfs' or myfmt == 'xfs':
                    opts = 'defaults,rw,noatime,discard'
                elif myfmt == 'btrfs':
                    opts = 'defaults,rw,noatime,compress=lzo,ssd,discard,space_cache,autodefrag,inode_cache'
                else:
                    opts = 'defaults,rw,noatime'

            no_check = ["btrfs", "f2fs"]

            if mount_point == "/" and myfmt not in no_check:
                chk = '1'
            else:
                chk = '0'

            if mount_point == "/":
                self.settings.set('ruuid', uuid)

            txt = "UUID={0} {1} {2} {3} 0 {4}".format(uuid, mount_point, myfmt, opts, chk)
            all_lines.append(txt)
            logging.debug("Added %s to fstab", txt)

        full_text = '\n'.join(all_lines) + '\n'

        fstab_path = os.path.join(DEST_DIR, 'etc/fstab')
        with open(fstab_path, 'w') as fstab_file:
            fstab_file.write(full_text)

        logging.debug("fstab written.")

    def set_scheduler(self):
        rule_src = os.path.join(self.settings.get('cnchi'), 'scripts/60-schedulers.rules')
        rule_dst = os.path.join(DEST_DIR, "etc/udev/rules.d/60-schedulers.rules")
        try:
            shutil.copy2(rule_src, rule_dst)
            os.chmod(rule_dst, 0o755)
        except FileNotFoundError:
            logging.warning("Cannot copy udev rule for SSDs, file %s not found.", rule_src)
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
                chroot_run(['systemctl', '-f', 'enable', name])
                logging.debug("Service '%s' has been enabled.", name)
            else:
                logging.warning("Can't find service %s", name)

    @staticmethod
    def change_user_password(user, new_password):
        """ Changes the user's password """
        shadow_password = crypt.crypt(new_password, "$6${0}$".format(user))
        chroot_run(['usermod', '-p', shadow_password, user])

    @staticmethod
    def auto_timesetting():
        """ Set hardware clock """
        try:
            subprocess.check_call(["hwclock", "--systohc", "--utc"])
        except subprocess.CalledProcessError as process_error:
            txt = "Error adjusting hardware clock, command {0} failed: {1}".format(
                process_error.cmd, process_error.output)
            logging.warning(txt)
        shutil.copy2("/etc/adjtime", os.path.join(DEST_DIR, "etc/"))

    @staticmethod
    def update_pacman_conf():
        """ Add Antergos and multilib repos """
        path = os.path.join(DEST_DIR, "etc/pacman.conf")
        if os.path.exists(path):
            paclines = []
            with open(path) as f:
                paclines = f.readlines()

            if os.uname()[-1] == "x86_64":
                for i in range(0, len(paclines)):
                    if paclines[i] == "#[multilib]\n":
                        paclines[i] = "[multilib]\n"
                        paclines[i+1] = "Include = /etc/pacman.d/mirrorlist\n"
                        break
            paclines.append("\n")
            paclines.append("[antergos]\n")
            paclines.append("SigLevel = PackageRequired\n")
            paclines.append("Include = /etc/pacman.d/antergos-mirrorlist\n")
            with open(path, "w") as f:
                f.write("".join(paclines))
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

    @staticmethod
    def check_output(command):
        """ Helper function to run a command """
        return subprocess.check_output(command.split()).decode().strip("\n")

    def copy_cached_packages(self, cache_dir):
        """ Copy all packages from specified directory to install's target """
        # Check in case user has given a wrong folder
        if not os.path.exists(cache_dir):
            return
        self.queue_event('info', _('Copying xz files from cache...'))
        dest_dir = os.path.join(DEST_DIR, "var/cache/pacman/pkg")
        os.makedirs(dest_dir, mode=0o755, exist_ok=True)
        self.copy_files_progress(cache_dir, dest_dir)

    def copy_files_progress(self, src, dst):
        """ Copy files updating the slides' progress bar """
        percent = 0.0
        items = os.listdir(src)
        if len(items) > 0:
            step = 1.0 / len(items)
            for item in items:
                self.queue_event('percent', percent)
                source = os.path.join(src, item)
                destination = os.path.join(dst, item)
                try:
                    shutil.copy2(source, destination)
                except (FileExistsError, shutil.Error) as file_error:
                    logging.warning(file_error)
                percent += step

    def setup_features(self):
        """ Do all set up needed by the user's selected features """
        services = []

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

        if self.settings.get("feature_lamp") and not self.settings.get("feature_lemp"):
            try:
                from installation import lamp
                logging.debug("Configuring LAMP...")
                lamp.setup()
                services.extend(["httpd", "mysqld"])
            except ImportError as import_error:
                logging.warning("Unable to import LAMP module: %s", str(import_error))
        elif self.settings.get("feature_lemp"):
            try:
                from installation import lemp
                logging.debug("Configuring LEMP...")
                lemp.setup()
                services.extend(["nginx", "mysqld", "php-fpm"])
            except ImportError as import_error:
                logging.warning("Unable to import LEMP module: %s", str(import_error))

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
                    lightdm_conf.write(line)

            txt = _("LightDM display manager configuration completed.")
            logging.debug(txt)
        except FileNotFoundError:
            txt = _("Error while trying to configure the LightDM display manager")
            logging.warning(txt)

    @staticmethod
    def alsa_mixer_setup():
        """ Sets ALSA mixer settings """

        cmds = [
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

        for cmd in cmds:
            chroot_run(['sh', '-c', 'amixer -c 0 sset {0}'.format(cmd)])

        # Save settings
        chroot_run(['alsactl', '-f', '/etc/asound.state', 'store'])

    @staticmethod
    def set_fluidsynth():
        """ Sets fluidsynth configuration file """

        fluid_path = os.path.join(DEST_DIR, "etc/conf.d/fluidsynth")

        if not os.path.exists(fluid_path):
            return

        audio_system = "alsa"

        pulse_path = os.path.join(DEST_DIR, "usr/bin/pulseaudio")
        if os.path.exists(pulse_path):
            audio_system = "pulse"

        with open(fluid_path, "w") as fluid_conf:
            fluid_conf.write('# Created by Cnchi, Antergos installer\n')
            fluid_conf.write('SYNTHOPTS="-is -a {0} -m alsa_seq -r 48000"\n\n'.format(audio_system))

    def configure_system(self):
        """ Final install steps
            Set clock, language, timezone
            Run mkinitcpio
            Populate pacman keyring
            Setup systemd services
            ... and more """

        self.queue_event('pulse', 'start')
        self.queue_event('info', _("Configuring your new system"))

        # This mounts (binds) /dev and others to /DEST_DIR/dev and others
        chroot.mount_special_dirs(DEST_DIR)

        self.auto_fstab()
        logging.debug("fstab file generated.")

        # If SSD was detected copy udev rule for deadline scheduler
        if self.ssd:
            self.set_scheduler()
            logging.debug("SSD udev rule copied successfully")

        # Copy configured networks in Live medium to target system
        if self.network_manager == 'NetworkManager':
            self.copy_network_config()

        if self.desktop == "base":
            # Setup systemd-networkd for systems that won't use the
            # networkmanager or connman daemons (atm it's just base install)
            # Enable systemd_networkd services
            # See: https://github.com/Antergos/Cnchi/issues/332#issuecomment-108745026
            self.enable_services(["systemd-networkd", "systemd-resolved"])
            # Setup systemd_networkd
            # TODO: Ask user for SSID and passphrase if a wireless link is found
            # (should this be done here or inside systemd_networkd.setup() ?)
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
            logging.error("Can't copy mirrorlist file. File %s not found", mirrorlist_src_path)
        except FileExistsError:
            logging.warning("File %s already exists.", mirrorlist_dst_path)

        # Add Antergos repo to /etc/pacman.conf
        self.update_pacman_conf()

        logging.debug("pacman.conf has been created successfully")

        # Enable some useful services
        services = []
        if self.desktop != "base":
            # In base there's no desktop manager ;)
            services.append(self.desktop_manager)
            # In base we use systemd-networkd (setup already done above)
            services.append(self.network_manager)
        services.extend(["ModemManager", "haveged"])
        self.enable_services(services)

        # Enable timesyncd service
        if self.settings.get("use_timesyncd"):
            timesyncd_path = os.path.join(DEST_DIR, "etc/systemd/timesyncd.conf")
            with open(timesyncd_path, 'w') as timesyncd:
                timesyncd.write("[Time]\n")
                timesyncd.write("NTP=0.arch.pool.ntp.org 1.arch.pool.ntp.org 2.arch.pool.ntp.org 3.arch.pool.ntp.org\n")
                timesyncd.write("FallbackNTP=0.pool.ntp.org 1.pool.ntp.org 0.fr.pool.ntp.org\n")
            chroot_run(['timedatectl', 'set-ntp', 'true'])

        # Set timezone
        zoneinfo_path = os.path.join("/usr/share/zoneinfo", self.settings.get("timezone_zone"))
        chroot_run(['ln', '-s', zoneinfo_path, "/etc/localtime"])
        logging.debug("Timezone set.")

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
            # Do not fail if can't write 10-installer file. Something bad must be happening, though.
            logging.error(io_error)

        # Configure detected hardware
        # NOTE: Because hardware can need extra repos, this code must run
        # always after having called the update_pacman_conf method
        if self.hardware_install:
            try:
                logging.debug("Running hardware drivers post-install jobs...")
                self.hardware_install.post_install(DEST_DIR)
            except Exception as general_error:
                logging.error("Unknown error in hardware module. Output: %s", general_error)

        # Setup user

        default_groups = 'lp,video,network,storage,wheel,audio'

        if self.vbox:
            # Why there is no vboxusers group? Add it ourselves.
            chroot_run(['groupadd', 'vboxusers'])
            default_groups += ',vboxusers,vboxsf'
            self.enable_services(["vboxservice"])

        if self.settings.get('require_password') is False:
            # Prepare system for autologin. LightDM needs the user to be in the autologin group.
            chroot_run(['groupadd', 'autologin'])
            default_groups += ',autologin'

        cmd = ['useradd', '-m', '-s', '/bin/bash', '-g', 'users', '-G', default_groups, username]
        chroot_run(cmd)
        logging.debug("User %s added.", username)

        self.change_user_password(username, password)

        cmd = ['chfn', '-f', fullname, username]
        chroot_run(cmd)

        cmd = ['chown', '-R', '{0}:users'.format(username), os.path.join("/home", username)]
        chroot_run(cmd)

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
        chroot_run(['locale-gen'])
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

        keyboard_layout = self.settings.get("keyboard_layout")
        keyboard_variant = self.settings.get("keyboard_variant")

        if self.desktop != "base":
            # Set /etc/X11/xorg.conf.d/00-keyboard.conf for the xkblayout
            logging.debug("Set /etc/X11/xorg.conf.d/00-keyboard.conf for the xkblayout")
            xorg_conf_dir = os.path.join(DEST_DIR, "etc/X11/xorg.conf.d")
            if not os.path.exists(xorg_conf_dir):
                os.mkdir(xorg_conf_dir, 0o755)
            xorg_conf_xkb_path = os.path.join(xorg_conf_dir, "00-keyboard.conf")
            try:
                with open(xorg_conf_xkb_path, "w") as xorg_conf_xkb:
                    xorg_conf_xkb.write(
                        "# Read and parsed by systemd-localed. It's probably wise not to edit this file\n")
                    xorg_conf_xkb.write('# manually too freely.\n')
                    xorg_conf_xkb.write('Section "InputClass"\n')
                    xorg_conf_xkb.write('        Identifier "system-keyboard"\n')
                    xorg_conf_xkb.write('        MatchIsKeyboard "on"\n')
                    xorg_conf_xkb.write('        Option "XkbLayout" "{0}"\n'.format(keyboard_layout))
                    if keyboard_variant and len(keyboard_variant) > 0:
                        xorg_conf_xkb.write('        Option "XkbVariant" "{0}"\n'.format(keyboard_variant))
                    xorg_conf_xkb.write('EndSection\n')
                logging.debug("00-keyboard.conf written.")
            except IOError as io_error:
                # Do not fail if 00-keyboard.conf can't be created.
                # Something bad must be happening, though.
                logging.error(io_error)

        # Set vconsole.conf for console keymap
        if keyboard_layout == "gb":
            # The keyboard layout for Great Britain is "uk" in the cli and
            # "gb" (not uk) in X, just to make things more complicated.
            keyboard_layout_cli = "uk"
        else:
            keyboard_layout_cli = keyboard_layout

        vconsole_path = os.path.join(DEST_DIR, "etc/vconsole.conf")
        with open(vconsole_path, 'w') as vconsole:
            vconsole.write("KEYMAP={0}\n".format(keyboard_layout_cli))

        # Install configs for root
        cmd = ['cp', '-av', '/etc/skel/.', '/root/']
        chroot_run(cmd)

        self.queue_event('info', _("Configuring hardware..."))

        # Copy generated xorg.conf to target
        if os.path.exists("/etc/X11/xorg.conf"):
            shutil.copy2(
                "/etc/X11/xorg.conf",
                os.path.join(DEST_DIR, 'etc/X11/xorg.conf'))

        # Configure ALSA
        self.alsa_mixer_setup()
        logging.debug("Updated Alsa mixer settings")

        # Set pulse
        if os.path.exists(os.path.join(DEST_DIR, "usr/bin/pulseaudio-ctl")):
            chroot_run(['pulseaudio-ctl', 'normal'])

        # Set fluidsynth audio system (in our case, pulseaudio)
        self.set_fluidsynth()
        logging.debug("Updated fluidsynth configuration file")

        # Let's start without using hwdetect for mkinitcpio.conf.
        # It should work out of the box most of the time.
        # This way we don't have to fix deprecated hooks.
        # NOTE: With LUKS or LVM maybe we'll have to fix deprecated hooks.
        self.queue_event('info', _("Configuring System Startup..."))
        mkinitcpio.run(DEST_DIR, self.settings, self.mount_devices, self.blvm)

        logging.debug("Running Cnchi post-install script")
        # Call post-install script to fine tune our setup
        script_path_postinstall = os.path.join(
            self.settings.get('cnchi'),
            "scripts",
            POSTINSTALL_SCRIPT)
        cmd = ["/usr/bin/bash", script_path_postinstall, username, DEST_DIR, self.desktop, keyboard_layout]
        if keyboard_variant:
            cmd.append(keyboard_variant)
        else:
            cmd.append("")
        cmd.append(str(self.vbox))
        try:
            subprocess.check_call(cmd, timeout=300)
            logging.debug("Post install script completed successfully.")
        except subprocess.CalledProcessError as process_error:
            # Even though Post-install script call has failed we will go on
            logging.error("Error running post-install script, command %s failed: %s",
                process_error.cmd, process_error.output)
        except subprocess.TimeoutExpired as timeout_error:
            logging.error(timeout_error)

        # Set lightdm config including autologin if selected
        if self.desktop != "base":
            self.setup_display_manager()

        # Configure user features (firewall, libreoffice language pack, ...)
        self.setup_features()

        # Encrypt user's home directory if requested
        # FIXME: This is not working atm
        if self.settings.get('encrypt_home'):
            logging.debug("Encrypting user home dir...")
            encfs.setup(username, DEST_DIR)
            logging.debug("User home dir encrypted")

        # Install boot loader (always after running mkinitcpio)
        if self.settings.get('bootloader_install'):
            try:
                logging.debug("Installing bootloader...")
                from installation import bootloader
                boot_loader = bootloader.Bootloader(DEST_DIR, self.settings, self.mount_devices)
                boot_loader.install()
            except Exception as general_error:
                logging.warning("While installing boot loader Cnchi encountered this error: %s", general_error)

        # This unmounts (unbinds) /dev and others to /DEST_DIR/dev and others
        chroot.umount_special_dirs(DEST_DIR)

        # Copy installer log to the new installation (just in case something goes wrong)
        logging.debug("Copying install log to /var/log.")
        self.copy_log()

        self.queue_event('pulse', 'stop')
