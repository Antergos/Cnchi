#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lemp.py
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

"""
LEMP stack is a group of open source software to get web servers up
and running. The acronym stands for Linux, nginx (pronounced Engine x),
MySQL, and PHP. Since the server is already running Antergos, the linux
part is taken care of.
"""


import os
import logging

try:
    from installation import chroot
except ImportError:
    import chroot

DEST_DIR = '/install'


def chroot_run(cmd):
    chroot.run(cmd, DEST_DIR)


def setup():
    logging.debug(_("Doing Mariadb setup..."))
    mariadb_setup()
    logging.debug(_("Mariadb setup done. Doing Nginx setup..."))
    nginx_setup()
    logging.debug(_("Nginx setup done. Doing PHP-fpm setup..."))
    php_fpm_setup()
    logging.debug(_("PHP-fpm setup done."))


def mariadb_setup():
    cmd = [
        "mysql_install_db",
        "--user=mysql",
        "--basedir=/usr",
        "--datadir=/var/lib/mysql"]
    chroot_run(cmd)

    cmd = ["systemctl", "enable", "mysqld"]
    chroot_run(cmd)

    # TODO: Warn user to run mysql_secure_installation


def nginx_setup():
    cmd = ["systemctl", "enable", "nginx"]
    chroot_run(cmd)

    # We need to tell nginx to run php using php-fpm.
    path = os.path.join(DEST_DIR, "etc/nginx/nginx.conf")
    with open(path, 'r') as nginx_conf:
        lines = nginx_conf.readlines()

    sections = {"http": False, "server": False, "location": False}
    with open(path, 'w') as nginx_conf:
        for line in lines:
            if "http {" in line:
                sections["http"] = True

            if sections["http"] and "server {" in line:
                sections["server"] = True

            if sections["http"] and sections["server"] and "#location ~ \.php$ {" in line:
                nginx_conf.write("        location ~ \.php$ {\n")
                nginx_conf.write("            fastcgi_pass   unix:/var/run/php-fpm/php-fpm.sock;\n")
                nginx_conf.write("            fastcgi_index  index.php;\n")
                nginx_conf.write("            root   /usr/share/nginx/html;\n")
                nginx_conf.write("            include        fastcgi.conf;\n")
                nginx_conf.write("        }\n\n")
                sections = {"http": False, "server": False, "location": False}

            nginx_conf.write(line)


def php_fpm_setup():
    cmd = ["systemctl", "enable", "php-fpm"]
    chroot_run(cmd)


if __name__ == '__main__':
    setup()
