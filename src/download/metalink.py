#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  metalink.py
#
#  Parts of code from pm2ml Copyright (C) 2012-2013 Xyne
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


""" Operations with metalinks """

import logging
import tempfile
import os

import hashlib
import re
import argparse

from collections import deque

import xml.dom.minidom as minidom
try:
    import xml.etree.cElementTree as eTree
except ImportError:
    import xml.etree.ElementTree as eTree

import pyalpm

MAX_URLS = 15


def get_info(metalink):
    """ Reads metalink xml info and returns it """

    # tag = "{urn:ietf:params:xml:ns:metalink}"

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(str(metalink).encode('UTF-8'))
    temp_file.close()

    metalink_info = {}
    element = {}

    for event, elem in eTree.iterparse(temp_file.name, events=('start', 'end')):
        if event == "start":
            if elem.tag.endswith("file"):
                element['filename'] = elem.attrib['name']
            elif elem.tag.endswith("identity"):
                element['identity'] = elem.text
            elif elem.tag.endswith("size"):
                element['size'] = elem.text
            elif elem.tag.endswith("version"):
                element['version'] = elem.text
            elif elem.tag.endswith("description"):
                element['description'] = elem.text
            elif elem.tag.endswith("hash"):
                element['hash'] = elem.text
            elif elem.tag.endswith("url"):
                try:
                    element['urls'].append(elem.text)
                except KeyError:
                    element['urls'] = [elem.text]
        if event == "end":
            if elem.tag.endswith("file"):
                # Limit to MAX_URLS for file
                if len(element['urls']) > MAX_URLS:
                    element['urls'] = element['urls'][:MAX_URLS]
                key = element['identity']
                metalink_info[key] = element.copy()
                element.clear()
                elem.clear()

    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)

    return metalink_info


def create(alpm, package_name, pacman_conf_file):
    """ Creates a metalink to download package_name and its dependencies """

    options = ["--conf", pacman_conf_file, "--noconfirm", "--all-deps"]

    if package_name == "databases":
        options.append("--refresh")
    else:
        options.append(package_name)

    try:
        download_queue, not_found, missing_deps = build_download_queue(
            alpm, args=options)
    except Exception as ex:
        template = "Unable to create download queue for package {0}. " \
            "An exception of type {1} occured. Arguments:\n{2!r}"
        message = template.format(package_name, type(ex).__name__, ex.args)
        logging.error(message)
        return None

    if not_found:
        msg = "Can't find these packages: "
        for pkg_not_found in sorted(not_found):
            msg = msg + pkg_not_found + " "
        logging.error(msg)
        return None

    if missing_deps:
        msg = "Can't resolve these dependencies: "
        for missing in sorted(missing_deps):
            msg = msg + missing + " "
        logging.error(msg)
        return None

    metalink = download_queue_to_metalink(download_queue)

    return metalink


# From here comes modified code from pm2ml
# pm2ml is Copyright (C) 2012-2013 Xyne
# More info: http://xyne.archlinux.ca/projects/pm2ml


def download_queue_to_metalink(download_queue):
    """ Converts a download_queue object to a metalink """
    metalink = Metalink()

    for database, sigs in download_queue.dbs:
        metalink.add_db(database, sigs)

    for pkg, urls, sigs in download_queue.sync_pkgs:
        metalink.add_sync_pkg(pkg, urls, sigs)

    return metalink


class Metalink(object):
    """ Metalink class """

    def __init__(self):
        self.doc = minidom.getDOMImplementation().createDocument(None, "metalink", None)
        self.doc.documentElement.setAttribute(
            'xmlns', "urn:ietf:params:xml:ns:metalink")
        self.files = self.doc.documentElement

    # def __del__(self):
    #    self.doc.unlink()

    def __str__(self):
        """ Get a string representation of a metalink """
        return re.sub(
            r'(?<=>)\n\s*([^\s<].*?)\s*\n\s*',
            r'\1',
            self.doc.toprettyxml(indent=' ')
        )

    def add_urls(self, element, urls):
        """Add URL elements to the given element."""
        for url in urls:
            url_tag = self.doc.createElement('url')
            element.appendChild(url_tag)
            url_val = self.doc.createTextNode(url)
            url_tag.appendChild(url_val)

    def add_sync_pkg(self, pkg, urls, sigs=False):
        """Add a sync db package."""
        file_ = self.doc.createElement("file")
        file_.setAttribute("name", pkg.filename)
        self.files.appendChild(file_)
        for tag, db_attr, attrs in (
                ('identity', 'name', ()),
                ('size', 'size', ()),
                ('version', 'version', ()),
                ('description', 'desc', ()),
                ('hash', 'sha256sum', (('type', 'sha256'),)),
                ('hash', 'md5sum', (('type', 'md5'),))):
            tag = self.doc.createElement(tag)
            file_.appendChild(tag)
            val = self.doc.createTextNode(str(getattr(pkg, db_attr)))
            tag.appendChild(val)
            for key, val in attrs:
                tag.setAttribute(key, val)
        urls = list(urls)
        self.add_urls(file_, urls)
        if sigs:
            self.add_file(pkg.filename + '.sig', (u + '.sig' for u in urls))

    def add_file(self, name, urls):
        """Add a signature file."""
        file_ = self.doc.createElement("file")
        file_.setAttribute("name", name)
        self.files.appendChild(file_)
        self.add_urls(file_, urls)

    def add_db(self, database, sigs=False):
        """Add a sync db."""
        file_ = self.doc.createElement("file")
        name = database.name + '.db'
        file_.setAttribute("name", name)
        self.files.appendChild(file_)
        urls = list(os.path.join(url, database.name + '.db')
                    for url in database.servers)
        self.add_urls(file_, urls)
        if sigs:
            self.add_file(name + '.sig', (u + '.sig' for u in urls))


class PkgSet(object):
    """ Represents a set of packages """

    def __init__(self, pkgs=None):
        """ Init our internal self.pkgs dict with all given packages in pkgs """

        self.pkgs = dict()
        if pkgs:
            for pkg in pkgs:
                self.pkgs[pkg.name] = pkg

    def __repr__(self):
        return 'PkgSet({0})'.format(repr(self.pkgs))

    def add(self, pkg):
        """ Adds package info to the set """
        self.pkgs[pkg.name] = pkg

    def __and__(self, other):
        new = PkgSet(set(self.pkgs.values()) & set(other.pkgs.values()))
        return new

    def __iand__(self, other):
        self.pkgs = self.__and__(other).pkgs
        return self

    def __or__(self, other):
        copy = PkgSet(list(self.pkgs.values()))
        return copy.__ior__(other)

    def __ior__(self, other):
        self.pkgs.update(other.pkgs)
        return self

    def __contains__(self, pkg):
        return pkg.name in self.pkgs

    def __iter__(self):
        for value in self.pkgs.values():
            yield value

    def __len__(self):
        return len(self.pkgs)


class DownloadQueue(object):
    """ Represents a download queue """

    def __init__(self):
        self.dbs = list()
        self.sync_pkgs = list()

    def __bool__(self):
        return bool(self.dbs or self.sync_pkgs)

    def __nonzero__(self):
        return self.dbs or self.sync_pkgs

    def add_db(self, database, sigs=False):
        """ Adds db info and signatures to the queue """
        self.dbs.append((database, sigs))

    def add_sync_pkg(self, pkg, urls, sigs=False):
        """ Adds package and its urls to the queue """
        self.sync_pkgs.append((pkg, urls, sigs))


def parse_args(args):
    """ Parse arguments to build_download_queue function
        These arguments mimic pacman ones """
    parser = argparse.ArgumentParser()

    parser.add_argument('pkgs', nargs='*', default=[], metavar='<pkgname>',
                        help='Packages or groups to download.')
    parser.add_argument('--all-deps', action='store_true', dest='alldeps',
                        help='Include all dependencies even if they are already installed.')
    parser.add_argument('-c', '--conf', metavar='<path>', default='/etc/pacman.conf', dest='conf',
                        help='Use a different pacman.conf file.')
    parser.add_argument('--noconfirm', action='store_true', dest='noconfirm',
                        help='Suppress user prompts.')
    parser.add_argument('-d', '--nodeps', action='store_true', dest='nodeps',
                        help='Skip dependencies.')
    parser.add_argument('--needed', action='store_true', dest='needed',
                        help='Skip packages if they already exist in the cache.')
    help_msg = '''Include signature files for repos with optional and required SigLevels.
        Pass this flag twice to attempt to download signature for all databases and packages.'''
    parser.add_argument('-s', '--sigs', action='count', default=0, dest='sigs',
                        help=help_msg)
    parser.add_argument('-y', '--databases', '--refresh', action='store_true', dest='db',
                        help='Download databases.')

    return parser.parse_args(args)


def get_antergos_repo_pkgs(alpm_handle):
    """ Returns pkgs from Antergos groups (cinnamon, mate, mate-extra) and
        the antergos db info """

    antdb = None
    for database in alpm_handle.get_syncdbs():
        if database.name == 'antergos':
            antdb = database
            break

    group_names = ['cinnamon', 'mate', 'mate-extra']
    repo_groups = []
    for group_name in group_names:
        group = antdb.read_grp(group_name)
        if not group:
            # Group does not exist
            group = ['None', []]
        repo_groups.append(group)

    repo_pkgs = {
        pkg for repo_group in repo_groups
        for pkg in repo_group[1] if repo_group}

    return repo_pkgs, antdb


def resolve_deps(alpm_handle, other, alldeps):
    """ Resolve dependencies """
    missing_deps = []
    queue = deque(other)
    local_cache = alpm_handle.get_localdb().pkgcache
    syncdbs = alpm_handle.get_syncdbs()
    seen = set(queue)
    while queue:
        pkg = queue.popleft()
        for dep in pkg.depends:
            if pyalpm.find_satisfier(local_cache, dep) is None or alldeps:
                for database in syncdbs:
                    prov = pyalpm.find_satisfier(database.pkgcache, dep)
                    if prov:
                        other.add(prov)
                        if prov.name not in seen:
                            seen.add(prov.name)
                            queue.append(prov)
                        break
                else:
                    missing_deps.append(dep)
    return other, missing_deps


def create_package_set(requested, repo_pkgs, antdb, alpm_handle):
    """ Create package set from requested set """
    other = PkgSet()
    found = set()

    for pkg in requested:
        other_grp = PkgSet()
        for database in alpm_handle.get_syncdbs():
            if pkg in repo_pkgs and database.name != 'antergos':
                # pkg should be sourced from the antergos repo only.
                database = antdb

            syncpkg = database.get_pkg(pkg)

            if syncpkg:
                other.add(syncpkg)
                break
            else:
                syncgrp = database.read_grp(pkg)
                if syncgrp:
                    found.add(pkg)
                    other_grp |= PkgSet(syncgrp[1])
                    break
        else:
            other |= other_grp
    return found, other

def build_download_queue(alpm, args=None):
    """ Function to build a download queue.
        Needs a pkgname in args """

    pargs = parse_args(args)

    requested = set(pargs.pkgs)

    handle = alpm.get_handle()
    conf = alpm.get_config()

    missing_deps = list()

    ant_repo_pkgs, antdb = get_antergos_repo_pkgs(handle)

    found, other = create_package_set(requested, ant_repo_pkgs, antdb, handle)

    # foreign_names = requested - set(x.name for x in other)

    # Resolve dependencies.
    if other and not pargs.nodeps:
        other, missing_deps = resolve_deps(handle, other, pargs.alldeps)

    found |= set(other.pkgs)
    not_found = requested - found
    if pargs.needed:
        other = PkgSet(list(check_cache(conf, other)))

    # Build download queue
    download_queue = DownloadQueue()

    # Add databases (and their signature)
    if pargs.db:
        for database in handle.get_syncdbs():
            try:
                siglevel = conf[database.name]['SigLevel'].split()[0]
            except KeyError:
                siglevel = None
            download_sig = needs_sig(siglevel, pargs.sigs, 'Database')
            download_queue.add_db(database, download_sig)

    # Add packages (pkg, url, signature)
    for pkg in other:
        try:
            siglevel = conf[pkg.db.name]['SigLevel'].split()[0]
        except KeyError:
            siglevel = None
        download_sig = needs_sig(siglevel, pargs.sigs, 'Package')

        urls = []
        server_urls = list(pkg.db.servers)
        for server_url in server_urls:
            url = os.path.join(server_url, pkg.filename)
            urls.append(url)

        # Limit to MAX_URLS url
        while len(urls) > MAX_URLS:
            urls.pop()

        download_queue.add_sync_pkg(pkg, urls, download_sig)

    return download_queue, not_found, missing_deps


def get_checksum(path, typ):
    """ Returns checksum of a file """
    new_hash = hashlib.new(typ)
    block_size = new_hash.block_size
    try:
        with open(path, 'rb') as myfile:
            buf = myfile.read(block_size)
            while buf:
                new_hash.update(buf)
                buf = myfile.read(block_size)
        return new_hash.hexdigest()
    except FileNotFoundError:
        return -1
    except IOError as io_error:
        logging.error(io_error)


def check_cache(conf, pkgs):
    """ Checks package checksum in cache """
    for pkg in pkgs:
        for cache in conf.options['CacheDir']:
            fpath = os.path.join(cache, pkg.filename)
            for checksum in ('sha256', 'md5'):
                real_checksum = get_checksum(fpath, checksum)
                correct_checksum = getattr(pkg, checksum + 'sum')
                if real_checksum is None or real_checksum != correct_checksum:
                    yield pkg
                    break
            else:
                continue
            break


def needs_sig(siglevel, insistence, prefix):
    """ Determines if a signature should be downloaded.
        The siglevel is the pacman.conf SigLevel for the given repo.
        The insistence is an integer. Anything below 1 will return false,
        anything above 1 will return true, and 1 will check if the
        siglevel is required or optional.
        The prefix is either "Database" or "Package". """

    if insistence > 1:
        return True
    elif insistence == 1 and siglevel:
        for sl_type in ('Required', 'Optional'):
            if siglevel == sl_type or siglevel == prefix + sl_type:
                return True
    return False


def test_module():
    """ Module test function """
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

    #import gc
    #import pprint
    import pacman.pac as pac

    try:
        pacman = pac.Pac(
            conf_path="/etc/pacman.conf",
            callback_queue=None)

        print("Creating metalink...")
        meta4 = create(
            alpm=pacman,
            package_name="automake",
            pacman_conf_file="/etc/pacman.conf")
        print(get_info(meta4))
        # print(get_info(meta4)['automake']['urls'])
        meta4 = None
        # objects = gc.collect()
        # print("Unreachable objects: ", objects)
        # print("Remaining garbage: ", pprint.pprint(gc.garbage))

        pacman.release()
        del pacman
    except Exception as ex:
        template = "Can't initialize pyalpm. An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logging.error(message)


# Test case
if __name__ == '__main__':
    test_module()
