#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  encfs.py
#
#  Copyright 2013 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Configures Antergos to encrypt user's home with encFS """

#import logging
import os
import shutil
import subprocess

def setup(username, dest_dir):
    """ Encrypt user's home folder """
    # encfs pam_mount packages are needed
    # pam_encfs from AUR
    # https://wiki.debian.org/TransparentEncryptionForHomeFolder

    # Edit configuration files
    name = os.path.join(dest_dir, "etc/security/pam_encfs.conf")
    shutil.copy(name, name + ".cnchi")
    
    with open(name, "r") as pam_encfs:
        lines = pam_encfs.readlines()
    
    i = len(lines) - 1
    lines[i] = "# " + lines[i]
    
    with open(name, "w") as pam_encfs:
        pam_encfs.write(lines)
        pam_encfs.write("# Added by Cnchi - Antergos Installer\n")
        pam_encfs.write("-\t/home/.encfs\t-\t-v\t-\n")
        
    name = os.path.join(dest_dir, "etc/security/pam_env.conf")
    shutil.copy(name, name + ".cnchi")
    with open(name, "a") as pam_env:
        pam_env.write("# Added by Cnchi - Antergos Installer\n")
        pam_env.write("# Set the ICEAUTHORITY file location to allow GNOME to start on encfs $HOME\n")
        pam_env.write("ICEAUTHORITY DEFAULT=/tmp/.ICEauthority_@{PAM_USER}\n")
    
    name = os.path.join(dest_dir, "etc/fuse.conf")
    shutil.copy(name, name + ".cnchi")
    with open(name, "a") as fuse_conf:
        fuse_conf.write("# Added by Cnchi - Antergos Installer\n")
        fuse_conf.write("user_allow_other\n")

    name = os.path.join(dest_dir, "etc/pam.d/system-login")
    shutil.copy(name, name + ".cnchi")
    with open(name, "a") as system_login:
        system_login.write("# Added by Cnchi - Antergos Installer\n")
        system_login.write("session required\tpam_encfs.so\n")
        system_login.write("session optional\tpam_mount.so\n")
        
    name = os.path.join(dest_dir, "etc/pam.d/system-auth")
    shutil.copy(name, name + ".cnchi")
    with open(name, "a") as system_auth:
        system_auth.write("# Added by Cnchi - Antergos Installer\n")
        system_auth.write("auth sufficient\tpam_encfs.so\n")
        system_auth.write("auth optional\tpam_mount.so\n")

    # Setup finished

    # Move user home dir out of the way
    mounted_dir = os.path.join(self.dest_dir, "home/", username)
    backup_dir = os.path.join(self.dest_dir, "var/tmp/", username)
    subprocess.check_call(['mv', src_dir, backup_dir])

    # Create necessary dirs, encrypted and mounted(unecrypted)
    encrypted_dir = os.path.join(self.dest_dir, "home/.encfs/", username)
    subprocess.check_call(['mkdir', '-p', encrypted_dir, mounted_dir])

    # Set owner
    subprocess.check_call(['chown', '%s:users' % username, encrypted_dir, mounted_dir])
    
    # Create encrypted directory
    subprocess.check_call(['encfs', '-v', encrypted_dir, mounted_dir])
    
    # Restore user home files
    src = os.path.join(backup_dir, "*")
    subprocess.check_call(['mv', src, mounted_dir])
    src = os.path.join(backup_dir, ".[A-Za-z0-9]*")
    subprocess.check_call(['mv', src, mounted_dir])
    
    # Delete home backup
    subprocess.check_call(['rmdir', backup_dir])
