#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# grub2.py
#
# Copyright © 2013-2017 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.


""" GRUB2 bootloader installation """

import logging
import os
import shutil
import subprocess
import re

try:
    import parted3.fs_module as fs
    from installation import special_dirs
    from misc.run_cmd import call, chroot_call
    from misc.extra import random_generator
except ImportError:
    pass


# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


class Grub2(object):
    """ Class to perform boot loader installation """
    def __init__(self, dest_dir, settings, uuids):
        self.dest_dir = dest_dir
        self.settings = settings
        self.uuids = uuids

    def install(self):
        """ Install Grub2 bootloader """
        self.modify_grub_default()
        self.prepare_grub_d()

        if os.path.exists('/sys/firmware/efi'):
            logging.debug("Cnchi will install the Grub2 (efi) loader")
            self.install_efi()
        else:
            logging.debug("Cnchi will install the Grub2 (bios) loader")
            self.install_bios()

        self.check_root_uuid_in_grub()

    def check_root_uuid_in_grub(self):
        """ Checks grub.cfg for correct root UUID """
        if self.settings.get("zfs"):
            # No root uuid checking if using zfs
            return

        if "/" not in self.uuids:
            logging.warning(
                "Root uuid variable is not set. I can't check root UUID"
                "in grub.cfg, let's hope it's ok")
            return

        ruuid_str = 'root=UUID={0}'.format(self.uuids["/"])

        cmdline_linux = self.settings.get('GRUB_CMDLINE_LINUX')
        if cmdline_linux is None:
            cmdline_linux = ""

        cmdline_linux_default = self.settings.get('GRUB_CMDLINE_LINUX_DEFAULT')
        if cmdline_linux_default is None:
            cmdline_linux_default = ""

        boot_command = 'linux /vmlinuz-linux {0} {1} {2}\n'.format(
            ruuid_str,
            cmdline_linux,
            cmdline_linux_default)

        pattern = re.compile("menuentry 'Antergos Linux'[\s\S]*initramfs-linux.img\n}")

        cfg = os.path.join(self.dest_dir, "boot/grub/grub.cfg")
        with open(cfg) as grub_file:
            parse = grub_file.read()

        if not self.settings.get('use_luks') and ruuid_str not in parse:
            entry = pattern.search(parse)
            if entry:
                logging.debug("Wrong uuid in grub.cfg, Cnchi will try to fix it.")
                new_entry = re.sub(
                    "linux\t/vmlinuz.*quiet\n",
                    boot_command,
                    entry.group())
                parse = parse.replace(entry.group(), new_entry)

                with open(cfg, 'w') as grub_file:
                    grub_file.write(parse)

    def modify_grub_default(self):
        """ If using LUKS as root, we need to modify GRUB_CMDLINE_LINUX
            GRUB_CMDLINE_LINUX : Command-line arguments to add to menu entries
            for the Linux kernel.
            GRUB_CMDLINE_LINUX_DEFAULT : Unless ‘GRUB_DISABLE_RECOVERY’ is set
            to ‘true’, two menu entries will be generated for each Linux kernel:
            one default entry and one entry for recovery mode. This option lists
            command-line arguments to add only to the default menu entry, after
            those listed in ‘GRUB_CMDLINE_LINUX’. """

        plymouth_bin = os.path.join(self.dest_dir, "usr/bin/plymouth")
        cmd_linux_default = "quiet"
        cmd_linux = ""

        # https://www.kernel.org/doc/Documentation/kernel-parameters.txt
        # cmd_linux_default : quiet splash resume=UUID=ABC zfs=ABC

        if os.path.exists(plymouth_bin):
            cmd_linux_default += " splash"

        # resume does not work in zfs (or so it seems)
        if "swap" in self.uuids and not self.settings.get("zfs"):
            cmd_linux_default += " resume=UUID={0}".format(self.uuids["swap"])

        if self.settings.get("zfs"):
            zfs_pool_name = self.settings.get("zfs_pool_name")
            cmd_linux += " zfs={0}".format(zfs_pool_name)

        if self.settings.get('use_luks'):
            # When using separate boot partition,
            # add GRUB_ENABLE_CRYPTODISK to grub.cfg
            if self.uuids["/"] != self.uuids["/boot"]:
                self.set_grub_option("GRUB_ENABLE_CRYPTODISK", "y")

            # Let GRUB automatically add the kernel parameters for
            # root encryption
            luks_root_volume = self.settings.get('luks_root_volume')
            logging.debug("Luks Root Volume: %s", luks_root_volume)

            if (self.settings.get("partition_mode") == "advanced" and
                    self.settings.get('use_luks_in_root')):
                # In advanced, if using luks in root device,
                # we store root device it in luks_root_device var
                root_device = self.settings.get('luks_root_device')
                self.uuids["/"] = fs.get_uuid(root_device)

            cmd_linux += " cryptdevice=/dev/disk/by-uuid/{0}:{1}".format(
                self.uuids["/"],
                luks_root_volume)

            if self.settings.get("luks_root_password") == "":
                # No luks password, so user wants to use a keyfile
                cmd_linux += " cryptkey=/dev/disk/by-uuid/{0}:ext2:/.keyfile-root".format(
                    self.uuids["/boot"])

        # Remove leading/ending spaces
        cmd_linux_default = cmd_linux_default.strip()
        cmd_linux = cmd_linux.strip()

        # Modify /etc/default/grub
        self.set_grub_option("GRUB_THEME", "/boot/grub/themes/Antergos-Default/theme.txt")
        self.set_grub_option("GRUB_DISTRIBUTOR", "Antergos")
        self.set_grub_option("GRUB_CMDLINE_LINUX_DEFAULT", cmd_linux_default)
        self.set_grub_option("GRUB_CMDLINE_LINUX", cmd_linux)

        # Also store grub line in settings, we'll use it later in check_root_uuid_in_grub()
        try:
            self.settings.set('GRUB_CMDLINE_LINUX', cmd_linux)
        except AttributeError:
            pass

        logging.debug("Grub configuration completed successfully.")

    def set_grub_option(self, option, cmd):
        """ Changes a grub setup option in /etc/default/grub """
        try:
            default_grub_path = os.path.join(self.dest_dir, "etc/default", "grub")
            default_grub_lines = []

            with open(default_grub_path, 'r', newline='\n') as grub_file:
                default_grub_lines = [x for x in grub_file.readlines()]

            with open(default_grub_path, 'w', newline='\n') as grub_file:
                param_in_file = False
                param_to_look_for = option + '='
                for line in default_grub_lines:
                    if param_to_look_for in line:
                        # Option was already in file, update it
                        line = '{0}="{1}"\n'.format(option, cmd)
                        param_in_file = True
                    grub_file.write(line)

                if not param_in_file:
                    # Option was not found. Thus, append new option
                    grub_file.write('\n{0}="{1}"\n'.format(option, cmd))

            logging.debug('Set %s="%s" in /etc/default/grub', option, cmd)
        except FileNotFoundError as ex:
            logging.error(ex)
        except Exception as ex:
            tpl1 = "Can't modify {0}".format(default_grub_path)
            tpl2 = "An exception of type {0} occured. Arguments:\n{1!r}"
            template = '{0} {1}'.format(tpl1, tpl2)
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)

    def prepare_grub_d(self):
        """ Copies 10_antergos script into /etc/grub.d/ """
        grub_d_dir = os.path.join(self.dest_dir, "etc/grub.d")
        script_dir = os.path.join(self.settings.get("cnchi"), "scripts")
        script = "10_antergos"

        os.makedirs(grub_d_dir, mode=0o755, exist_ok=True)

        script_path = os.path.join(script_dir, script)
        if os.path.exists(script_path):
            try:
                shutil.copy2(script_path, grub_d_dir)
                os.chmod(os.path.join(grub_d_dir, script), 0o755)
            except FileNotFoundError:
                logging.debug("Could not copy %s to grub.d", script)
            except FileExistsError:
                pass
        else:
            logging.warning("Can't find script %s", script_path)

    def run_mkconfig(self):
        """ Create grub.cfg file using grub-mkconfig """
        logging.debug("Generating grub.cfg...")

        # Make sure that /dev and others are mounted (binded).
        special_dirs.mount(self.dest_dir)

        # Add -l option to os-prober's umount call so that it does not hang
        self.apply_osprober_patch()
        logging.debug("Running grub-mkconfig...")
        locale = self.settings.get("locale")
        cmd = 'LANG={0} grub-mkconfig -o /boot/grub/grub.cfg'.format(locale)
        cmd_sh = ['sh', '-c', cmd]
        if not chroot_call(cmd_sh, self.dest_dir, timeout=300):
            msg = ("grub-mkconfig does not respond. Killing grub-mount and"
                   "os-prober so we can continue.")
            logging.error(msg)
            call(['killall', 'grub-mount'])
            call(['killall', 'os-prober'])

    def install_bios(self):
        """ Install Grub2 bootloader in a BIOS system """
        grub_location = self.settings.get('bootloader_device')
        txt = _("Installing GRUB(2) BIOS boot loader in {0}").format(grub_location)
        logging.info(txt)

        # /dev and others need to be mounted (binded).
        # We call mount_special_dirs here just to be sure
        special_dirs.mount(self.dest_dir)

        grub_install = ['grub-install',
                        '--directory=/usr/lib/grub/i386-pc',
                        '--target=i386-pc',
                        '--boot-directory=/boot',
                        '--recheck']

        # Use --force when installing in /dev/sdXY or in /dev/mmcblk
        if len(grub_location) > len("/dev/sdX"):
            grub_install.append("--force")

        grub_install.append(grub_location)

        chroot_call(grub_install, self.dest_dir)

        self.install_locales()

        self.run_mkconfig()

        grub_cfg_path = os.path.join(self.dest_dir, "boot/grub/grub.cfg")
        with open(grub_cfg_path) as grub_cfg:
            if "Antergos" in grub_cfg.read():
                txt = _("GRUB(2) BIOS has been successfully installed.")
                logging.info(txt)
                self.settings.set('bootloader_installation_successful', True)
            else:
                txt = _("ERROR installing GRUB(2) BIOS.")
                logging.warning(txt)
                self.settings.set('bootloader_installation_successful', False)

    def install_efi(self):
        """ Install Grub2 bootloader in a UEFI system """
        uefi_arch = "x86_64"
        spec_uefi_arch = "x64"
        spec_uefi_arch_caps = "X64"
        fpath = '/install/boot/efi/EFI/antergos_grub'
        bootloader_id = 'antergos_grub' if not os.path.exists(fpath) else \
            'antergos_grub_{0}'.format(random_generator())

        # grub2 in efi needs efibootmgr
        if not os.path.exists("/usr/bin/efibootmgr"):
            txt = _("Please install efibootmgr package to install Grub2 for x86_64-efi platform.")
            logging.warning(txt)
            txt = _("GRUB(2) will NOT be installed")
            logging.warning(txt)
            self.settings.set('bootloader_installation_successful', False)
            return

        txt = _("Installing GRUB(2) UEFI {0} boot loader").format(uefi_arch)
        logging.info(txt)

        grub_install = [
            'grub-install',
            '--target={0}-efi'.format(uefi_arch),
            '--efi-directory=/install/boot/efi',
            '--bootloader-id={0}'.format(bootloader_id),
            '--boot-directory=/install/boot',
            '--recheck']
        load_module = ['modprobe', '-a', 'efivarfs']

        call(load_module, timeout=15)
        call(grub_install, timeout=120)

        self.install_locales()

        # Copy grub into dirs known to be used as default by some OEMs
        # if they do not exist yet.
        grub_defaults = [
            os.path.join(
                self.dest_dir,
                "boot/efi/EFI/BOOT",
                "BOOT{0}.efi".format(spec_uefi_arch_caps)),
            os.path.join(
                self.dest_dir,
                "boot/efi/EFI/Microsoft/Boot",
                "bootmgfw.efi")]

        grub_path = os.path.join(
            self.dest_dir,
            "boot/efi/EFI/antergos_grub",
            "grub{0}.efi".format(spec_uefi_arch))

        for grub_default in grub_defaults:
            path = grub_default.split()[0]
            if not os.path.exists(path):
                msg = _("No OEM loader found in %s. Copying Grub(2) into dir.")
                logging.info(msg, path)
                os.makedirs(path, mode=0o755)
                msg_failed = _("Copying Grub(2) into OEM dir failed: %s")
                try:
                    shutil.copy(grub_path, grub_default)
                except FileNotFoundError:
                    logging.warning(msg_failed, _("File not found."))
                except FileExistsError:
                    logging.warning(msg_failed, _("File already exists."))
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    logging.error(message)

        self.run_mkconfig()

        paths = [
            os.path.join(self.dest_dir, "boot/grub/x86_64-efi/core.efi"),
            os.path.join(
                self.dest_dir,
                "boot/efi/EFI/{0}".format(bootloader_id),
                "grub{0}.efi".format(spec_uefi_arch))]

        exists = True
        for path in paths:
            if not os.path.exists(path):
                exists = False
                logging.debug("Path '%s' doesn't exist, when it should", path)

        if exists:
            logging.info("GRUB(2) UEFI install completed successfully")
            self.settings.set('bootloader_installation_successful', True)
        else:
            logging.warning("GRUB(2) UEFI install may not have completed successfully.")
            self.settings.set('bootloader_installation_successful', False)

    def apply_osprober_patch(self):
        """ Adds -l option to os-prober's umount call so that it does not hang """
        osp_path = os.path.join(
            self.dest_dir,
            "usr/lib/os-probes/50mounted-tests")
        if os.path.exists(osp_path):
            with open(osp_path) as osp:
                text = osp.read().replace("umount", "umount -l")
            with open(osp_path, 'w') as osp:
                osp.write(text)
            logging.debug("50mounted-tests file patched successfully")
        else:
            logging.warning("Failed to patch 50mounted-tests, file not found.")

    def install_locales(self):
        """ Install Grub2 locales """
        logging.debug("Installing Grub2 locales.")
        dest_locale_dir = os.path.join(self.dest_dir, "boot/grub/locale")

        os.makedirs(dest_locale_dir, mode=0o755, exist_ok=True)

        grub_mo = os.path.join(
            self.dest_dir,
            "usr/share/locale/en@quot/LC_MESSAGES/grub.mo")

        try:
            shutil.copy2(grub_mo, os.path.join(dest_locale_dir, "en.mo"))
        except FileNotFoundError:
            logging.warning("Can't install GRUB(2) locale.")
        except FileExistsError:
            # Ignore if already exists
            pass

if __name__ == '__main__':
    os.makedirs("/install/etc/default", mode=0o755, exist_ok=True)
    shutil.copy2("/etc/default/grub", "/install/etc/default/grub")
    dest_dir = "/install"
    settings = {}
    settings["zfs"] = True
    settings["zfs_pool_name"] = "Antergos_d3sq"
    settings["use_luks"] = True
    uuids = {}
    uuids["/"] = "ABCD"
    uuids["/boot"] = "ZXCV"
    grub2 = Grub2(dest_dir, settings, uuids)
    grub2.modify_grub_default()
