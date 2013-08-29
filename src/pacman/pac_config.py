#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pac.py
#
#  This file has fragments of code from pamac (package manager from Manjaro)
#  Check it at http://git.manjaro.org/core/pamac
#  
#  Copyright 2013 Manjaro (http://manjaro.org)
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
#  
#  Antergos Team:
#   Alex Filgueira (faidoc) <alexfilgueira.antergos.com>
#   Raúl Granados (pollitux) <raulgranados.antergos.com>
#   Gustau Castells (karasu) <karasu.antergos.com>
#   Kirill Omelchenko (omelcheck) <omelchek.antergos.com>
#   Marc Miralles (arcnexus) <arcnexus.antergos.com>
#   Alex Skinner (skinner) <skinner.antergos.com>

import io
import os
import glob
import sys
import argparse
import collections
import warnings

import pyalpm

class InvalidSyntax(Warning):
    def __init__(self, filename, problem, arg):
        self.filename = filename
        self.problem = problem
        self.arg = arg

    def __str__(self):
        return "unable to parse %s, %s: %r" % (self.filename, self.problem, self.arg)

# Options that may occur several times in a section. Their values should be
# accumulated in a list.
LIST_OPTIONS = (
    'CacheDir',
    'HoldPkg',
    'IgnoreGroup',
    'IgnorePkg',
    'NoExtract',
    'NoUpgrade',
    'Server'
)

SINGLE_OPTIONS = (
    'RootDir',
    'DBPath',
    'GPGDir',
    'LogFile',
    'Architecture',
    'XferCommand',
    'CleanMethod',
    'SigLevel',
    'LocalFileSigLevel'
)

BOOLEAN_OPTIONS = (
    'UseSyslog',
    'ShowSize',
    'UseDelta',
    'TotalDownload',
    'CheckSpace',
    'VerbosePkgLists',
    'ILoveCandy',
    'Color'
)

def pacman_conf_enumerator(path):
    filestack = []
    current_section = None
    filestack.append(open(path))
    while len(filestack) > 0:
        f = filestack[-1]
        line = f.readline()
        if len(line) == 0:
            # end of file
            filestack.pop()
            continue

        line = line.strip()
        if len(line) == 0: continue
        if line[0] == '#':
            continue
        if line[0] == '[' and line[-1] == ']':
            current_section = line[1:-1]
            continue
        if current_section is None:
            raise InvalidSyntax(f.name, 'statement outside of a section', line)
        # read key, value
        key, equal, value = [x.strip() for x in line.partition('=')]

        # include files
        if equal == '=' and key == 'Include':
            filestack.extend(open(f) for f in glob.glob(value))
            continue
        if current_section != 'options':
            # repos only have the Server option
            if key == 'Server' and equal == '=':
                yield (current_section, 'Server', value)
            elif key == 'SigLevel' and equal == '=':
                yield (current_section, 'SigLevel', value)
            else:
                raise InvalidSyntax(f.name, 'invalid key for repository configuration', line)
            continue
        if equal == '=':
            if key in LIST_OPTIONS:
                for val in value.split():
                    yield (current_section, key, val)
            elif key in SINGLE_OPTIONS:
                yield (current_section, key, value)
            else:
                warnings.warn(InvalidSyntax(f.name, 'unrecognized option', key))
        else:
            if key in BOOLEAN_OPTIONS:
                yield (current_section, key, True)
            else:
                warnings.warn(InvalidSyntax(f.name, 'unrecognized option', key))

class PacmanConfig(object):
    def __init__(self, conf = None, options = None):
        self.options = {}
        self.repos = collections.OrderedDict()

        # Default options
        self.options["RootDir"] = "/install"
        self.options["DBPath"]  = "/install/var/lib/pacman"
        self.options["GPGDir"]  = "/install/etc/pacman.d/gnupg/"
        self.options["LogFile"] = "/install/var/log/pacman.log"
        self.options["Architecture"] = os.uname()[-1]
        
        # If a pacman.conf file is given, we parse it
        if conf is not None:
            self.load_from_file(conf)
            
        # If an options array is given, we add it
        if options is not None:
            self.load_from_options(options)

    def load_from_file(self, filename):
        for section, key, value in pacman_conf_enumerator(filename):
            if section == 'options':
                if key == 'Architecture' and value == 'auto':
                    continue
                if key in LIST_OPTIONS:
                    self.options.setdefault(key, []).append(value)
                else:
                    self.options[key] = value
            else:
                servers = self.repos.setdefault(section, [])
                if key == 'Server':
                    servers.append(value)
        if "CacheDir" not in self.options:
            self.options["CacheDir"]= ["/var/cache/pacman/pkg"]

    def load_from_options(self, options):
        global _logmask
        if options.root is not None:
            self.options["RootDir"] = options.root
        if options.dbpath is not None:
            self.options["DBPath"] = options.dbpath
        if options.gpgdir is not None:
            self.options["GPGDir"] = options.gpgdir
        if options.arch is not None:
            self.options["Architecture"] = options.arch
        if options.logfile is not None:
            self.options["LogFile"] = options.logfile
        if options.cachedir is not None:
            self.options["CacheDir"] = [option.cachedir]
        if options.debug:
            _logmask = 0xffff

    def apply(self, h):
        h.arch = self.options["Architecture"]
        h.logfile = self.options["LogFile"]
        h.gpgdir = self.options["GPGDir"]
        h.cachedirs = self.options["CacheDir"]
        if "IgnoreGroup" in self.options:
            h.ignoregrps = self.options["IgnoreGroup"]
        if "IgnorePkg" in self.options:
            h.ignorepkgs = self.options["IgnorePkg"]
        if "NoExtract" in self.options:
            h.noextracts = self.options["NoExtract"]
        if "NoUpgrade" in self.options:
            h.noupgrades = self.options["NoUpgrade"]

        # set sync databases
        for repo, servers in self.repos.items():
            db = h.register_syncdb(repo, 0)
            db_servers = []
            for rawurl in servers:
                url = rawurl.replace("$repo", repo)
                url = url.replace("$arch", self.options["Architecture"])
                db_servers.append(url)
            db.servers = db_servers

    def initialize_alpm(self):
        h = pyalpm.Handle(self.options["RootDir"], self.options["DBPath"])
        self.apply(h)
        return h

    def __str__(self):
        return("PacmanConfig(options=%s, repos=%s)" % (str(self.options), str(self.repos)))

