#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# select_packages.py
#
# Copyright © 2013-2017 Antergos
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
import queue
import sys
import requests
from requests.exceptions import RequestException

try:
    import xml.etree.cElementTree as eTree
except ImportError as err:
    import xml.etree.ElementTree as eTree

import desktop_info
import info


import pacman.pac as pac
import misc.extra as misc
from misc.extra import InstallError

import hardware.hardware as hardware

from lembrame.lembrame import Lembrame

DEST_DIR = "/install"
PKGLIST_URL = 'https://raw.githubusercontent.com/Antergos/Cnchi/master/data/packages.xml'


def write_file(filecontents, filename):
    """ writes a string of data to disk """
    os.makedirs(os.path.dirname(filename), mode=0o755, exist_ok=True)

    with open(filename, "w") as my_file:
        my_file.write(filecontents)


class SelectPackages(object):
    """ Package list creation class """

    def __init__(self, settings, callback_queue):
        """ Initialize package class """

        self.callback_queue = callback_queue
        self.settings = settings
        self.alternate_package_list = self.settings.get(
            'alternate_package_list')
        self.desktop = self.settings.get('desktop')
        self.zfs = self.settings.get('zfs')

        # Packages to be removed
        self.conflicts = []

        # Packages to be installed
        self.packages = []

        self.vbox = False
        self.my_arch = os.uname()[-1]

        # If Lembrame enabled set pacman.conf pointing to the decrypted folder
        if self.settings.get('feature_lembrame'):
            self.lembrame = Lembrame(self.settings)
            self.settings.set('pacman_config_file', self.lembrame.config.folder_file_path + '/pacman.conf')

    def queue_fatal_event(self, txt):
        """ Enqueues a fatal event and quits """
        self.queue_event('error', txt)
        # self.callback_queue.join()
        sys.exit(0)

    def queue_event(self, event_type, event_text=""):
        """ Enqueue event """
        if self.callback_queue is not None:
            try:
                self.callback_queue.put_nowait((event_type, event_text))
            except queue.Full:
                pass
        else:
            print("{0}: {1}".format(event_type, event_text))

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
            pacman = pac.Pac(self.settings.get('pacman_config_file'), self.callback_queue)
        except Exception as ex:
            template = "Can't initialize pyalpm. An exception of type {0} occured. Arguments:\n{1!r}"
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
            template = "Can't release pyalpm. An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            raise InstallError(message)

    def add_package(self, pkg):
        """ Adds xml node text to our package list
            returns TRUE if the package is added """
        libs = desktop_info.LIBS

        arch = pkg.attrib.get('arch')
        if arch and arch != self.my_arch:
            return False

        lang = pkg.attrib.get('lang')
        locale = self.settings.get("locale").split('.')[0][:2]
        if lang and lang != locale:
            return False

        lib = pkg.attrib.get('lib')
        if lib and not self.desktop in libs[lib]:
            return False

        desktops = pkg.attrib.get('desktops')
        if desktops and not self.desktop in desktops:
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

    def select_packages(self):
        """ Get package list from the Internet """
        self.packages = []
        packages_xml_data = None
        packages_xml_filename = None

        if len(self.alternate_package_list) > 0:
            # Use file passed by parameter (overrides server one)
            packages_xml_filename = self.alternate_package_list
        else:
            # The list of packages is retrieved from an online XML to let us
            # control the pkgname in case of any modification

            self.queue_event('info', _("Getting package list..."))

            try:
                # url = '{0}packages-{1}.xml'.format(PKGLIST_URL, info.CNCHI_VERSION.rsplit('.')[-2])
                url = PKGLIST_URL
                logging.debug("Getting url %s...", url)
                req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                packages_xml_data = req.content
            except RequestException as url_error:
                # If the installer can't retrieve the remote file Cnchi will use
                # a local copy, which might be updated or not.
                data_dir = self.settings.get("data")
                packages_xml_filename = os.path.join(data_dir, 'packages.xml')
                msg = "{0}. Can't retrieve remote package list, using the local file instead."
                msg = msg.format(url_error)
                if info.CNCHI_RELEASE_STAGE == "production":
                    logging.warning(msg)
                else:
                    logging.debug(msg)

        if packages_xml_data != None:
            logging.debug("Loading xml data from server...")
            xml_root = eTree.fromstring(packages_xml_data)
        else:
            logging.debug("Loading %s", packages_xml_filename)
            xml_tree = eTree.parse(packages_xml_filename)
            xml_root = xml_tree.getroot()

        for editions in xml_root.iter('editions'):
            for edition in editions.iter('edition'):
                name = edition.attrib.get("name").lower()

                # Add common packages to all desktops (including base)
                if name == "common":
                    for pkg in edition.iter('pkgname'):
                        self.add_package(pkg)

                # Add common graphical packages
                if name == "graphic" and self.desktop != "base":
                    for pkg in edition.iter('pkgname'):
                        self.add_package(pkg)

                # Add specific desktop packages
                if name == self.desktop:
                    logging.debug("Adding %s desktop packages", self.desktop)
                    for pkg in edition.iter('pkgname'):
                        self.add_package(pkg)

        # Set KDE language pack
        if self.desktop == 'kde':
            pkg_text = ""
            base_name = 'kde-l10n-'
            lang_name = self.settings.get("language_name").lower()
            if lang_name == "english":
                # There're some English variants available but not all of them.
                lang_packs = ['en_gb']
                locale = self.settings.get('locale').split('.')[0].lower()
                if locale in lang_packs:
                    pkg_text = base_name + locale
            else:
                # All the other language packs use their language code
                lang_code = self.settings.get('language_code').lower()
                pkg_text = base_name + lang_code
            if pkg_text:
                logging.debug("Selected kde language pack: %s", pkg_text)
                self.packages.append(pkg_text)

        try:
            # Detect which hardware drivers are needed
            hardware_install = hardware.HardwareInstall(
                use_proprietary_graphic_drivers=self.settings.get('feature_graphic_drivers'))
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
            template = "Error in hardware module. An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)

        # Add virtualbox-guest-utils-nox if "base" is installed in a vbox vm
        if self.vbox and self.desktop == "base":
            self.packages.append("virtualbox-guest-utils-nox")

        # Add linux-lts-headers if LTS kernel is installed in a vbox vm
        # only if not already appended
        if self.vbox and self.settings.get('feature_lts'):
            if "linux-lts-headers" not in self.packages:
                self.packages.append("linux-lts-headers")

        # Add filesystem packages
        logging.debug("Adding filesystem packages")
        for child in xml_root.iter("filesystems"):
            for pkg in child.iter('pkgname'):
                self.add_package(pkg)

        # Add ZFS filesystem
        if self.zfs:
            logging.debug("Adding zfs packages")
            for child in xml_root.iter("zfs"):
                for pkg in child.iter('pkgname'):
                    self.add_package(pkg)

        # Add chinese fonts
        lang_code = self.settings.get("language_code")
        if lang_code in ["zh_TW", "zh_CN"]:
            logging.debug("Selecting chinese fonts.")
            for child in xml_root.iter('chinese'):
                for pkg in child.iter('pkgname'):
                    self.add_package(pkg)

        # Add bootloader packages if needed
        if self.settings.get('bootloader_install'):
            boot_loader = self.settings.get('bootloader')
            # Search boot_loader in packages.xml
            bootloader_found = False
            for child in xml_root.iter('bootloader'):
                if child.attrib.get('name') == boot_loader:
                    txt = _("Adding '%s' bootloader packages")
                    logging.debug(txt, boot_loader)
                    bootloader_found = True
                    for pkg in child.iter('pkgname'):
                        self.add_package(pkg)
            if not bootloader_found and boot_loader != 'gummiboot':
                txt = _("Couldn't find %s bootloader packages!")
                logging.warning(txt, boot_loader)

        # Check for user desired features and add them to our installation
        logging.debug(
            "Check for user desired features and add them to our installation")
        self.add_features_packages(xml_root)
        logging.debug("All features needed packages have been added")

        # Add Lembrame packages but install Cnchi defaults too
        # TODO: Lembrame has to generate a better package list indicating DM and stuff
        if self.settings.get("feature_lembrame"):
            self.queue_event('info', _("Appending list of packages from Lembrame"))
            self.packages = self.packages + self.lembrame.get_pacman_packages()

        # Remove duplicates
        self.packages = list(set(self.packages))
        self.conflicts = list(set(self.conflicts))

        # Check the list of packages for empty strings and remove any that we find.
        self.packages = [pkg for pkg in self.packages if pkg != '']
        self.conflicts = [pkg for pkg in self.conflicts if pkg != '']

        # Remove any package from self.packages that is already in self.conflicts
        if self.conflicts:
            logging.debug("Conflicts list: %s", ", ".join(self.conflicts))
            for pkg in self.packages:
                if pkg in self.conflicts:
                    self.packages.remove(pkg)

        logging.debug("Packages list: %s", ",".join(self.packages))

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

    def add_features_packages(self, xml_root):
        """ Selects packages based on user selected features """

        # Add necessary packages for user desired features to our install list
        for xml_features in xml_root.iter('features'):
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

        # Add libreoffice language package
        if self.settings.get('feature_office'):
            lang_name = self.settings.get("language_name").lower()
            code = None
            if lang_name == "english":
                locale = self.settings.get("locale").split('.')[0]
                if locale in ['en_GB', 'en_ZA']:
                    # There're some English variants available but not all of them.
                    code = locale
            else:
                # All the other language packs use their language code
                code = self.settings.get('language_code')

            if code:
                code = code.replace('_', '-')
                pkg_text = "libreoffice-fresh-{0}".format(code)
                logging.debug(
                    "Adding libreoffice language package (%s)", pkg_text)
                self.packages.append(pkg_text)
                # hunspell
                code = code[:2]
                codes = ['de', 'es', 'fr', 'he', 'it',
                         'ro', 'el', 'hu', 'nl', 'pl']
                if code in codes:
                    pkg_text = "hunspell-{0}".format(code)
                    logging.debug(
                        "Adding hunspell dictionaries for %s language", pkg_text)
                    self.packages.append(pkg_text)

        # Add firefox language package
        if self.settings.get('feature_firefox'):
            # Firefox is available in these languages
            lang_codes = [
                'ach', 'af', 'an', 'ar', 'as', 'ast', 'az', 'be', 'bg', 'bn-bd',
                'bn-in', 'br', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'dsb', 'el',
                'en-gb', 'en-us', 'en-za', 'eo', 'es-ar', 'es-cl', 'es-es',
                'es-mx', 'et', 'eu', 'fa', 'ff', 'fi', 'fr', 'fy-nl', 'ga-ie',
                'gd', 'gl', 'gu-in', 'he', 'hi-in', 'hr', 'hsb', 'hu', 'hy-am',
                'id', 'is', 'it', 'ja', 'kk', 'km', 'kn', 'ko', 'lij', 'lt',
                'lv', 'mai', 'mk', 'ml', 'mr', 'ms', 'nb-no', 'nl', 'nn-no',
                'or', 'pa-in', 'pl', 'pt-br', 'pt-pt', 'rm', 'ro', 'ru', 'si',
                'sk', 'sl', 'son', 'sq', 'sr', 'sv-se', 'ta', 'te', 'th', 'tr',
                'uk', 'uz', 'vi', 'xh', 'zh-cn', 'zh-tw']

            lang_code = self.settings.get('language_code')
            lang_code = lang_code.replace('_', '-')
            if lang_code in lang_codes:
                pkg_text = "firefox-i18n-{0}".format(lang_code)
                logging.debug("Adding firefox language package (%s)", pkg_text)
                self.packages.append(pkg_text)
