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

try:
    import misc.extra as misc
except ModuleNotFoundError as _err:
    import extra as misc

# https://github.com/rfjakob/gocryptfs/blob/master/Documentation/CLI_ABI.md

def _gocryptfs(cmd, password):
    """ Calls gocrypt program (giving the password through a pipe).
        cmd: tuple """
    cat = subprocess.Popen(("echo", password), stdout=subprocess.PIPE)
    output = subprocess.check_output(cmd, stdin=cat.stdout)
    cat.wait()
    logging.debug(output)


def _gocryptfs_binary():
    """ Checks if gocrypt binary file exists """
    if os.path.exists("/usr/bin/gocryptfs") or os.path.exists("/usr/local/bin/gocryptfs"):
        return True
    return False

def setup(username, usergroup, install_dir, password):
    """ Prepare home folder to be stored using cryfs """

    if _gocryptfs_binary():
        paths = {
            'plain': os.path.join(install_dir, 'home', username),
            'backup': os.path.join(install_dir, 'home', username + '.backup'),
            'cipher': os.path.join(install_dir, 'home', '.' + username)
        }

        logging.debug("User folder (plain): %s", paths['plain'])
        logging.debug("User folder (backup): %s", paths['backup'])
        logging.debug("User folder (cipher): %s", paths['cipher'])

        # Backup home user directory
        with misc.raised_privileges() as __:
            try:
                shutil.move(paths['plain'], paths['backup'])
                os.makedirs(paths['plain'], mode=0o755, exist_ok=True)
                os.makedirs(paths['cipher'], mode=0o755, exist_ok=True)
                # Encrypt (using gocryptfs)
                # gocryptfs -init cipher
                # gocryptfs cipher plain

                # echo "xxx" | gocryptfs cipher plain

                _gocryptfs(('gocryptfs', '-init', paths['cipher']), password)

                # FIXME: Does not work!
                _gocryptfs(('gocryptfs', paths['cipher'], paths['plain']), password)

                # Restore all user home files
                #shutil.move(os.path.join(paths['backup'], '*'), paths['plain'])

                # Restore owner
                #for path in paths:
                #    shutil.chown(path, username, usergroup)
            except PermissionError as err:
                logging.error(err)
                return
    else:
        logging.error("Cannot find gocryptfs program. Is it really installed?")

def test_module():
    """ Test gocryptfs encryption of a user called test """
    setup("test", "users", "/", "test123")

if __name__ == "__main__":
    test_module()
