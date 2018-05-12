#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# post_install.py
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

""" Post-Installation process module. """

import crypt
import logging
import os
import queue
import shutil
import time
import re
import tempfile

import desktop_info
#import encfs

from installation import mkinitcpio
from installation import firewall

from installation.boot import loader

import misc.extra as misc
from misc.run_cmd import call, chroot_call

import parted3.fs_module as fs

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

DEST_DIR = "/install"

class PostInstallation(object):
    """ Post-Installation process thread class """
    POSTINSTALL_SCRIPT = 'postinstall.sh'

    def __init__(
            self,
            settings,
            callback_queue,
            mount_devices,
            fs_devices,
            ssd=None,
            blvm=False):

        """ Initialize installation class """
        self.settings = settings
        self.callback_queue = callback_queue

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

        self.virtual_box = self.settings.get('is_vbox')


    def queue_event(self, event_type, event_text=""):
        """ Enqueue a new event """
        if self.callback_queue:
            try:
                self.callback_queue.put_nowait((event_type, event_text))
            except queue.Full:
                pass

    def copy_logs(self):
        """ Copy Cnchi logs to new installation """
        log_dest_dir = os.path.join(DEST_DIR, "var/log/cnchi")
        os.makedirs(log_dest_dir, mode=0o755, exist_ok=True)

        datetime = "{0}-{1}".format(time.strftime("%Y%m%d"),
                                    time.strftime("%H%M%S"))

        file_names = ["cnchi", "postinstall", "pacman"]

        for name in file_names:
            src = os.path.join("/tmp", "{0}.log".format(name))
            dst = os.path.join(
                log_dest_dir, "{0}-{1}.log".format(name, datetime))
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

    @staticmethod
    def copy_network_config():
        """ Copies Network Manager configuration """
        source_nm = "/etc/NetworkManager/system-connections/"
        target_nm = os.path.join(
            DEST_DIR, "etc/NetworkManager/system-connections")

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
                    logging.warning(
                        "Can't copy network configuration files, file %s not found", source_network)
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
                if luks_root_password:
                    # Use password and not a keyfile
                    home_keyfile = "none"
                else:
                    # Use a keyfile
                    home_keyfile = "/etc/luks-keys/home"

                os.chmod(crypttab_path, 0o666)
                with open(crypttab_path, 'a') as crypttab_file:
                    line = "cryptAntergosHome /dev/disk/by-uuid/{0} {1} luks\n".format(
                        uuid, home_keyfile)
                    crypttab_file.write(line)
                    logging.debug("Added %s to crypttab", line)
                os.chmod(crypttab_path, 0o600)

                # Add line to fstab
                txt = "/dev/mapper/cryptAntergosHome {0} {1} defaults 0 0".format(
                    mount_point, myfmt)
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
                if luks_uuid:
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
                if mount_point:
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
        """ Copies udev rule for SSDs """
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
        shadow_password = crypt.crypt(new_password, crypt.mksalt())
        chroot_call(['usermod', '-p', shadow_password, user])

    @staticmethod
    def auto_timesetting():
        """ Set hardware clock """
        cmd = ["hwclock", "--systohc", "--utc"]
        call(cmd)
        try:
            shutil.copy2("/etc/adjtime", os.path.join(DEST_DIR, "etc/"))
        except FileNotFoundError:
            logging.warning("File /etc/adjtime not found!")
        except FileExistsError:
            pass


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
        """ Enables AUR searches in pamac config file """
        pamac_conf = "/etc/pamac.conf"
        if os.path.exists(pamac_conf):
            _fd, name = tempfile.mkstemp()
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

        # openssh comes with two kinds of systemd service files:
        # sshd.service, which will keep the SSH daemon permanently active and
        # fork for each incoming connection. It is especially suitable for systems
        # with a large amount of SSH traffic.
        # sshd.socket + sshd@.service, which spawn on-demand instances of the SSH
        # daemon per connection. Using it implies that systemd listens on the SSH
        # socket and will only start the daemon process for an incoming connection.
        # It is the recommended way to run sshd in almost all cases.
        if self.settings.get("feature_sshd"):
            services.append('sshd.socket')

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

        username = self.settings.get('user_name')
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
            "Master 70% unmute", "Front 70% unmute", "Side 70% unmute", "Surround 70% unmute",
            "Center 70% unmute", "LFE 70% unmute", "Headphone 70% unmute", "Speaker 70% unmute",
            "PCM 70% unmute", "Line 70% unmute", "External 70% unmute", "FM 50% unmute",
            "Master Mono 70% unmute", "Master Digital 70% unmute", "Analog Mix 70% unmute",
            "Aux 70% unmute", "Aux2 70% unmute", "PCM Center 70% unmute", "PCM Front 70% unmute",
            "PCM LFE 70% unmute", "PCM Side 70% unmute", "PCM Surround 70% unmute",
            "Playback 70% unmute", "PCM,1 70% unmute", "DAC 70% unmute", "DAC,0 70% unmute",
            "DAC,1 70% unmute", "Synth 70% unmute", "CD 70% unmute", "Wave 70% unmute",
            "Music 70% unmute", "AC97 70% unmute", "Analog Front 70% unmute",
            "VIA DXS,0 70% unmute", "VIA DXS,1 70% unmute", "VIA DXS,2 70% unmute",
            "VIA DXS,3 70% unmute", "Mic 70% mute", "IEC958 70% mute",
            "Master Playback Switch on", "Master Surround on",
            "SB Live Analog/Digital Output Jack off", "Audigy Analog/Digital Output Jack off"]

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
        if os.path.exists(fluid_path):
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
        path = os.path.join(DEST_DIR, "etc/xdg/autostart/user-dirs-update-gtk.desktop")
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
        # localectl set-x11-keymap es cat
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
        files = ["/etc/X11/xorg.conf.d/00-keyboard.conf", "/etc/vconsole.conf"]
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
                    logging.info(
                        "Installed zfs module's version: %s", zfs_version)
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
            PostInstallation.POSTINSTALL_SCRIPT)
        cmd = [
            "/usr/bin/bash",
            script_path_postinstall,
            self.settings.get('user_name'),
            DEST_DIR,
            self.desktop,
            self.settings.get("locale"),
            str(self.virtual_box),
            keyboard_layout]

        # Keyboard variant is optional
        if keyboard_variant:
            cmd.append(keyboard_variant)

        call(cmd, timeout=300)
        logging.debug("Post install script completed successfully.")

    @staticmethod
    def modify_makepkg():
        """
            Modify the makeflags to allow for threading.
            Use threads for xz compression.
        """
        makepkg_conf_path = os.path.join(DEST_DIR, 'etc/makepkg.conf')
        if os.path.exists(makepkg_conf_path):
            with open(makepkg_conf_path, 'r') as makepkg_conf:
                contents = makepkg_conf.readlines()
            with open(makepkg_conf_path, 'w') as makepkg_conf:
                for line in contents:
                    if '#MAKEFLAGS' in line:
                        line = 'MAKEFLAGS="-j$(nproc)"\n'
                    elif 'COMPRESSXZ' in line:
                        line = 'COMPRESSXZ=(xz -c -z - --threads=0)\n'
                    makepkg_conf.write(line)

    def setup_user(self):
        """ Set user parameters """

        username = self.settings.get('user_name')
        fullname = self.settings.get('user_fullname')
        password = self.settings.get('user_password')
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

        # Setup user

        default_groups = 'wheel'

        if self.virtual_box:
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
            '--create-home',
            '--shell', '/bin/bash',
            '--gid', 'users',
            '--groups', default_groups,
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

        ## Encrypt user's home directory if requested
        #if self.settings.get('encrypt_home'):
        #    self.queue_event('info', _("Encrypting user home dir..."))
        #    encfs.setup(username, DEST_DIR, password)
        #    logging.debug("User home dir encrypted")

    @staticmethod
    def nano_setup():
        """ Enable colors and syntax highlighting in nano editor """
        nanorc_path = os.path.join(DEST_DIR, 'etc/nanorc')
        if os.path.exists(nanorc_path):
            logging.debug(
                "Enabling colors and syntax highlighting in nano editor")
            with open(nanorc_path, 'a') as nanorc:
                nanorc.write('\n')
                nanorc.write('# Added by Cnchi (Antergos Installer)\n')
                nanorc.write('set titlecolor brightwhite,blue\n')
                nanorc.write('set statuscolor brightwhite,green\n')
                nanorc.write('set numbercolor cyan\n')
                nanorc.write('set keycolor cyan\n')
                nanorc.write('set functioncolor green\n')
                nanorc.write('include "/usr/share/nano/*.nanorc"\n')

    def rebuild_zfs_modules(self):
        """ Sometimes dkms tries to build the zfs module before spl. """
        self.queue_event('info', _("Building zfs modules..."))
        zfs_version = self.get_installed_zfs_version()
        spl_module = 'spl/{}'.format(zfs_version)
        zfs_module = 'zfs/{}'.format(zfs_version)
        kernel_versions = self.get_installed_kernel_versions()
        if kernel_versions:
            for kernel_version in kernel_versions:
                logging.debug(
                    "Installing zfs v%s modules for kernel %s", zfs_version, kernel_version)
                chroot_call(
                    ['dkms', 'install', spl_module, '-k', kernel_version])
                chroot_call(
                    ['dkms', 'install', zfs_module, '-k', kernel_version])
        else:
            # No kernel version found, try to install for current kernel
            logging.debug(
                "Installing zfs v%s modules for current kernel.", zfs_version)
            chroot_call(['dkms', 'install', spl_module])
            chroot_call(['dkms', 'install', zfs_module])

    def pamac_setup(self):
        """ Enable AUR in pamac if AUR feature selected """
        pamac_conf = os.path.join(DEST_DIR, 'etc/pamac.conf')
        if os.path.exists(pamac_conf) and self.settings.get('feature_aur'):
            logging.debug("Enabling AUR options in pamac")
            with open(pamac_conf, 'r') as pamac_conf_file:
                file_data = pamac_conf_file.read()
            file_data = file_data.replace("#EnableAUR", "EnableAUR")
            file_data = file_data.replace(
                "#SearchInAURByDefault", "SearchInAURByDefault")
            file_data = file_data.replace(
                "#CheckAURUpdates", "CheckAURUpdates")
            with open(pamac_conf, 'w') as pamac_conf_file:
                pamac_conf_file.write(file_data)

    @staticmethod
    def setup_timesyncd():
        """ Setups and enables time sync service """
        timesyncd_path = os.path.join(DEST_DIR, "etc/systemd/timesyncd.conf")
        try:
            with open(timesyncd_path, 'w') as timesyncd:
                timesyncd.write("[Time]\n")
                timesyncd.write("NTP=0.arch.pool.ntp.org 1.arch.pool.ntp.org "
                                "2.arch.pool.ntp.org 3.arch.pool.ntp.org\n")
                timesyncd.write("FallbackNTP=0.pool.ntp.org 1.pool.ntp.org "
                                "0.fr.pool.ntp.org\n")
        except FileNotFoundError as err:
            logging.warning("Can't find %s file: %s", timesyncd_path, err)
        chroot_call(['systemctl', '-fq', 'enable',
                     'systemd-timesyncd.service'])

    def configure_system(self, hardware_install):
        """ Final install steps.
            Set clock, language, timezone, run mkinitcpio,
            populate pacman keyring, setup systemd services, ... """

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
            self.setup_timesyncd()

        # Set timezone
        zone = self.settings.get("timezone_zone")
        if zone:
            zoneinfo_path = os.path.join("/usr/share/zoneinfo", zone)
            localtime_path = "/etc/localtime"
            chroot_call(['ln', '-sf', zoneinfo_path, localtime_path])
            logging.debug("Timezone set to %s", zoneinfo_path)
        else:
            logging.warning(
                "Can't read selected timezone! Will leave it to UTC.")

        # Wait FOREVER until the user sets his params
        # FIXME: We can wait here forever!
        while self.settings.get('user_info_done') is False:
            # Wait five seconds and try again
            time.sleep(5)

        # Configure detected hardware
        # NOTE: Because hardware can need extra repos, this code must run
        # always after having called the update_pacman_conf method
        if hardware_install:
            try:
                logging.debug("Running hardware drivers post-install jobs...")
                hardware_install.post_install(DEST_DIR)
            except Exception as ex:
                template = "Error in hardware module. " \
                    "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                logging.error(message)

        self.setup_user()

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
        # self.alsa_mixer_setup()
        #logging.debug("Updated Alsa mixer settings")

        # Set pulse
        # if os.path.exists(os.path.join(DEST_DIR, "usr/bin/pulseaudio-ctl")):
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
            self.rebuild_zfs_modules()

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

        # Install boot loader (always after running mkinitcpio)
        if self.settings.get('bootloader_install'):
            try:
                self.queue_event('info', _("Installing bootloader..."))
                boot_loader = loader.Bootloader(
                    DEST_DIR,
                    self.settings,
                    self.mount_devices)
                boot_loader.install()
            except Exception as ex:
                template = "Cannot install bootloader. " \
                    "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                logging.error(message)

        # Create an initial database for mandb (slow)
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

        # Install sonar (a11y) gsettings if present in the ISO (and a11y is on)
        src = "/usr/share/glib-2.0/schemas/92_antergos_sonar.gschema.override"
        if self.settings.get('a11y') and os.path.exists(src):
            dst = os.path.join(DEST_DIR, 'usr/share/glib-2.0/schemas')
            shutil.copy2(src, dst)

        # Enable AUR in pamac if AUR feature selected
        self.pamac_setup()

        # Apply makepkg tweaks upon install (issue #871)
        self.modify_makepkg()

        self.nano_setup()

        logging.debug("Setting .bashrc to load .bashrc.aliases")
        bashrc_files = ["etc/skel/.bashrc"]
        username = self.settings.get('user_name')
        bashrc_files.append("home/{}/.bashrc".format(username))
        for bashrc_file in bashrc_files:
            bashrc_file = os.path.join(DEST_DIR, bashrc_file)
            if os.path.exists(bashrc_file):
                with open(bashrc_file, 'a') as bashrc:
                    bashrc.write('\n')
                    bashrc.write('if [ -e ~/.bashrc.aliases ] ; then\n')
                    bashrc.write('   source ~/.bashrc.aliases\n')
                    bashrc.write('fi\n')

        # This must be done at the end of the installation when using zfs
        if self.method == "zfs":
            logging.debug("Installation done, exporting ZFS pool")
            pool_name = self.settings.get("zfs_pool_name")
            cmd = ["zpool", "export", "-f", pool_name]
            call(cmd)
