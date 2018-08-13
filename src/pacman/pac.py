#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pac.py
#
#  This code is based on previous work by Rémy Oudompheng <remy@archlinux.org>
#
#  Copyright © 2013-2018 Antergos
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


""" Module interface to pyalpm """

from collections import OrderedDict

import logging
import os
import queue
import sys
#import traceback

from misc.events import Events

import pacman.alpm_include as _alpm
import pacman.pkginfo as pkginfo
import pacman.pacman_conf as config

try:
    import pyalpm
except ImportError as err:
    # This is already logged elsewhere
    # logging.error(err)
    pass

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

_DEFAULT_ROOT_DIR = "/"
_DEFAULT_DB_PATH = "/var/lib/pacman"


class Pac():
    """ Communicates with libalpm using pyalpm """
    LOG_FOLDER = '/var/log/cnchi'

    def __init__(self, conf_path="/etc/pacman.conf", callback_queue=None):
        self.events = Events(callback_queue)

        self.conflict_to_remove = None

        self.handle = None

        self.logger = None
        self.setup_logger()

        # Some download indicators (used in cb_dl callback)
        self.last_target = ""
        self.last_percent = 0
        self.already_transferred = 0
        # Store package total download size
        self.total_size = 0
        # Store last action
        self.last_action = ""

        # Total packages to download
        self.total_packages_to_download = 0
        self.downloaded_packages = 0

        self.last_event = {}

        if not os.path.exists(conf_path):
            raise pyalpm.error

        if conf_path is not None and os.path.exists(conf_path):
            self.config = config.PacmanConfig(conf_path)
            self.initialize_alpm()
            logging.debug('ALPM repository database order is: %s',
                          self.config.repo_order)
        else:
            raise pyalpm.error

    @staticmethod
    def format_size(size):
        """ Formats downloaded size into a string """
        kib_size = size / 1024
        if kib_size < 1000:
            size_string = _('%.1f KiB') % (kib_size)
            return size_string
        size_string = _('%.2f MiB') % (kib_size / 1024)
        return size_string

    def get_handle(self):
        """ Return alpm handle """
        return self.handle

    def get_config(self):
        """ Get pacman.conf config """
        return self.config

    def initialize_alpm(self):
        """ Set alpm setup """
        if self.config is not None:
            root_dir = self.config.options["RootDir"]
            db_path = self.config.options["DBPath"]
        else:
            root_dir = _DEFAULT_ROOT_DIR
            db_path = _DEFAULT_DB_PATH

        self.handle = pyalpm.Handle(root_dir, db_path)

        logging.debug(
            "ALPM initialised with root dir %s and db path %s", root_dir, db_path)

        if self.handle is None:
            raise pyalpm.error

        if self.config is not None:
            self.config.apply(self.handle)

        # Set callback functions
        # Callback used for logging
        self.handle.logcb = self.cb_log
        # Callback used to report download progress
        self.handle.dlcb = self.cb_dl
        # Callback used to report total download size
        self.handle.totaldlcb = self.cb_totaldl
        # Callback used for events
        self.handle.eventcb = self.cb_event
        # Callback used for questions
        self.handle.questioncb = self.cb_question
        # Callback used for operation progress
        self.handle.progresscb = self.cb_progress
        # Downloading callback
        self.handle.fetchcb = None

    def release(self):
        """ Release alpm handle """
        if self.handle is not None:
            del self.handle
            self.handle = None

    @staticmethod
    def finalize_transaction(transaction):
        """ Commit a transaction """
        try:
            logging.debug("Prepare alpm transaction...")
            transaction.prepare()
            logging.debug("Commit alpm transaction...")
            transaction.commit()
        except pyalpm.error as err:
            logging.error("Can't finalize alpm transaction: %s", err)
            #traceback.print_exc()
            transaction.release()
            return False
        transaction.release()
        logging.debug("Alpm transaction done.")
        return True

    def init_transaction(self, options=None):
        """ Transaction initialization """
        if options is None:
            options = {}

        transaction = None
        try:
            transaction = self.handle.init_transaction(
                nodeps=options.get('nodeps', False),
                dbonly=options.get('dbonly', False),
                force=options.get('force', False),
                needed=options.get('needed', False),
                alldeps=(options.get('mode', None) ==
                         pyalpm.PKG_REASON_DEPEND),
                allexplicit=(options.get('mode', None) ==
                             pyalpm.PKG_REASON_EXPLICIT),
                cascade=options.get('cascade', False),
                nosave=options.get('nosave', False),
                recurse=(options.get('recursive', 0) > 0),
                recurseall=(options.get('recursive', 0) > 1),
                unneeded=options.get('unneeded', False),
                downloadonly=options.get('downloadonly', False))
        except pyalpm.error as pyalpm_error:
            logging.error("Can't init alpm transaction: %s", pyalpm_error)
        return transaction

    def remove(self, pkg_names, options=None):
        """ Removes a list of package names """

        if not options:
            options = {}

        # Prepare target list
        targets = []
        database = self.handle.get_localdb()
        for pkg_name in pkg_names:
            pkg = database.get_pkg(pkg_name)
            if pkg is None:
                logging.error("Target %s not found", pkg_name)
                return False
            targets.append(pkg)

        transaction = self.init_transaction(options)

        if transaction is None:
            logging.error("Can't init transaction")
            return False

        for pkg in targets:
            logging.debug(
                "Adding package '%s' to remove transaction", pkg.name)
            transaction.remove_pkg(pkg)

        return self.finalize_transaction(transaction)

    def refresh(self):
        """ Sync databases like pacman -Sy """
        if self.handle is None:
            logging.error("alpm is not initialised")
            raise pyalpm.error

        force = True
        res = True
        for database in self.handle.get_syncdbs():
            transaction = self.init_transaction()
            if transaction:
                database.update(force)
                transaction.release()
            else:
                res = False
        return res

    def install(self, pkgs, conflicts=None, options=None):
        """ Install a list of packages like pacman -S """

        if not conflicts:
            conflicts = []

        if not options:
            options = {}

        if self.handle is None:
            logging.error("alpm is not initialised")
            raise pyalpm.error

        if not pkgs:
            logging.error("Package list is empty")
            raise pyalpm.error

        # Discard duplicates
        pkgs = list(set(pkgs))

        # `alpm.handle.get_syncdbs()` returns a list (the order is important) so we
        # have to ensure we don't clobber the priority of the repos.
        repos = OrderedDict()
        repo_order = []
        db_match = [db for db in self.handle.get_syncdbs()
                    if db.name == 'antergos']
        antdb = OrderedDict()
        antdb['antergos'] = db_match[0]

        one_repo_groups_names = ['cinnamon', 'mate', 'mate-extra']
        one_repo_groups = []
        for one_repo_group_name in one_repo_groups_names:
            grp = antdb['antergos'].read_grp(one_repo_group_name)
            if not grp:
                # Group does not exist
                grp = ['None', []]
            one_repo_groups.append(grp)

        one_repo_pkgs = {pkg for one_repo_group in one_repo_groups
                         for pkg in one_repo_group[1] if one_repo_group}

        for syncdb in self.handle.get_syncdbs():
            repo_order.append(syncdb)
            repos[syncdb.name] = syncdb

        targets = []
        for name in pkgs:
            _repos = repos

            if name in one_repo_pkgs:
                # pkg should be sourced from the antergos repo only.
                _repos = antdb

            result_ok, pkg = self.find_sync_package(name, _repos)

            if result_ok:
                # Check that added package is not in our conflicts list
                if pkg.name not in conflicts:
                    targets.append(pkg.name)
            else:
                # Couldn't find the package, check if it's a group
                group_pkgs = self.get_group_pkgs(name)
                if group_pkgs is not None:
                    # It's a group
                    for group_pkg in group_pkgs:
                        # Check that added package is not in our conflicts list
                        # Ex: connman conflicts with netctl(openresolv),
                        # which is installed by default with base group
                        if group_pkg.name not in conflicts:
                            targets.append(group_pkg.name)
                else:
                    # No, it wasn't neither a package nor a group. As we don't
                    # know if this error is fatal or not, we'll register it and
                    # we'll allow to continue.
                    logging.error(
                        "Can't find a package or group called '%s'", name)

        # Discard duplicates
        targets = list(set(targets))
        logging.debug(targets)

        if not targets:
            logging.error("No targets found")
            return False

        num_targets = len(targets)
        logging.debug("%d target(s) found", num_targets)

        # Maybe not all this packages will be downloaded, but it's
        # how many have to be there before starting the installation
        self.total_packages_to_download = num_targets

        transaction = self.init_transaction(options)

        if transaction is None:
            logging.error("Can't initialize alpm transaction")
            return False

        for _index in range(0, num_targets):
            result_ok, pkg = self.find_sync_package(targets.pop(), repos)
            if result_ok:
                transaction.add_pkg(pkg)
            else:
                logging.warning(pkg)

        return self.finalize_transaction(transaction)

    def upgrade(self, pkgs, conflicts=None, options=None):
        """ Install a list package tarballs like pacman -U """

        conflicts = conflicts if conflicts else []
        options = options if options else {}

        if self.handle is None:
            logging.error("alpm is not initialised")
            raise pyalpm.error

        if not pkgs:
            logging.error("Package list is empty")
            raise pyalpm.error

        # Discard duplicates
        pkgs = list(set(pkgs))

        self.handle.get_localdb()

        # Prepare targets list
        targets = []
        for tarball in pkgs:
            pkg = self.handle.load_pkg(tarball)
            targets.append(pkg)

        transaction = self.init_transaction(options)

        if transaction is None:
            logging.error("Can't initialize alpm transaction")
            return False

        for pkg in targets:
            transaction.add_pkg(pkg)

        return self.finalize_transaction(transaction)

    @staticmethod
    def find_sync_package(pkgname, syncdbs):
        """ Finds a package name in a list of DBs
        :rtype : tuple (True/False, package or error message)
        """
        for database in syncdbs.values():
            pkg = database.get_pkg(pkgname)
            if pkg is not None:
                return True, pkg
        return False, "Package '{0}' was not found.".format(pkgname)

    def get_group_pkgs(self, group):
        """ Get group's packages """
        for repo in self.handle.get_syncdbs():
            grp = repo.read_grp(group)
            if grp is not None:
                _name, pkgs = grp
                return pkgs
        return None

    def get_packages_info(self, pkg_names=None):
        """ Get information about packages like pacman -Si """
        if not pkg_names:
            pkg_names = []
        packages_info = {}
        if not pkg_names:
            # Store info from all packages from all repos
            for repo in self.handle.get_syncdbs():
                for pkg in repo.pkgcache:
                    packages_info[pkg.name] = pkginfo.get_pkginfo(
                        pkg,
                        level=2,
                        style='sync')
        else:
            repos = OrderedDict((database.name, database)
                                for database in self.handle.get_syncdbs())
            for pkg_name in pkg_names:
                result_ok, pkg = self.find_sync_package(pkg_name, repos)
                if result_ok:
                    packages_info[pkg_name] = pkginfo.get_pkginfo(
                        pkg,
                        level=2,
                        style='sync')
                else:
                    packages_info = {}
                    logging.error(pkg)
        return packages_info

    def get_package_info(self, pkg_name):
        """ Get information about packages like pacman -Si """
        repos = OrderedDict((database.name, database)
                            for database in self.handle.get_syncdbs())
        result_ok, pkg = self.find_sync_package(pkg_name, repos)
        if result_ok:
            info = pkginfo.get_pkginfo(pkg, level=2, style='sync')
        else:
            logging.error(pkg)
            info = {}
        return info

    # Callback functions

    @staticmethod
    def cb_question(*args):
        """ Called to get user input """
        pass

    def cb_event(self, event, event_data):
        """ Converts action ID to descriptive text and enqueues it to the events queue """
        action = self.last_action

        if event == _alpm.ALPM_EVENT_CHECKDEPS_START:
            action = _('Checking dependencies...')
        elif event == _alpm.ALPM_EVENT_FILECONFLICTS_START:
            action = _('Checking file conflicts...')
        elif event == _alpm.ALPM_EVENT_RESOLVEDEPS_START:
            action = _('Resolving dependencies...')
        elif _alpm.ALPM_EVENT_INTERCONFLICTS_START:
            action = _('Checking inter conflicts...')
        elif event == _alpm.ALPM_EVENT_PACKAGE_OPERATION_START:
             # ALPM_EVENT_PACKAGE_OPERATION_START is shown in cb_progress
            action = ''
        elif event == _alpm.ALPM_EVENT_INTEGRITY_START:
            action = _('Checking integrity...')
            self.already_transferred = 0
        elif event == _alpm.ALPM_EVENT_LOAD_START:
            action = _('Loading packages files...')
        elif event == _alpm.ALPM_EVENT_DELTA_INTEGRITY_START:
            action = _("Checking target delta integrity...")
        elif event == _alpm.ALPM_EVENT_DELTA_PATCHES_START:
            action = _('Applying deltas to packages...')
        elif event == _alpm.ALPM_EVENT_DELTA_PATCH_START:
            action = _('Generating {} with {}...')
            action = action.format(event_data[0], event_data[1])
        elif event == _alpm.ALPM_EVENT_RETRIEVE_START:
            action = _('Downloading files from the repositories...')
        elif event == _alpm.ALPM_EVENT_DISKSPACE_START:
            action = _('Checking available disk space...')
        elif event == _alpm.ALPM_EVENT_KEYRING_START:
            action = _('Checking keys in keyring...')
        elif event == _alpm.ALPM_EVENT_KEY_DOWNLOAD_START:
            action = _('Downloading missing keys into the keyring...')
        elif event == _alpm.ALPM_EVENT_SCRIPTLET_INFO:
            action = _('Configuring {}').format(self.last_target)

        if action != self.last_action:
            self.last_action = action
            self.events.add('info', action)

    def cb_log(self, level, line):
        """ Log pyalpm warning and error messages.
            Possible message types:
            LOG_ERROR, LOG_WARNING, LOG_DEBUG, LOG_FUNCTION """

        # Strip ending '\n'
        line = line.rstrip()

        # Log everything to cnchi-alpm.log
        self.logger.debug(line)

        logmask = pyalpm.LOG_ERROR | pyalpm.LOG_WARNING

        if not level & logmask:
            # Only log errors and warnings
            return

        if level & pyalpm.LOG_ERROR:
            logging.error(line)
        elif level & pyalpm.LOG_WARNING:
            logging.warning(line)
        elif level & pyalpm.LOG_DEBUG or level & pyalpm.LOG_FUNCTION:
            logging.debug(line)

    def cb_progress(self, target, percent, total, current):
        """ Shows install progress """
        if target:
            action = _("Installing {0} ({1}/{2})").format(target, current, total)
            percent = current / total
            self.events.add('info', action)
        else:
            percent = round(percent / 100, 2)

        if target != self.last_target:
            self.last_target = target

        if percent != self.last_percent:
            self.last_percent = percent
            self.events.add('percent', percent)

    def cb_totaldl(self, total_size):
        """ Stores total download size for use in cb_dl and cb_progress """
        self.total_size = total_size

    def cb_dl(self, filename, transferred, total):
        """ Shows downloading progress """
        if filename.endswith('.db'):
            action = _("Updating {0} database").format(filename.replace('.db', ''))
        else:
            action = _("Downloading {}...").format(filename.replace('.pkg.tar.xz', ''))

        # target = self.last_target
        percent = self.last_percent

        if self.total_size > 0:
            percent = round((transferred + self.already_transferred) / self.total_size, 2)
        elif total > 0:
            percent = round(transferred / total, 2)

        if action != self.last_action:
            self.last_action = action
            self.events.add('info', action)

        if percent != self.last_percent:
            self.last_percent = percent
            self.events.add('percent', percent)
        elif transferred == total:
            self.already_transferred += total
            self.downloaded_packages += 1

    def is_package_installed(self, package_name):
        """ Check if package is already installed """
        database = self.handle.get_localdb()
        pkgs = database.search(*[package_name])
        names = []
        for pkg in pkgs:
            names.append(pkg.name)
        return bool(package_name in names)

    def setup_logger(self):
        """ Configure our logger """
        self.logger = logging.getLogger(__name__)

        self.logger.setLevel(logging.DEBUG)

        self.logger.propagate = False

        # Log format
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(filename)s(%(lineno)d) %(funcName)s(): %(message)s")

        if not self.logger.hasHandlers():
            # File logger
            try:
                log_path = os.path.join(Pac.LOG_FOLDER, 'cnchi-alpm.log')
                file_handler = logging.FileHandler(log_path, mode='w')
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except PermissionError as permission_error:
                print("Can't open ", log_path, " : ", permission_error)


def test():
    """ Test case """
    import gettext
    _ = gettext.gettext

    formatter = logging.Formatter(
        '[%(asctime)s] [%(module)s] %(levelname)s: %(message)s',
        "%Y-%m-%d %H:%M:%S.%f")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    try:
        pacman = Pac("/etc/pacman.conf")
    except pyalpm.error as ex:
        print("Can't initialize pyalpm: ", ex)
        sys.exit(1)

    try:
        pacman.refresh()
    except pyalpm.error as err:
        print("Can't update databases: ", err)
        sys.exit(1)

    # pacman_options = {"downloadonly": True}
    # pacman.do_install(pkgs=["base"], conflicts=[], options=pacman_options)
    pacman.release()


if __name__ == "__main__":
    test()
