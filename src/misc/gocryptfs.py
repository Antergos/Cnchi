#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# gocryptfs.py
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

""" gocryptfs encription module. """

import logging
import os
import shutil
import subprocess
import tempfile

try:
    import misc.extra as misc
except ImportError as _err:
    import extra as misc

# https://github.com/rfjakob/gocryptfs/blob/master/Documentation/CLI_ABI.md

def _sync():
    """ Synchronize cached writes to persistent storage """
    try:
        subprocess.check_call(['/usr/bin/sync'])
    except subprocess.CalledProcessError as why:
        logging.warning(
            "Can't synchronize cached writes to persistent storage: %s",
            why)

def _gocryptfs(params, _username, password):
    """ Calls gocrypt program (giving the password through a pipe). """
    try:
        cmd = ['/usr/bin/gocryptfs'] + params
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write(password.encode())
        proc.stdin.close()
        proc.wait()
        _sync()
    except subprocess.CalledProcessError as why:
        logging.warning("Error calling gocryptfs: %s", why)

def _copy_folder_contents(src_path, dst_path, username=None, usergroup=None):
    """ Copies all files from user's home folder """
    with os.scandir(src_path) as items:
        for entry in items:
            src = os.path.join(src_path, entry.name)
            dst = os.path.join(dst_path, entry.name)
            if entry.is_file():
                shutil.copy(src, dst)
            elif entry.is_dir():
                shutil.copytree(src, dst)
            # Set correct owner
            if username and usergroup:
                shutil.chown(dst, username, usergroup)

def _restore_user_home_files(paths, username=None, usergroup=None):
    """ Copies previously saved user files to its original destination """

    _copy_folder_contents(paths['backup'], paths['plain'])

    # Fix gocrypt files owner in cipher directory
    if username and usergroup:
        gocrypt_files = ["gocryptfs.conf", "gocryptfs.diriv"]
        for gocrypt_file in gocrypt_files:
            path = os.path.join(paths['cipher'], gocrypt_file)
            if os.path.exists(path):
                shutil.chown(path, username, usergroup)

def setup(username, usergroup, install_dir, password):
    """ Prepare home folder to be stored using cryfs """

    if os.path.exists("/usr/bin/gocryptfs"):
        paths = {
            'plain': os.path.join(install_dir, 'home', username),
            'cipher': os.path.join(install_dir, 'home', '.' + username)
        }

        with tempfile.TemporaryDirectory() as backup_dir:
            paths['backup'] = backup_dir
            logging.debug("User folder (plain): %s", paths['plain'])
            logging.debug("User folder (backup): %s", paths['backup'])
            logging.debug("User folder (cipher): %s", paths['cipher'])

            # Backup home user directory
            with misc.raised_privileges():
                try:
                    # Save all user files before doing anything
                    _copy_folder_contents(paths['plain'], paths['backup'])
                    _sync()

                    # Create user dirs (plain and cipher)
                    os.makedirs(paths['plain'], mode=0o700, exist_ok=True)
                    os.makedirs(paths['cipher'], mode=0o700, exist_ok=True)

                    # Set correct owner
                    shutil.chown(paths['plain'], username, usergroup)
                    shutil.chown(paths['cipher'], username, usergroup)

                    # gocryptfs -init cipher
                    params = ['-init', '-q', '--', paths['cipher']]
                    _gocryptfs(params, username, password)

                    # Before mounting, delete user's home folder
                    shutil.rmtree(paths['plain'])
                    os.makedirs(paths['plain'], mode=0o700)

                    # gocryptfs cipher plain
                    params = ['-q', '--', paths['cipher'], paths['plain']]
                    _gocryptfs(params, username, password)

                    # Restore all user home files
                    _restore_user_home_files(paths, username, usergroup)
                except (shutil.Error, PermissionError, LookupError) as err:
                    logging.error(err)
                except FileNotFoundError as err:
                    logging.warning(err)
    else:
        logging.error("Cannot find gocryptfs program. Is it really installed?")

def test_module():
    """ Test gocryptfs encryption of a user called test """
    setup("test", "users", "/", "test123")

if __name__ == "__main__":
    test_module()
