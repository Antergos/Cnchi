#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# select_packages.py
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

""" Package list generation module. """

import logging
import os
import subprocess
import requests
from requests.exceptions import RequestException

import xml.etree.cElementTree as elementTree

import desktop_info

import pacman.pac as pac

from misc.events import Events
import misc.extra as misc
from misc.extra import InstallError

import hardware.hardware as hardware

from lembrame.lembrame import Lembrame

import i18n_packages

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message


class SelectPackages():
    """ Package list creation class """

    PKGLIST_URL = 'https://raw.githubusercontent.com/Antergos/Cnchi/master/data/packages.xml'

    def __init__(self, settings, callback_queue):
        """ Initialize package class """

        self.events = Events(callback_queue)
        self.settings = settings
        self.desktop = self.settings.get('desktop')

        # Packages to be removed
        self.conflicts = []

        # Packages to be installed
        self.packages = []

        self.vbox = False

        self.xml_root = None

        # If Lembrame enabled set pacman.conf pointing to the decrypted folder
        if self.settings.get('feature_lembrame'):
            self.lembrame = Lembrame(self.settings)
            path = os.path.join(self.lembrame.config.folder_file_path, 'pacman.conf')
            self.settings.set('pacman_config_file', path)

    def create_package_list(self):
        """ Create package list """

        # Common vars
        self.packages = []

        logging.debug("Refreshing pacman databases...")
        self.refresh_pacman_databases()
        logging.debug("Pacman ready")

        logging.debug("Selecting packages...")
        self.select_packages()
        logging.debug("Packages selected")

        # Fix bug #263 (v86d moved from [extra] to AUR)
        if "v86d" in self.packages:
            self.packages.remove("v86d")
            logging.debug("Removed 'v86d' package from list")

        if self.vbox:
            self.settings.set('is_vbox', True)

    @misc.raise_privileges
    def refresh_pacman_databases(self):
        """ Updates pacman databases """
        # Init pyalpm
        try:
            pacman = pac.Pac(self.settings.get('pacman_config_file'), self.events.queue)
        except Exception as ex:
            template = (
                "Can't initialize pyalpm. An exception of type {0} occured. Arguments:\n{1!r}")
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            raise InstallError(message)

        # Refresh pacman databases
        if not pacman.refresh():
            logging.error("Can't refresh pacman databases.")
            txt = _("Can't refresh pacman databases.")
            raise InstallError(txt)

        try:
            pacman.release()
            del pacman
        except Exception as ex:
            template = (
                "Can't release pyalpm. An exception of type {0} occured. Arguments:\n{1!r}")
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            raise InstallError(message)

    def add_package(self, pkg):
        """ Adds xml node text to our package list
            returns TRUE if the package is added """
        libs = desktop_info.LIBS

        arch = pkg.attrib.get('arch')
        if arch and arch != os.uname()[-1]:
            return False

        lang = pkg.attrib.get('lang')
        locale = self.settings.get("locale").split('.')[0][:2]
        if lang and lang != locale:
            return False

        lib = pkg.attrib.get('lib')
        if lib and self.desktop not in libs[lib]:
            return False

        desktops = pkg.attrib.get('desktops')
        if desktops and self.desktop not in desktops:
            return False

        # If package is a Desktop Manager or a Network Manager,
        # save the name to activate the correct service later
        if pkg.attrib.get('dm'):
            self.settings.set("desktop_manager", pkg.attrib.get('name'))
        if pkg.attrib.get('nm'):
            self.settings.set("network_manager", pkg.attrib.get('name'))

        # check conflicts attrib
        conflicts = pkg.attrib.get('conflicts')
        if conflicts:
            self.add_conflicts(pkg.attrib.get('conflicts'))

        # finally, add package
        self.packages.append(pkg.text)
        return True

    def load_xml_local(self, xml_filename):
        """ Load xml packages list from file name """
        self.events.add('info', _("Reading local package list..."))
        if os.path.exists(xml_filename):
            logging.debug("Loading %s", xml_filename)
            xml_tree = elementTree.parse(xml_filename)
            self.xml_root = xml_tree.getroot()
        else:
            logging.warning("Cannot find %s file", xml_filename)

    def load_xml_remote(self):
        """ Load xml packages list from url """
        self.events.add('info', _("Getting online package list..."))
        url = SelectPackages.PKGLIST_URL
        logging.debug("Getting url %s...", url)
        try:
            req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            self.xml_root = elementTree.fromstring(req.content)
        except RequestException as url_error:
            msg = "Can't retrieve remote package list: {}".format(
                url_error)
            logging.warning(msg)

    def load_xml_root_node(self):
        """ Loads xml data, storing the root node """
        self.xml_root = None

        alternate_package_list = self.settings.get('alternate_package_list')
        if alternate_package_list:
            # Use file passed by parameter (overrides server one)
            self.load_xml_local(alternate_package_list)

        if self.xml_root is None:
            # The list of packages is retrieved from an online XML to let us
            # control the pkgname in case of any modification
            self.load_xml_remote()

        if self.xml_root is None:
            # If the installer can't retrieve the remote file Cnchi will use
            # a local copy, which might be updated or not.
            xml_filename = os.path.join(self.settings.get('data'), 'packages.xml')
            self.load_xml_local(xml_filename)

        if self.xml_root is None:
            txt = "Could not load packages XML file (neither local nor from the Internet)"
            logging.error(txt)
            txt = _("Could not load packages XML file (neither local nor from the Internet)")
            raise InstallError(txt)

    def add_drivers(self):
        """ Add package drivers """
        try:
            # Detect which hardware drivers are needed
            hardware_install = hardware.HardwareInstall(
                self.settings.get('cnchi'),
                self.settings.get('feature_graphic_drivers'))
            driver_names = hardware_install.get_found_driver_names()
            if driver_names:
                logging.debug(
                    "Hardware module detected these drivers: %s",
                    driver_names)

            # Add needed hardware packages to our list
            hardware_pkgs = hardware_install.get_packages()
            if hardware_pkgs:
                logging.debug(
                    "Hardware module added these packages: %s",
                    ", ".join(hardware_pkgs))
                if 'virtualbox' in hardware_pkgs:
                    self.vbox = True
                self.packages.extend(hardware_pkgs)

            # Add conflicting hardware packages to our conflicts list
            self.conflicts.extend(hardware_install.get_conflicts())
        except Exception as ex:
            template = (
                "Error in hardware module. An exception of type {0} occured. Arguments:\n{1!r}")
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)

    def add_filesystems(self):
        """ Add filesystem packages """
        logging.debug("Adding filesystem packages")
        for child in self.xml_root.iter("filesystems"):
            for pkg in child.iter('pkgname'):
                self.add_package(pkg)

        # Add ZFS filesystem
        if self.settings.get('zfs'):
            logging.debug("Adding zfs packages")
            for child in self.xml_root.iter("zfs"):
                for pkg in child.iter('pkgname'):
                    self.add_package(pkg)

    def maybe_add_bootloader(self):
        """ Add bootloader packages if needed """
        if self.settings.get('bootloader_install'):
            boot_loader = self.settings.get('bootloader')
            bootloader_found = False
            for child in self.xml_root.iter('bootloader'):
                if child.attrib.get('name') == boot_loader:
                    txt = _("Adding '%s' bootloader packages")
                    logging.debug(txt, boot_loader)
                    bootloader_found = True
                    for pkg in child.iter('pkgname'):
                        self.add_package(pkg)
            if not bootloader_found:
                logging.warning(
                    "Couldn't find %s bootloader packages!", boot_loader)

    def add_edition_packages(self):
        """ Add common and specific edition packages """
        for editions in self.xml_root.iter('editions'):
            for edition in editions.iter('edition'):
                name = edition.attrib.get('name').lower()

                # Add common packages to all desktops (including base)
                if name == 'common':
                    for pkg in edition.iter('pkgname'):
                        self.add_package(pkg)

                # Add common graphical packages (not if installing 'base')
                if name == 'graphic' and self.desktop != 'base':
                    for pkg in edition.iter('pkgname'):
                        self.add_package(pkg)

                # Add specific desktop packages
                if name == self.desktop:
                    logging.debug("Adding %s desktop packages", self.desktop)
                    for pkg in edition.iter('pkgname'):
                        self.add_package(pkg)

    def maybe_add_vbox_packages(self):
        """ Adds specific virtualbox packages if running inside a VM """
        if self.vbox:
            # Add virtualbox-guest-utils-nox package if 'base' is installed in a vbox vm
            if self.desktop == 'base':
                self.packages.append('virtualbox-guest-utils-nox')

            # Add linux-lts-headers if LTS kernel is installed in a vbox vm
            if self.settings.get('feature_lts'):
                self.packages.append('linux-lts-headers')

    def select_packages(self):
        """ Get package list from the Internet and add specific packages to it """
        self.packages = []

        # Load package list
        self.load_xml_root_node()

        # Add common and desktop specific packages
        self.add_edition_packages()

        # Add drivers' packages
        self.add_drivers()

        # Add file system packages
        self.add_filesystems()

        # Add asian fonts (if necessary)
        self.maybe_add_asian_fonts()

        # Add bootloader (if user chose it)
        self.maybe_add_bootloader()

        # Add extra virtualbox packages (if needed)
        self.maybe_add_vbox_packages()

        # Check for user desired features and add them to our installation
        logging.debug(
            "Check for user desired features and add them to our installation")
        self.add_features()
        logging.debug("All features needed packages have been added")

        # Add Lembrame packages but install Cnchi defaults too
        # TODO: Lembrame has to generate a better package list indicating DM and stuff
        if self.settings.get("feature_lembrame"):
            self.events.add('info', _("Appending list of packages from Lembrame"))
            self.packages = self.packages + self.lembrame.get_pacman_packages()

        # Remove duplicates and conflicting packages
        self.cleanup_packages_list()
        logging.debug("Packages list: %s", ','.join(self.packages))

        # Check if all packages ARE in the repositories
        # This is done mainly to avoid errors when Arch removes a package silently
        self.check_packages()

    def check_packages(self):
        """ Checks that all selected packages ARE in the repositories """
        not_found = []
        self.events.add('percent', 0)
        self.events.add('info', _("Checking that all selected packages are available online..."))
        num_pkgs = len(self.packages)
        for index, pkg_name in enumerate(self.packages):
            # TODO: Use libalpm instead
            cmd = ["/usr/bin/pacman", "-Ss", pkg_name]
            try:
                output = subprocess.check_output(cmd).decode()
            except subprocess.CalledProcessError:
                output = ""

            if pkg_name not in output:
                not_found.append(pkg_name)
                logging.error("Package %s...NOT FOUND!", pkg_name)

            percent = (index + 1) / num_pkgs
            self.events.add('percent', percent)

        if not_found:
            txt = _("Cannot find these packages: {}").format(', '.join(not_found))
            raise misc.InstallError(txt)

    def cleanup_packages_list(self):
        """ Cleans up a bit our packages list """
        # Remove duplicates
        self.packages = list(set(self.packages))
        self.conflicts = list(set(self.conflicts))

        # Check the list of packages for empty strings and remove any that we find.
        self.packages = [pkg for pkg in self.packages if pkg != '']
        self.conflicts = [pkg for pkg in self.conflicts if pkg != '']

        # Remove any package from self.packages that is already in self.conflicts
        if self.conflicts:
            logging.debug("Conflicts list: %s", ", ".join(self.conflicts))
            for pkg in self.conflicts:
                if pkg in self.packages:
                    self.packages.remove(pkg)

    def add_conflicts(self, conflicts):
        """ Maintains a list of conflicting packages """
        if conflicts:
            if ',' in conflicts:
                for conflict in conflicts.split(','):
                    conflict = conflict.rstrip()
                    if conflict not in self.conflicts:
                        self.conflicts.append(conflict)
            else:
                self.conflicts.append(conflicts)

    def maybe_add_asian_fonts(self):
        """ Add chinese, japanese and korean fonts if necessary """
        locale = self.settings('locale')
        if locale.endswith('.UTF-8'):
            locale = locale.split('.')[0]
        if locale in ['zh_TW', 'zh_CN']:
            logging.debug("Adding chinese fonts packages (%s)", locale)
            for child in self.xml_root.iter('chinese'):
                for pkg in child.iter('pkgname'):
                    self.add_package(pkg)
        if locale in ['zh_TW', 'zh_CN', 'ja_JP', 'ko_KR']:
            logging.debug("Adding cjk font packages (%s)", locale)
            for child in self.xml_root.iter('cjk'):
                for pkg in child.iter('pkgname'):
                    self.add_package(pkg)

    def add_features(self):
        """ Selects packages based on user selected features """
        for xml_features in self.xml_root.iter('features'):
            for xml_feature in xml_features.iter('feature'):
                feature = xml_feature.attrib.get("name")

                # If LEMP is selected, do not install lamp even if it's selected
                if feature == "lamp" and self.settings.get("feature_lemp"):
                    continue

                # Add packages from each feature
                if self.settings.get("feature_" + feature):
                    logging.debug("Adding packages for '%s' feature.", feature)
                    for pkg in xml_feature.iter('pkgname'):
                        if self.add_package(pkg):
                            logging.debug(
                                "Selecting package %s for feature %s",
                                pkg.text,
                                feature)

        # Prepare i18n packages class
        i18n_pkgs = i18n_packages.I18NPackages(
            self.settings.get('locale'),
            self.settings.get('data'))

        # Add firefox language package
        if self.settings.get('feature_firefox'):
            pkg = i18n_pkgs.firefox()
            if pkg:
                self.packages.append(pkg)

        # Add libreoffice language package
        if self.settings.get('feature_office'):
            pkg = i18n_pkgs.libreoffice()
            if pkg:
                self.packages.append(pkg)

        # Always add a hunspell dictionary if available
        pkg = i18n_pkgs.hunspell()
        if pkg:
            self.packages.append(pkg)
