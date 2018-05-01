#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# lamp.py
#
# Copyright © 2013-2018 Antergos
#
# This file is part of Cnchi.
#
# Cnchi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Cnchi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The following additional terms are in effect as per Section 7 of the license:
#
# The preservation of all legal notices and author attributions in
# the material or in the Appropriate Legal Notices displayed
# by works containing it is required.
#
# You should have received a copy of the GNU General Public License
# along with Cnchi; If not, see <http://www.gnu.org/licenses/>.


"""
LAMP stack is a group of open source software to get web servers up
and running. The acronym stands for Linux, Apache, MySQL, and PHP.
Since the server is already running Antergos, the linux
part is taken care of.
"""


import os
import logging
import shutil

from misc.run_cmd import chroot_call

DEST_DIR = '/install'


def setup():
    """ Runs lamp setup """
    try:
        logging.debug("Doing Mariadb setup...")
        mariadb_setup()
        logging.debug("Mariadb setup done. Doing Apache setup...")
        apache_setup()
        logging.debug("Apache setup done. Doing PHP setup...")
        php_setup()
        logging.debug("PHP setup done.")
    except (FileExistsError, OSError) as io_error:
        logging.error(io_error)


def mariadb_setup():
    """ Runs MariaDB setup """
    cmd = [
        "mysql_install_db",
        "--user=mysql",
        "--basedir=/usr",
        "--datadir=/var/lib/mysql"]
    chroot_call(cmd)

    cmd = ["systemctl", "enable", "mysqld"]
    chroot_call(cmd)

    # TODO: Warn user to run mysql_secure_installation


def apache_setup():
    """ Configure Apache web server """
    # Allow site virtualization
    httpd_path = os.path.join(DEST_DIR, 'etc/httpd/conf/httpd.conf')
    with open(httpd_path, 'a') as httpd_conf:
        httpd_conf.write('IncludeOptional conf/sites-enabled/*.conf\n')
        httpd_conf.write('IncludeOptional conf/mods-enabled/*.conf\n')

    # We create config directories
    dirs = [
        "etc/httpd/conf/sites-available",
        "etc/httpd/conf/sites-enabled",
        "etc/httpd/conf/mods-enabled"]

    for path in dirs:
        path = os.path.join(DEST_DIR, path)
        os.makedirs(path, mode=0o755, exist_ok=True)

    # Copy a2ensite and a2dissite scripts
    scripts = ["a2ensite", "a2dissite"]
    for script in scripts:
        try:
            src = os.path.join("/usr/share/cnchi/scripts", script)
            dst = os.path.join(DEST_DIR, 'usr/local/bin', script)
            shutil.copy2(src, dst)
            os.chmod(dst, 0o755)
        except (FileExistsError, shutil.Error) as file_error:
            logging.warning(file_error)

    # Create localhost.conf in /etc/httpd/conf/sites-available/
    localhost_path = os.path.join(
        DEST_DIR, "etc/httpd/conf/sites-available/localhost.conf")
    with open(localhost_path, 'a') as localhost_conf:
        localhost_conf.write('\n# phpmyadmin alias and directory setup\n')
        localhost_conf.write(
            'Alias /phpmyadmin "/usr/share/webapps/phpMyAdmin"\n')
        localhost_conf.write('<Directory "/usr/share/webapps/phpMyAdmin">\n')
        localhost_conf.write('    DirectoryIndex index.html index.php\n')
        localhost_conf.write('    AllowOverride All\n')
        localhost_conf.write('    Options FollowSymlinks\n')
        localhost_conf.write('    Require all granted\n')
        localhost_conf.write('</Directory>\n')

    # We activate the virtual localhost site
    chroot_call(["a2ensite", "localhost"])

    chroot_call(["systemctl", "enable", "httpd"])


def php_setup():
    """ Setup PHP """
    # Comment mpm_event_module
    httpd_path = os.path.join(DEST_DIR, 'etc/httpd/conf/httpd.conf')
    with open(httpd_path, 'r') as load_module:
        lines = load_module.readlines()
    with open(httpd_path, 'w') as load_module:
        for line in lines:
            if "LoadModule mpm_event_module" in line:
                line = '# LoadModule mpm_event_module modules/mod_mpm_event.so\n'
            load_module.write(line)

    # Add mpm_prefork_module and php5_module
    php_path = os.path.join(DEST_DIR, 'etc/httpd/conf/mods-enabled/php.conf')
    with open(php_path, 'w') as php_conf:
        php_conf.write(
            "LoadModule mpm_prefork_module /etc/httpd/modules/mod_mpm_prefork.so\n")
        php_conf.write(
            "LoadModule php7_module /etc/httpd/modules/libphp7.so\n")
        php_conf.write("Include conf/extra/php7_module.conf\n")

    # PHP extensions that will be activated
    so_extensions = ["mysql", "mcrypt", "mssql", "mysqli",
                     "openssl", "iconv", "imap", "zip", "bz2"]

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
                line = ("open_basedir = /srv/http/:/home/:/tmp/:"
                        "/usr/share/pear/:/usr/share/webapps/:/etc/webapps/\n")
            php_ini.write(line)

    # Create a symlink (sites-enabled/localhost.conf) to sites-available/localhost.conf
    # Not necessary, a2ensite does this for us
    # source = os.path.join(DEST_DIR, 'etc/httpd/conf/sites-available/localhost.conf')
    # link_name = os.path.join(DEST_DIR, 'etc/httpd/conf/sites-enabled/localhost.conf')
    # os.symlink(source, link_name)


if __name__ == '__main__':
    setup()
