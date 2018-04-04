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


import requests
import sys
import os
import shutil
import tarfile
from pathlib import Path
import logging

try:
    import libnacl
except ImportError:
    sys.stderr.write('Please install python-libnacl package')
    exit()

import libnacl.utils

from lembrame.config import LembrameConfig

import misc.gsettings as gsettings
from misc.run_cmd import chroot_call


def _(x): return x


def get_key_decryption_file(pass_hash, salt):
    for i in range(2, 2 ** 17):
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
        self.user_home = '/home/' + self.settings.get('username')
        self.install_user_home = '/install/home/' + self.settings.get('username')
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
                logging.debug("Downloading the Lembrame encrypted file failed")
                return False
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
            logging.debug("Requesting for download link to Lembrame failed")
            return False

    def setup(self):
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
                logging.debug("Signature on the Lembrame file doesn't match")
                return False
        else:
            logging.debug("Lembrame encrypted file doesn't exists")
            return False

        if self.extract_encrypted_file():
            logging.debug("Lembrame decrypted file successfully extracted to: %s", self.config.folder_file_path)
            return True
        else:
            return False

    def open_file(self):
        try:
            self.encrypted_file = open(self.config.file_path, 'rb')
        except IOError:
            logging.debug("Can't read Lembrame encrypted file: %s", IOError)

    def verify_file_signature(self):
        if self.encrypted_file.read(self.LEN_MAGICNUM) == self.APP_MAGICNUM:
            return True
        else:
            return False

    def decrypt_file(self):
        pass_hash, saltnonce = self.get_decryption_hash()
        prot_key = get_key_decryption_file(pass_hash, saltnonce)

        self.encrypted_file.seek(self.LEN_MAGICNUM + self.LEN_NONCE)
        prot_box = self.encrypted_file.read(self.LEN_PROT_BOX)

        try:
            prot_keynonce = libnacl.crypto_secretbox_open(prot_box, saltnonce, prot_key)
        except ValueError:
            logging.debug("Incorrect upload code trying to decrypt Lembrame file")
            return False

        data_nonce = prot_keynonce[0:self.LEN_NONCE]
        data_key = prot_keynonce[self.LEN_NONCE:self.LEN_NONCE + self.LEN_KEY]

        self.encrypted_file.seek(self.LEN_MAGICNUM + self.LEN_NONCE + self.LEN_PROT_BOX)

        plaindata = open(self.config.decrypted_file_path, 'xb')

        plaindata.write(libnacl.crypto_secretbox_open(self.encrypted_file.read(), data_nonce, data_key))

        return True

    def get_decryption_hash(self):
        self.encrypted_file.seek(self.LEN_MAGICNUM)
        saltnonce = self.encrypted_file.read(self.LEN_NONCE)
        password = saltnonce + self.credentials.get_upload_code().encode('utf-8')
        return libnacl.crypto_hash_sha512(password), saltnonce

    def extract_encrypted_file(self):
        try:
            tar = tarfile.open(self.config.decrypted_file_path, "r:gz")
            tar.extractall(self.config.folder_file_path)
            tar.close()
            return True
        except tarfile.TarError as err:
            logging.debug("Error trying to extract Lembrame decrypted file: %s", str(err))
            return False

    def copy_folder_to_dest(self):
        shutil.copytree(self.config.folder_file_path, self.install_user_home + self.dest_folder, False, None)

    def before_setup(self):
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
        packages = []
        package_list_file = self.config.folder_file_path + '/' + self.config.pacman_packages
        package_list = Path(self.config.folder_file_path + '/' + self.config.pacman_packages)
        logging.debug("Get pacman package list from Lembrame")
        if package_list.is_file():
            with open(package_list_file) as line:
                packages = line.read().splitlines()
        logging.debug("Packages from Lembrame: %s", ",".join(packages))
        return packages

    def overwrite_content(self):
        # Copy the extracted Lembrame file to the user's home
        self.copy_folder_to_dest()

        # Check if the background folder has at least one file.
        # It should have just one, so select the first found by default
        background_folder = os.listdir(self.install_user_home + self.dest_folder + '/background')
        if len(background_folder) > 0:
            logging.debug("Configuring the background")
            background_image = background_folder[0]
            gsettings.set(
                self.settings.get('username'),
                'org.gnome.desktop.background',
                'picture-uri',
                'file://' + self.user_home + self.dest_folder + '/background/' + background_image
            )

        # Overwrite .bashrc
        bashrc_file = self.install_user_home + self.dest_folder + '/.bashrc'
        bashrc_file_dest = self.install_user_home + '/.bashrc'
        shutil.copy(bashrc_file, bashrc_file_dest)

        # Set the file owner
        chroot_call([
            'chown',
            '-R',
            self.settings.get('username') + ':' + 'users',
            self.user_home + self.dest_folder
        ])
