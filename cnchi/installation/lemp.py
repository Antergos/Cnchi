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
    try:
        logging.debug("Doing Mariadb setup...")
        mariadb_setup()
        logging.debug("Mariadb setup done. Doing Nginx setup...")
        nginx_setup()
        logging.debug("Nginx setup done. Doing PHP-fpm setup...")
        php_setup()
        logging.debug("PHP-fpm setup done.")
    except (FileExistsError, OSError) as io_error:
        logging.error(io_error)


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


def php_setup():
    # Setup /etc/php/php.ini
    php_ini_path = os.path.join(DEST_DIR, 'etc/php/php.ini')
    with open(php_ini_path, 'r') as php_ini:
        lines = php_ini.readlines()

    # PHP extensions that will be activated
    so_extensions = ["mysql", "mcrypt", "mssql", "mysqli", "openssl", "iconv", "imap", "zip", "bz2"]

    php_ini_path = os.path.join(DEST_DIR, 'etc/php/php.ini')
    with open(php_ini_path, 'r') as php_ini:
        lines = php_ini.readlines()

    with open(php_ini_path, 'w') as php_ini:
        for line in lines:
            # Uncomment extensions
            for so_ext in so_extensions:
                ext = ";extension={0}.so".format(so_ext)
                if line.startswith(ext):
                    line = line[1:]
            # Add PhpMyAdmin system path (/etc/webapps/ and /usr/share/webapps/)
            # to make sure PHP can access and read files under those directories
            if "open_basedir =" in line:
                line = 'open_basedir = /srv/http/:/home/:/tmp/:/usr/share/pear/:/usr/share/webapps/:/etc/webapps/\n'
            php_ini.write(line)

    cmd = ["systemctl", "enable", "php-fpm"]
    chroot_run(cmd)


if __name__ == '__main__':
    setup()
