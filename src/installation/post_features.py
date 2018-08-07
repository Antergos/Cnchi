#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# post_features.py
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

""" Features post installation """

import logging
import os
import shutil
import tempfile

from installation import firewall
from installation import services as srv
import misc.extra as misc

class PostFeatures():
    """ Manages post installation of selected features """
    def __init__(self, dest_dir, settings):
        self.dest_dir = dest_dir
        self.settings = settings

    def setup(self):
        """ Do all set up needed by the user's selected features """
        services = []
        masked = []

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

        if self.settings.get('feature_lts'):
            self.set_kernel_lts()

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

        if self.settings.get("feature_energy"):
            # tlp
            services.extend(['tlp.service', 'tlp-sleep.service'])
            masked.extend(['systemd-rfkill.service', 'systemd-rfkill.socket'])
            # thermald
            services.append('thermald')

        srv.mask_services(masked)
        srv.enable_services(services)

    def read_file_from_install(self, path):
        """ Read file from new installation /install """
        lines = []
        path = os.path.join(self.dest_dir, path)
        try:
            with open(path) as grub_cfg:
                lines = grub_cfg.readlines()
        except OSError as err:
            logging.error("Couldn't read %s file: %s", path, err)
        return lines

    def set_kernel_lts(self):
        """ Sets LTS kernel as default when booting """
        bootloader = self.settings.get('bootloader')
        if bootloader == 'grub':
            self.set_kernel_lts_grub()
        elif bootloader == 'systemd-boot':
            self.set_kernel_lts_systemdboot()
        elif bootloader == 'refind':
            self.set_kernel_lts_refind()
        else:
            logging.warning("Unknown bootloader '%s'", bootloader)

    def set_kernel_lts_grub(self):
        """ Sets LTS kernel as default in Grub """
        # Get menu options
        path = 'boot/grub.cfg'
        lines = self.read_file_from_install(path)

        menu_entries = []
        index = 0
        for line in lines:
            if line.startswith('menuentry'):
                title = line.split("'")[1]
                menu_entries.append((index, title))

        new_default = ""
        for menu_entry in menu_entries:
            index, title = menu_entry
            if 'linux-lts' in title and 'recovery' not in title:
                new_default = index
                break

        if new_default:
            path = 'etc/default/grub'
            lines = self.read_file_from_install(path)
            path = os.path.join(self.dest_dir, path)
            with open(path, 'wt') as grub_file:
                for line in lines:
                    if "GRUB_DEFAULT" in line:
                        line = "GRUB_DEFAULT={}".format(new_default)
                    grub_file.write(line + '\n')

    def set_kernel_lts_systemdboot(self):
        """ TODO """
        pass

    def set_kernel_lts_refind(self):
        """ TODO """
        pass

    @staticmethod
    def enable_aur_in_pamac():
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
