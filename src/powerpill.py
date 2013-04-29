#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  powerpill.py
#  
#  Copyright 2012-2013 Xyne
#  Copyright 2013 Cinnarch
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
#  Cinnarch Team:
#   Alex Filgueira (faidoc) <alexfilgueira.cinnarch.com>
#   Raúl Granados (pollitux) <raulgranados.cinnarch.com>
#   Gustau Castells (karasu) <karasu.cinnarch.com>
#   Kirill Omelchenko (omelcheck) <omelchek.cinnarch.com>
#   Marc Miralles (arcnexus) <arcnexus.cinnarch.com>
#   Alex Skinner (skinner) <skinner.cinnarch.com>

"""
Powerpill is a wrapper around Pacman that uses pm2ml, aria2c and rsync to speed
up package downloads. It is a replacement for the long-ago deprecated Perl
version that became quite popular.

It supports preferential downloads from Pacserve to reduce bandwidth.
"""

# The code is a bit messy because I cobbled it together from parisync.
# I intend to clean it up when I have the time and proper motivation.

import glob
import hashlib
import json
import pm2ml
import shutil

from os import chdir, getcwd, makedirs, unlink
from os.path import join, isfile, abspath, realpath, getsize, exists
from pm2ml import build_download_queue, DownloadQueue, download_queue_to_metalink, PacmanConfig
from Reflector import MirrorStatus
from subprocess import Popen, PIPE, DEVNULL, call, CalledProcessError
from sys import argv, stderr, exit
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen

# Globals

OFFICIAL_REPOSITORIES = MirrorStatus.REPOSITORIES
POWERPILL_CONFIG = '/etc/powerpill/powerpill.json'
ARIA2_EXT = '.aria2'

# See the aria2c manual page for details.
ARIA2_DOWNLOAD_ERROR_EXIT_CODES = (0, 2, 3, 4, 5)
# See the rsync manual page for details.
RSYNC_DOWNLOAD_ERROR_EXIT_CODES = (2, 5, 10, 12, 23, 24, 30)

def digest(fpath):
  # Return the hexadecimal sha256 digest of the given file.
    try:
        with open(fpath, 'rb') as f:
            h = hashlib.sha256()
            block = f.read(h.block_size)
            while block:
                h.update(block)
                block = f.read(h.block_size)
            return h.hexdigest()
    except FileNotFoundError:
        return None

def search_pacserve(pacserve_url):
  # Search for a package on Pacserve. Return the package URL and a boolean
  # indicating if the server appears to be running.
    try:
        with urlopen(pacserve_url) as f:
            return f.geturl().replace('/search/', '/request/'), True
    except HTTPError as e:
        if e.code == 418:
            return None, True
        else:
            raise e
    except URLError as e:
        stderr.write('warning: failed to query Pacserve: %s\n' % e.reason)
    return None, False

# Config Class

class Config(object):
  """
  JSON object wrapper for implementing a configuration file.
  """
  DEFAULTS = {
    'aria2' : {'path' : '/usr/bin/aria2c'},
    'pacman' : {'path' : '/usr/bin/pacman','config' : '/etc/pacman.conf'},
    'powerpill' : {'ask' : True, 'reflect databases' : False},
    'rsync' : {'rsync' : '/usr/bin/rsync'},
  }
  
  def __init__(self, path=None):
    if path is None:
      self.obj = dict()
      self.path = None
    else:
      self.load(path)

  def __str__(self):
    return json.dumps(self.obj, indent='  ', sort_keys=True)

  def load(self, path):
    """
    Load the configuration file.
    """
    with open(path) as f:
      try:
        self.obj = json.load(f)
      except ValueError as e:
        die("error: failed to load %s [%s]\nCheck the file for syntax errors." % (path, e))
      self.path = path

  def save(self, path=None):
    """
    Save the configuration file.
    """
    if path is None:
      path = self.path
    if path is None:
      die('error: no path given for saving configuration file\n')
    with open(path, 'w') as f:
      json.dump(self.obj, f, indent='  ', sort_keys=True)

  def get(self, args):
    """
    Return the requested entry or None if it does not exist.
    """
    obj = self.obj
    args = args.split('/')
    for arg in args:
      try:
        obj = obj[arg]
      except KeyError:
        obj = None
        break
    # Get default if not found.
    if obj is None:
      obj = self.DEFAULTS
      for arg in args:
        try:
          obj = obj[arg]
        except KeyError:
          obj = None
          break
    return obj

  def set(self, args, value):
    """
    Set the requested entry to the given value.
    """
    obj = self.obj
    args = args.split('/')
    for arg in args[:-1]:
      try:
        obj = obj[arg]
      except KeyError:
        obj[arg] = dict()
        obj = obj[arg]
    obj[args[-1]] = value

# Lockfile Class

# TODO
# Maybe merge into Powerpill class.

class Lockfile(object):
  """
  Database lock file wrapper.
  """
  def __init__(self, path):
    self.path = abspath(path)
    self.locked = False

  def __enter__(self):
    if isfile(self.path):
      die('error: lock file exists (%s)\n' % self.path)
    try:
      with open(self.path, 'w') as f:
        self.locked = True
    except PermissionError:
      die('error: failed to create database lock file (%s) [permission denied]\n' % self.path)
    except FileNotFoundError:
      die('error: failed to create database lock file (%s) [database does not exist]\n' % self.path)

  def __exit__(self, typ, val, traceback):
    if self.locked:
      unlink(self.path)
      self.locked = False

# Powerpill

class Powerpill(object):

  def __init__(self, conf, pacman_conf):
    self.conf = conf
    self.pacman_conf = pacman_conf
    self.db_lock = None


  def download_queue_to_rsync_cmd(self,rsync_server,queue,output_dir=None):
    """
    Convert a download queue to an rsync command list.
    """
    cmd = [self.conf.get('rsync/path'), '-aL'] + self.conf.get('rsync/args')

    url = urlparse(rsync_server)
    host = url.netloc
    # [1:] to remove initial slash
    path = url.path[1:].replace('$arch', self.pacman_conf.options['Architecture'])

    host_added = False

    for db, sigs in queue.dbs:
      db_path = '::' + join(path.replace('$repo', db.name), '%s.db' % db.name)
      if not host_added:
        cmd.append(host + db_path)
        host_added = True
      else:
        cmd.append(db_path)
      if sigs:
        cmd.append(db_path + '.sig')

    for pkg, urls, sigs in queue.sync_pkgs:
      pkg_path = '::' + join(path.replace('$repo', pkg.db.name), pkg.filename)
      if not host_added:
        cmd.append(host + pkg_path)
        host_added = True
      else:
        cmd.append(pkg_path)
      if sigs:
        cmd.append(pkg_path + '.sig')

    if not output_dir:
      output_dir = '.'
    cmd.append(output_dir)
    return cmd

  def _download(self, pm2ml_args, dbs=False):
    """
    Download files specified by pm2ml arguments.
    """
    for pkg in self.pacman_conf.options['IgnorePkg']:
      pm2ml_args.extend(('--ignore', pkg))
    for grp in self.pacman_conf.options['IgnoreGroup']:
      pm2ml_args.extend(('--ignoregroup', grp))
    if self.conf.get('powerpill/ask'):
      pm2ml_args.append('--ask')
    if dbs:
#       pm2ml_args.append('--preference')
      reflect = self.conf.get('powerpill/reflect databases')
    else:
      reflect = True
    # This must be added last.
    if reflect and self.conf.get('reflector/args'):
      pm2ml_args += ['--reflector'] + self.conf.get('reflector/args')
    pargs, self.pacman_conf, download_queue, not_found, missing_deps = \
      build_download_queue(pm2ml_args, conf=self.pacman_conf)

    rsync_queue = DownloadQueue()
    metalink_queue = DownloadQueue()

    if pargs.output_dir:
      # A FileExistsError will be raised even with exists_ok=True if the mode
      # does not match the umask-masked mode.
      try:
        makedirs(pargs.output_dir, exist_ok=True)
      except FileExistsError:
        pass
      chdir(pargs.output_dir)

    rsync_servers = self.conf.get('rsync/servers')
    pacserve_server = self.conf.get('pacserve/server')

    for db, sigs in download_queue.dbs:
      is_local = False
      for server in db.servers:
        if server[:7] == 'file://':
          db_name = db.name + '.db'
          local_path = join(server[7:], db_name)
          output_path = join(getcwd(), db_name)
          try:
            shutil.copyfile(local_path, output_path)
            if sigs:
              shutil.copyfile(local_path+'.sig', output_path+'.sig')
            is_local = True
            continue
          except (shutil.Error, FileNotFoundError):
            pass
      if is_local:
        continue
      if rsync_servers and db.name in OFFICIAL_REPOSITORIES:
        rsync_queue.add_db(db, sigs)
      else:
        metalink_queue.add_db(db, sigs)

    if pacserve_server:
      try_pacserve = True
    else:
      try_pacserve = False

    for pkg, urls, sigs in download_queue.sync_pkgs:
#       if self.conf.get('powerpill/checksum'):
#         # Skip existing files if their checksums are correct.
#         # TODO
#         # Eventually add support for checking signatures. There are three ways
#         # to do this:
#         # - use the subprocess module to invoke pacman-key
#         # - package python-gpg and make it a(n optional) dependency
#         # - wait for pyalpm to wrap pacman-key functionality
#         #
#         # I would prefer the latter but I am still waiting for my pacman.conf
#         # parser patch to be accepted upstream in pyalpm, so I do not think there
#         # is much active development.
#
#         already_downloaded = False
#         for d in self.pacman_conf.options['CacheDir']:
#           file_cachepath = join(d, pkg.filename)
#           sha256 = digest(file_cachepath)
#           if sha256 is None:
#             continue
#           elif sha256 != pkg.sha256sum:
#             if self.conf.get('powerpill/clean'):
#               unlink(file_cachepath)
#               try:
#                 unlink(file_cachepath + ARIA2_EXT)
#               except FileNotFoundError:
#                 pass
#               # Continue in case there are others.
#               continue
#             else:
#               stderr.write(
#                 'warning: invalid sha256sum for %s\n> expected %s\n> found    %s\n' \
#                 % (file_cachepath, pkg.sha256sum, sha256)
#               )
#           already_downloaded = True
#           break
#         if already_downloaded:
#           continue
      is_local = False
      for server in urls:
        if server[:7] == 'file://':
          local_path = server[7:]
          output_path = join(getcwd(), pkg.filename)
          try:
            shutil.copyfile(local_path, output_path)
            is_local = True
            continue
          except (shutil.Error, FileNotFoundError):
            pass
      if is_local:
        continue
      use_pacserve = False
      if try_pacserve:
        found = False
        pacserve_url = join(pacserve_server, 'search', pkg.db.name, pkg.arch, pkg.filename)
        found_url, try_pacserve = search_pacserve(pacserve_url)
        # The local pacserve server likely points to the same cache
        # directory. The incoming file would be written to the same file
        # that Pacserve is reading, thus truncating the file. Avoid this
        # by skipping the file if it has a valid checksum, otherwise remove
        # it and requery Pacserve.
        if found_url is not None:
          use_pacserve = True
          if found_url.startswith(pacserve_server):
            unlinked = False
            for d in self.pacman_conf.options['CacheDir']:
              file_cachepath = join(d, pkg.filename)
              sha256 = digest(file_cachepath)
              if sha256 is None:
                continue
              elif sha256 != pkg.sha256sum:
                unlink(file_cachepath)
                unlinked = True
                continue
              else:
                found = True
                break
            else:
              # If a file was removed, it may have been the one found by Pacserve.
              # Requery to be sure. This time we know that a returned local URL
              # cannot point to the same cached file.
              if unlinked:
                found_url, try_pacserve = search_pacserve(pacserve_url)
                if found_url is None:
                  use_pacserve = False
            if found:
              continue
          if use_pacserve:
            urls = [found_url]
      if not use_pacserve \
      and not self.conf.get('rsync/db only') \
      and rsync_servers \
      and pkg.db.name in OFFICIAL_REPOSITORIES:
        rsync_queue.add_sync_pkg(pkg, urls, sigs)
      else:
        metalink_queue.add_sync_pkg(pkg, urls, sigs)

    metalink_queue.aur_pkgs = download_queue.aur_pkgs

    if metalink_queue:
      metalink = str(download_queue_to_metalink(metalink_queue)).encode()
      aria2_cmd = [
        self.conf.get('aria2/path'),
        '--metalink-file=-',
      ] + self.conf.get('aria2/args')
      aria2c_p = Popen(aria2_cmd, stdin=PIPE)
      aria2c_p.communicate(input=metalink)

    if rsync_queue:
      for rsync_server in rsync_servers:
        rsync_cmd = self.download_queue_to_rsync_cmd(
          rsync_server,
          rsync_queue,
          output_dir=pargs.output_dir
        )
        rsync_p = Popen(rsync_cmd)
        e = rsync_p.wait()
        if e == 0:
          # Success
          break
        elif e in RSYNC_DOWNLOAD_ERROR_EXIT_CODES:
          # Server error, try another one.
          continue
        else:
          die('error: rsync exited with %d\n> server: %s\n' % (e, rsync_server))
      else:
        # Fall back on Aria2
        metalink2 = str(download_queue_to_metalink(rsync_queue)).encode()
        aria2_cmd2 = [
          self.conf.get('aria2/path'),
          '--metalink-file=-',
        ] + self.conf.get('aria2/args')
        aria2c_p2 = Popen(aria2_cmd2, stdin=PIPE)
        aria2c_p2.communicate(input=metalink2)
        e = aria2c_p2.wait()
        if e not in ARIA2_DOWNLOAD_ERROR_EXIT_CODES:
          die('error: aria2c exited with %d\n' % e)

    if metalink_queue:
      e = aria2c_p.wait()
      if e not in ARIA2_DOWNLOAD_ERROR_EXIT_CODES:
        die('error: aria2c exited with %d\n' % e)


  def download(self, package):
    lock = Lockfile(join("/install/var/lib/pacman", 'db.lck'))
    powerpill = Powerpill(powerpill_conf, pacman_conf)

    '''
    pm2ml_args = ['-o', pacman_conf.options['CacheDir'][0]]
    if pargs['u'] > 0:
      pm2ml_args.append('-u')
    pm2ml_args.extend(pargs['pm2ml_options'])
    pm2ml_args.extend(pargs['args'])
    with lock:
      powerpill.download(pm2ml_args)
    '''
