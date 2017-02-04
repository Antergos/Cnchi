#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# select_packages.py
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

from installation import pacman as pac
import misc.extra as misc
from misc.extra import InstallError

import hardware.hardware as hardware

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
        self.alternate_package_list = self.settings.get('alternate_package_list')
        self.desktop = self.settings.get('desktop')
        self.zfs = self.settings.get('zfs')

        # Packages to be removed
        self.conflicts = []

        # Packages to be installed
        self.packages = []

        self.vbox = False
        self.my_arch = os.uname()[-1]

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
            pacman = pac.Pac("/etc/pacman.conf", self.callback_queue)
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

    def get_desktop_lib(self):
        """ Returns which widget library our desktop will need """
        for lib in desktop_info.LIBS:
            if self.desktop in desktop_info.LIBS[lib]:
                return lib
        return None

    def add_package(self, pkg):
        """ Adds xml node text to our package list
            returns TRUE if the package is added """
        added = False

        # Check node attributes
        names = ["arch", "lib", "desktops", "lang"]

        check_attr = {
            "arch" : self.my_arch,
            "lib" : self.get_desktop_lib(),
            "desktops" : self.desktop,
            "lang" : self.settings.get('language_code')
        }

        all_check = True
        for name in names:
            node_attr = pkg.attrib.get(name)
            if node_attr and check_attr[name] not in node_attr:
                all_check = False

        if all_check:
            conflicts = pkg.attrib.get("conflicts")
            if conflicts:
                self.add_conflicts(conflicts)
            self.packages.append(pkg.text)
            added = True
            # If package is a Desktop Manager or a Network Manager,
            # save the name to activate the correct service later
            if pkg.attrib.get('dm'):
                self.settings.set("desktop_manager", pkg.attrib.get('name'))
            if pkg.attrib.get('nm'):
                self.settings.set("network_manager", pkg.attrib.get('name'))
        return added

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
            self.add_language_pack("kde")

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
            self.conflicts.append("virtualbox-guest-utils")

        # Add linux-lts-headers if LTS kernel is installed in a vbox vm
        if self.vbox and self.settings.get('feature_lts'):
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

        # Add locale fonts (atm only asian) and input system (if needed)
        self.add_locale_fonts(xml_root)

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
        logging.debug("Check for user desired features and add them to our installation")
        self.add_features_packages(xml_root)
        logging.debug("All features needed packages have been added")

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

    def add_locale_fonts(self, root):
        """ Adds input system and fonts """
        # Add locale fonts (add_package checks lang)
        for child in root.iter('fonts'):
            for pkg in child.iter('pkgname'):
                self.add_package(pkg)

        # Add input system if needed for lang_code (we use fcitx)
        lang_code = self.settings.get("language_code").lower()
        for input_system in root.iter('input_systems'):
            name = input_system.get("name").lower()
            lang = input_system.get("lang").lower()
            if name == "fcitx" and lang == lang_code:
                # Check if we need to install this input system
                for child in root.iter('fcitx'):
                    for pkg in child.iter('pkgname'):
                        self.add_package(pkg)

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
            self.add_language_pack("libreoffice")

        # Add firefox language package
        if self.settings.get('feature_firefox'):
            self.add_language_pack("firefox")

    def add_language_pack(self, package):
        lang_codes = {
            "libreoffice" : [
                'af', 'am', 'ar', 'as', 'ast', 'be', 'bg', 'bn', 'bn-IN', 'bo',
                'br', 'brx', 'bs', 'ca', 'ca-valencia', 'cs', 'cy', 'da', 'de',
                'dgo', 'dz', 'el', 'en-GB', 'en-ZA', 'eo', 'es', 'et', 'eu', 'fa',
                'fi', 'fr', 'ga', 'gd', 'gl', 'gu', 'he', 'hi', 'hr', 'hu', 'id',
                'is', 'it', 'ja', 'ka', 'kk', 'km', 'kmr-Latn', 'kn', 'ko', 'kok',
                'ks', 'lb', 'lo', 'lt', 'lv', 'mai', 'mk', 'ml', 'mn', 'mni', 'mr',
                'my', 'nb', 'ne', 'nl', 'nn', 'nr', 'nso', 'oc', 'om', 'or', 'pa-IN',
                'pl', 'pt', 'pt-BR', 'ro', 'ru', 'rw', 'sa-IN', 'sat', 'sd', 'sdk',
                'si', 'sid', 'sk', 'sl', 'sq', 'sr', 'sr-Latn', 'ss', 'st', 'sv',
                'sw-TZ', 'ta', 'te', 'tg', 'th', 'tn', 'tr', 'ts', 'tt', 'ug', 'uk',
                'uz', 've', 'vi', 'xh', 'zh-CN', 'zh-TW', 'zu'],
            "firefox" : [
                'ach', 'af', 'an', 'ar', 'as', 'ast', 'az', 'be', 'bg', 'bn-bd',
                'bn-in', 'br', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'dsb', 'el',
                'en-gb', 'en-us', 'en-za', 'eo', 'es-ar', 'es-cl', 'es-es',
                'es-mx', 'et', 'eu', 'fa', 'ff', 'fi', 'fr', 'fy-nl', 'ga-ie',
                'gd', 'gl', 'gu-in', 'he', 'hi-in', 'hr', 'hsb', 'hu', 'hy-am',
                'id', 'is', 'it', 'ja', 'kk', 'km', 'kn', 'ko', 'lij', 'lt',
                'lv', 'mai', 'mk', 'ml', 'mr', 'ms', 'nb-no', 'nl', 'nn-no',
                'or', 'pa-in', 'pl', 'pt-br', 'pt-pt', 'rm', 'ro', 'ru', 'si',
                'sk', 'sl', 'son', 'sq', 'sr', 'sv-se', 'ta', 'te', 'th', 'tr',
                'uk', 'uz', 'vi', 'xh', 'zh-cn', 'zh-tw'],
            "kde" : [
                'ar', 'bg', 'bs', 'ca', 'ca@valencia', 'cs', 'da', 'de', 'el',
                'en-gb', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'ga', 'gl',
                'he', 'hi', 'hr', 'hu', 'ia', 'id', 'is', 'it', 'ja', 'kk', 'km',
                'ko', 'kok', 'ks', 'lb', 'lo', 'lt', 'lv', 'mai', 'mk', 'ml', 'mn',
                'mni', 'mr', 'my', 'nb', 'ne', 'nl', 'nn', 'nr', 'nso', 'oc', 'om',
                'or', 'pa-IN', 'pl', 'pt', 'pt-BR', 'ro', 'ru', 'rw', 'sa-IN', 'sat',
                'sd', 'sdk', 'si', 'sid', 'sk', 'sl', 'sq', 'sr', 'sr-Latn', 'ss',
                'st', 'sv', 'sw-TZ', 'ta', 'te', 'tg', 'th', 'tn', 'tr', 'ts', 'tt',
                'ug', 'uk', 'uz', 've', 'vi', 'xh', 'zh-CN', 'zh-TW', 'zu']}

        base_names = {
            "libreoffice" : "libreoffice-fresh",
            "firefox" : "firefox-i18n",
            "kde" : "kde-l10n"}

        lang_code = self.settings.get("language_code").lower()
        lang_code = lang_code.replace('_', '-')
        if package in lang_codes and lang_code in lang_codes[package]:
            pkg_text = "{0}-{1}".format(base_names[package], code)
            logging.debug("Adding %s (%s) language package: %s", package, lang_code, pkg_text)
            self.packages.append(pkg_text)
        else:
            logging.warning("Couldn't find %s (%s) language package", package, lang_code)
