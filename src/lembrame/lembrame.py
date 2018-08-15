#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lembrame.py
#
#  Copyright © 2013-2017 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

""" Lembrame module. Gets and applies previous user's lembrame setup """

import ast
import logging
import os
from pathlib import Path
import requests
import shutil
import tarfile

try:
    import libnacl
except ImportError:
    logging.error('Please install python-libnacl package')
    exit()

import libnacl.utils

from lembrame.config import LembrameConfig
from lembrame.gnome_extensions.downloader import GnomeExtensionsDownloader

import misc.gsettings as gsettings
from misc.run_cmd import chroot_call
from misc.extra import InstallError


def _(msg):
    return msg


def get_key_decryption_file(pass_hash, salt):
    """ Gets key for decryption """
    for _index in range(2, 2 ** 17):
        pass_hash = libnacl.crypto_hash_sha512(salt + pass_hash)
    return libnacl.crypto_hash_sha256(salt + pass_hash)


class Lembrame:
    """ Lembrame main class """

    download_link = False
    encrypted_file = False
    dest_folder = False
    user_home = False
    install_user_home = False

    APP_MAGICNUM = b'LEMBRAME0'
    LEN_MAGICNUM = 9
    LEN_NONCE = 24
    LEN_KEY = 32
    LEN_PROT_BOX = 72

    def __init__(self, settings):
        self.settings = settings
        self.config = LembrameConfig()
        self.credentials = self.settings.get('lembrame_credentials')
        self.user_home = '/home/' + self.settings.get('user_name')
        self.install_user_home = '/install/home/' + self.settings.get('user_name')
        self.dest_folder = '/.lembrame-sync'

    def download_file(self):
        """ Download the lembrame encrypted file """
        if self.request_download_link():
            req = requests.get(self.download_link, stream=True)
            if req.status_code == requests.codes.ok:
                with open(self.config.file_path, 'wb') as encrypted_file:
                    for data in req.iter_content(1024):
                        if not data:
                            break
                        encrypted_file.write(data)
                return True
            else:
                raise InstallError(_("Downloading the Lembrame encrypted file failed"))
        else:
            return False

    def request_download_link(self):
        """ Request for a signed S3 download link """
        payload = {'uid': self.credentials.user_id}

        logging.debug("Requesting download link for uid: %s", self.credentials.user_id)

        req = requests.post(self.config.request_download_endpoint, json=payload)
        if req.status_code == requests.codes.ok:
            self.download_link = req.json()['data']
            logging.debug("API responded with a download link")
            return True
        else:
            raise InstallError(_("Requesting for download link to Lembrame failed"))

    def setup(self):
        """ Get lembrame user's preferences """
        self.before_setup()
        logging.debug("Checking if the Lembrame encrypted file exists")
        encrypted_file = Path(self.config.file_path)
        if encrypted_file.is_file():
            self.open_file()
            signature = self.verify_file_signature()
            if signature:
                if self.decrypt_file() is False:
                    return False
            else:
                raise InstallError(_("Signature on the Lembrame file doesn't match"))
        else:
            logging.error("Lembrame encrypted file doesn't exists")
            return False

        if self.extract_encrypted_file():
            logging.debug("Lembrame decrypted file successfully extracted to: %s", self.config.folder_file_path)
            logging.debug("Overwriting Cnchi config variables")
            self.overwrite_installer_variables()
            return True
        else:
            return False

    def open_file(self):
        """ Opens encrypted file """
        try:
            self.encrypted_file = open(self.config.file_path, 'rb')
        except IOError:
            logging.error("Can't read Lembrame encrypted file: %s", IOError)
            raise InstallError(_("Can't read Lembrame encrypted file"))

    def verify_file_signature(self):
        """ Verifies signature of the encrypted file """
        if self.encrypted_file.read(self.LEN_MAGICNUM) == self.APP_MAGICNUM:
            return True
        else:
            return False

    def decrypt_file(self):
        """ Decripts file """
        pass_hash, saltnonce = self.get_decryption_hash()
        prot_key = get_key_decryption_file(pass_hash, saltnonce)

        self.encrypted_file.seek(self.LEN_MAGICNUM + self.LEN_NONCE)
        prot_box = self.encrypted_file.read(self.LEN_PROT_BOX)

        try:
            prot_keynonce = libnacl.crypto_secretbox_open(prot_box, saltnonce, prot_key)
        except ValueError:
            raise InstallError(_("Incorrect upload code trying to decrypt Lembrame file"))

        data_nonce = prot_keynonce[0:self.LEN_NONCE]
        data_key = prot_keynonce[self.LEN_NONCE:self.LEN_NONCE + self.LEN_KEY]

        self.encrypted_file.seek(self.LEN_MAGICNUM + self.LEN_NONCE + self.LEN_PROT_BOX)

        plaindata = open(self.config.decrypted_file_path, 'xb')

        plaindata.write(libnacl.crypto_secretbox_open(self.encrypted_file.read(), data_nonce, data_key))

        return True

    def get_decryption_hash(self):
        """ Gets sha512 hash from password """
        self.encrypted_file.seek(self.LEN_MAGICNUM)
        saltnonce = self.encrypted_file.read(self.LEN_NONCE)
        password = saltnonce + self.credentials.get_upload_code().encode('utf-8')
        return libnacl.crypto_hash_sha512(password), saltnonce

    def extract_encrypted_file(self):
        """ Untars decrypted file """
        try:
            tar = tarfile.open(self.config.decrypted_file_path, "r:gz")
            tar.extractall(self.config.folder_file_path)
            tar.close()
            return True
        except tarfile.TarError as err:
            logging.error("Error trying to extract Lembrame decrypted file: %s", str(err))
            raise InstallError(_("Error trying to extract Lembrame decrypted file"))

    def copy_folder_to_dest(self):
        """ Copies whole configuration folder to destination """
        shutil.copytree(self.config.folder_file_path, self.install_user_home + self.dest_folder, False, None)

    def before_setup(self):
        """ Cleanup before trying to get user configuration (just in case) """
        logging.debug("Removing existing decrypted files from Lembrame")
        try:
            os.remove(self.config.decrypted_file_path)
        except OSError:
            pass

        logging.debug("Removing existing extracted files from encrypted")
        shutil.rmtree(self.config.folder_file_path, True)
        logging.debug("Removing existing .lembrame-sync folder on /install")
        shutil.rmtree(self.install_user_home + self.dest_folder, True)

    def get_pacman_packages(self):
        """ Get list of pacman packages stored in lembrame user's configuration """
        packages = []
        package_list_file = self.config.folder_file_path + '/' + self.config.pacman_packages
        package_list = Path(self.config.folder_file_path + '/' + self.config.pacman_packages)
        logging.debug("Get pacman package list from Lembrame")
        if package_list.is_file():
            with open(package_list_file) as line:
                packages = line.read().splitlines()
        logging.debug("Packages from Lembrame: %s", ",".join(packages))
        return packages

    def overwrite_installer_variables(self):
        """ Overwrites installer variables with the ones obtained from lembrame """
        # Overwrite Display Manager
        self.settings.set('desktop_manager', self.get_synced_display_manager())

    def overwrite_content(self):
        """ Copy user configuration and files to new installation """
        # Copy the extracted Lembrame file to the user's home
        self.copy_folder_to_dest()

        # Check which gnome shell extensions the user had enabled and proceed
        # to download them from extensions.gnome.org and put it on the designated folder
        self.download_gnome_extensions()

        # Enable Gnome Shell extensions and other shell settings like favorite apps
        gsettings.dconf_load(
            self.settings.get('user_name'),
            '/org/gnome/shell/',
            self.user_home + self.dest_folder + '/' + self.config.dconf_dump
        )

        # Check if the background folder has at least one file.
        # It should have just one, so select the first found by default
        background_folder = os.listdir(self.install_user_home + self.dest_folder + '/background')
        if len(background_folder) > 0:
            logging.debug("Configuring the background")
            background_image = background_folder[0]
            gsettings.set(
                self.settings.get('user_name'),
                'org.gnome.desktop.background',
                'picture-uri',
                'file://' + self.user_home + self.dest_folder + '/background/' + background_image
            )

        # Check if the screensaver folder has at least one file.
        # It should have just one, so select the first found by default
        screensaver_folder = os.listdir(self.install_user_home + self.dest_folder + '/screensaver')
        if len(screensaver_folder) > 0:
            logging.debug("Configuring the screensaver")
            screensaver_image = screensaver_folder[0]
            gsettings.set(
                self.settings.get('user_name'),
                'org.gnome.desktop.screensaver',
                'picture-uri',
                'file://' + self.user_home + self.dest_folder + '/screensaver/' + screensaver_image
            )

        # Overwrite .bashrc
        bashrc_file = self.install_user_home + self.dest_folder + '/.bashrc'
        bashrc_file_dest = self.install_user_home + '/.bashrc'
        shutil.copy(bashrc_file, bashrc_file_dest)

        # Set the file owner
        chroot_call([
            'chown',
            '-R',
            self.settings.get('user_name') + ':' + 'users',
            self.user_home + self.dest_folder
        ])

    def download_gnome_extensions(self):
        """ Download Gnome extensions that are selected in user's lembrame configuration """
        dconf_dump_file = Path(self.install_user_home + self.dest_folder + '/' + self.config.dconf_dump)
        enabled_extensions = []
        if dconf_dump_file.is_file():
            with open(dconf_dump_file) as dconf_file:
                for line in dconf_file:
                    line = line.rstrip()
                    if 'enabled-extensions' in line:
                        line_array = line.split("enabled-extensions=")
                        if len(line_array) > 0:
                            enabled_extensions = ast.literal_eval(line_array[1])
                            logging.debug("Enabled Gnome Shell extensions to download: %s", ''.join(enabled_extensions))
                        else:
                            logging.debug("There's no enabled extensions")
        else:
            logging.error("There's a problem with the dconf dump file. Gnome Shell extension can't be downloaded")

        downloader = GnomeExtensionsDownloader(self.install_user_home, self.config)
        downloader.run(enabled_extensions)

    def get_synced_display_manager(self):
        """ Get display manager selected by the user """
        # Current default Antergos Display Manager
        display_manager = 'lightdm'

        dm_file = Path(self.config.folder_file_path + '/' + self.config.display_manager_file)
        if dm_file.is_file():
            try:
                with open(dm_file) as line:
                    dm_from_file = line.read()
                    if dm_from_file:
                        display_manager = dm_from_file
                    else:
                        logging.debug("We can't get the Display Manager from the file")
            except OSError as error:
                logging.error("We can't open the file to get the Display Manager: %s", error)
                # raise InstallError(_("We can't open the file to get the Display Manager"))

        logging.debug("Display manager selected: %s", display_manager)
        return display_manager
