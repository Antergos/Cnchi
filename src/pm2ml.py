#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Copyright (C) 2012-2013 Xyne
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# (version 2) as published by the Free Software Foundation.
#
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# TODO
# Refactor handling of signature options.

from collections import deque
from os.path import basename, join, relpath
from pycman import config
from xml.dom.minidom import getDOMImplementation
import argparse
import errno
import hashlib
import pyalpm
import re
import sys


PACMAN_OPTIONS = set((
  '-d', '--nodeps',
  '--ignore',
  '--ignoregroup',
  '--needed',
  '-u', '--sysupgrade',
  '-y', '--refresh',
  '--noconfirm',
))

PREFERENCE_MAX = 100
PREFERENCE_MIN = 1


################################################################################
# Temporary code. A patch has been submitted upstream to pyalpm
################################################################################

import os
from pycman.config import pacman_conf_enumerator, _logmask, cb_log, LIST_OPTIONS, BOOLEAN_OPTIONS
from collections import OrderedDict


class PacmanConfig(OrderedDict):
  def __init__(self, conf = None, options = None):
    super(PacmanConfig, self).__init__()
    self['options'] = OrderedDict()
    self.options = self['options']
    self.repos = OrderedDict()
    self.options["RootDir"] = "/"
    self.options["DBPath"]  = "/var/lib/pacman"
    self.options["GPGDir"]  = "/etc/pacman.d/gnupg/"
    self.options["LogFile"] = "/var/log/pacman.log"
    self.options["IgnorePkg"] = []
    self.options["IgnoreGroup"] = []
    self.options["SigLevel"] = 'Optional'
    self.options["Architecture"] = os.uname()[-1]
    if conf is not None:
      self.load_from_file(conf)
    if options is not None:
      self.load_from_options(options)

  def load_from_file(self, filename):
    for section, key, value in pacman_conf_enumerator(filename):
      if key == 'Architecture' and value == 'auto':
        continue
      self.setdefault(section, OrderedDict())
      if key in LIST_OPTIONS:
        self[section].setdefault(key, []).append(value)
      else:
        self[section][key] = value
    if "CacheDir" not in self.options:
      self.options["CacheDir"]= ["/var/cache/pacman/pkg"]
    for key, value in self.items():
      # For backwards compabilitility
      if key != 'options':
        self.repos[key] = self[key]['Server']

        if 'LocalFileSigLevel' not in value:
          value['LocalFileSigLevel'] = self.options['SigLevel']
        if 'RemoteFileSigLevel' not in value:
          value['RemoteFileSigLevel'] = self.options['SigLevel']

      if 'SigLevel' not in value:
        value['SigLevel'] = self.options['SigLevel']

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
    h.logcb = cb_log

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
    conf = ''
    for section, options in self.items():
      conf += '[%s]\n' % section
      for key, value in options.items():
        if key in LIST_OPTIONS:
          for v in value:
            conf += '%s = %s\n' % (key, v)
        elif key in BOOLEAN_OPTIONS:
          conf += key + '\n'
        else:
          conf += '%s = %s\n' % (key, value)
      conf += '\n'
    return conf

################################################################################




class PkgSet(object):
  def __init__(self, pkgs=[]):
    self.pkgs = dict()
    for pkg in pkgs:
      self.pkgs[pkg.name] = pkg

  def __repr__(self):
    return 'PkgSet(%s)' % repr(self.pkgs)

  def add(self, pkg):
    self.pkgs[pkg.name] = pkg

#   def remove(self, pkg):
#     if isinstance(pkg, str):
#       name = pkg
#     else:
#       name = pkg.name
#     del self.pkgs[name]

  def ignore(self, pkgs, groups):
    for name, pkg in tuple(self.pkgs.items()):
      if name in pkgs:
        del self.pkgs[name]
      else:
        for grp in pkg.groups:
          if grp in groups:
            del self.pkgs[name]
            break

  def __and__(self, other):
    new = PkgSet(set(self.pkgs.values()) & set(other.pkgs.values()))
    return new

  def __iand__(self, other):
    self.pkgs = self.__and__(other).pkgs
    return self

  def __or__(self, other):
    copy = PkgSet(self.pkgs.values())
    return copy.__ior__(other)

  def __ior__(self, other):
    self.pkgs.update(other.pkgs)
    return self

  def __contains__(self, pkg):
    return pkg.name in self.pkgs

  def __iter__(self):
    for v in self.pkgs.values():
      yield v

  def __len__(self):
    return len(self.pkgs)





# Make reflector support optional.
try:
  from Reflector import MirrorStatus as MS
  REPOSITORIES = MS.REPOSITORIES
  MIRROR_URL_FORMAT = MS.MIRROR_URL_FORMAT
except ImportError:
  REPOSITORIES = set()
  MIRROR_URL_FORMAT = None


def search_aur(names):
  """Search the AUR for the given pkgnames."""
  if not search_aur.aur:
    import AUR.RPC
    search_aur.aur = aur = AUR.RPC.AUR(log_func=lambda x,y: None)
  try:
    return AUR.RPC.insert_full_urls(search_aur.aur.info(names))
  except AUR.RPC.AURError as e:
    sys.stderr.write(str(e))
    sys.exit(1)
search_aur.aur = None



def determine_upgradable(handle, check_aur=False, aur_only=False, aur_names=None):
  """Determine upgradable packages in the repos and the AUR.

  Additional AUR pkgnames can be passed to this function to enable a single
  query to the AUR.
  """

  official = PkgSet()
  other = PkgSet()
  foreign = PkgSet()
  aur = []
  if not aur_names:
    aur_names =  set()

  if aur_only:
    check_aur = True

  global REPOSITORIES

  for pkg in handle.get_localdb().pkgcache:
    for db in handle.get_syncdbs():
      syncpkg = db.get_pkg(pkg.name)
      if syncpkg:
        if not aur_only:
          if pyalpm.vercmp(syncpkg.version, pkg.version) > 0:
            if db.name in REPOSITORIES:
              official.add(syncpkg)
            else:
              other.add(syncpkg)
        break
    else:
      if check_aur:
        foreign.add(pkg)

  if check_aur and foreign:
    aur_pkgs = search_aur(aur_names | set(foreign.pkgs))

    for aur_pkg in aur_pkgs:
      if aur_pkg['Name'] in aur_names:
        aur.append(aur_pkg)
        continue
      installed_pkg = foreign.pkgs[aur_pkg['Name']]
      if pyalpm.vercmp(aur_pkg['Version'], installed_pkg.version) > 0:
        aur.append(aur_pkg)

  return official, other, aur



class Metalink():
  def __init__(self, impl, output_dir=None, set_preference=False):
    self.doc = impl.createDocument(None, "metalink", None)
    self.doc.documentElement.setAttribute('xmlns', "urn:ietf:params:xml:ns:metalink")
    self.files = self.doc.documentElement
    self.set_output_dir(output_dir)
    self.set_preference = set_preference

  def __str__(self):
    return re.sub(
      r'(?<=>)\n\s*([^\s<].*?)\s*\n\s*',
      r'\1',
      self.doc.toprettyxml(indent=' ')
    )


  def set_output_dir(self, output_dir=None):
    if not output_dir:
      self.output_dir = None
    else:
      self.output_dir = relpath(output_dir)

  def add_urls(self, element, urls):
    """Add URL elements to the given element."""
    if self.set_preference:
      # This is necessary to get the length if `urls` is a generator.
      if not isinstance(urls, list):
        urls = list(urls)
      p = float(PREFERENCE_MAX)
      n = len(urls)
      dp = max((p / n), 1.0)

    for url in urls:
      url_tag = self.doc.createElement('url')
      element.appendChild(url_tag)
      if self.set_preference:
        url_tag.setAttribute('preference', '{:0.0f}'.format(p))
        p = max((p - dp), PREFERENCE_MIN)
      url_val = self.doc.createTextNode(url)
      url_tag.appendChild(url_val)


  def add_sync_pkg(self, pkg, urls, sigs=False):
    """Add a sync db package."""
    file_ = self.doc.createElement("file")
    if self.output_dir:
      file_.setAttribute("name", join(self.output_dir, pkg.filename))
    else:
      file_.setAttribute("name", pkg.filename)
    self.files.appendChild(file_)
    for tag, db_attr, attrs in (
      ('identity', 'name', ()),
      ('size', 'size', ()),
      ('version', 'version', ()),
      ('description', 'desc', ()),
      ('hash', 'sha256sum', (('type','sha256'),)),
      ('hash', 'md5sum', (('type','md5'),))
    ):
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
    if self.output_dir:
      file_.setAttribute("name", join(self.output_dir, name))
    else:
      file_.setAttribute("name", name)
    self.files.appendChild(file_)
    self.add_urls(file_, urls)


  def add_db(self, db, sigs=False):
    """Add a sync db."""
    file_ = self.doc.createElement("file")
    name = db.name + '.db'
    if self.output_dir:
      file_.setAttribute("name", join(self.output_dir, name))
    else:
      file_.setAttribute("name", name)
    self.files.appendChild(file_)
    urls = list(join(url, db.name + '.db') for url in db.servers)
    self.add_urls(file_, urls)
    if sigs:
      self.add_file(name + '.sig', (u + '.sig' for u in urls))


  def add_aur_pkg(self, pkg):
    """Add an AUR pkg."""
    file_ = self.doc.createElement("file")
    if self.output_dir:
      file_.setAttribute("name", join(self.output_dir, basename(pkg['URLPath'])))
    else:
      file_.setAttribute("name", basename(pkg['URLPath']))
    self.files.appendChild(file_)
    for tag, key in (
      ('identity', 'Name'),
      ('version', 'Version'),
      ('description', 'Description'),
      ('url', 'URLPath')
    ):
      tag = self.doc.createElement(tag)
      file_.appendChild(tag)
      val = self.doc.createTextNode(pkg[key])
      tag.appendChild(val)





class DownloadQueue():
  def __init__(self):
    self.dbs = list()
    self.sync_pkgs = list()
    self.aur_pkgs = list()

  def __bool__(self):
    return bool(self.dbs or self.sync_pkgs or self.aur_pkgs)

  def __nonzero__(self):
    return self.dbs or self.sync_pkgs or self.aur_pkgs

  def add_db(self, db, sigs=False):
    self.dbs.append((db, sigs))

  def add_sync_pkg(self, pkg, urls, sigs=False):
    self.sync_pkgs.append((pkg, urls, sigs))

  def add_aur_pkg(self, pkg):
    self.aur_pkgs.append(pkg)




def parse_args(args):
  parser = argparse.ArgumentParser(
    description='Download packages using parallel downloads.',
    prog='pm2ml',
  )
  parser.add_argument(
    'pkgs', nargs='*', default=[], metavar='<pkgname>',
    help='Packages or groups to download.'
  )
  parser.add_argument(
    '--all-deps', action='store_true', dest='alldeps',
    help='Include all dependencies even if they are already installed.'
  )
  parser.add_argument(
    '-a', '--aur', action='store_true', dest='aur',
    help='Enable AUR support.'
  )
  parser.add_argument(
    '--ask', action='store_true', dest='ask',
    help='Present a package selection dialogue for package groups. This may be overridden by --noconfirm.'
  )
  parser.add_argument(
    '--aur-only', action='store_true', dest='aur_only',
    help='Only download AUR archives. Use with "-u" to only download tarballs for upgradable AUR packages.'
  )
  parser.add_argument(
    '-c', '--conf', metavar='<path>', default='/etc/pacman.conf', dest='conf',
    help='Use a different pacman.conf file.'
  )
  parser.add_argument(
    '--noconfirm', action='store_true', dest='noconfirm',
    help='Suppress user prompts.'
  )
  parser.add_argument(
    '-d', '--nodeps', action='store_true', dest='nodeps',
    help='Skip dependencies.'
  )
  parser.add_argument(
    '--ignore', action='append', dest='ignore', default=[], metavar='<pkgname>',
    help='Ignore designated package.'
  )
  parser.add_argument(
    '--ignoregroup', action='append', dest='ignoregroup', default=[], metavar='<grpname>',
    help='Ignore packages belonging to designated groups.'
  )
  parser.add_argument(
    '--needed', action='store_true', dest='needed',
    help='Skip packages if they already exist in the cache.'
  )
  parser.add_argument(
    '-o', '--output-dir', metavar='<path>', dest='output_dir',
    help='Set the output directory.'
  )
  parser.add_argument(
    '-p', '--preference', action='store_true', dest='preference',
    help='Use preference attributes in URL elements in the metalink.'
  )
  parser.add_argument(
    '-r', '--reflector', nargs=argparse.REMAINDER, dest='reflector',
    help='Enable Reflector support and treat remaining arguments as Reflector arguments. E.g. "-r --latest 50'
  )
  parser.add_argument(
    '-s', '--sigs', action='count', default=0, dest='sigs',
    help='Include signature files for repos with optional and required SigLevels. Pass this flag twice to attempt to download signature for all databases and packages.'
  )
  parser.add_argument(
    '-u', '--upgrade', '--sysupgrade', action='store_true', dest='upgrade',
    help='Download upgradable packages.'
  )
  parser.add_argument(
    '-y', '--databases', '--refresh', action='store_true', dest='db',
    help='Download databases.'
  )
  return parser.parse_args(args)




def get_checksum(path, typ):
  h = hashlib.new(typ)
  b = h.block_size
  try:
    with open(path, 'rb') as f:
      buf = f.read(b)
      while buf:
        h.update(buf)
        buf = f.read(b)
    return h.hexdigest()
  except IOError as e:
    if e.errno != errno.ENOENT:
      raise e



def check_cache(conf, pkgs):
  for pkg in pkgs:
    for cache in conf.options['CacheDir']:
      fpath = join(cache, pkg.filename)
      for checksum in ('sha256', 'md5'):
        a = get_checksum(fpath, checksum)
        b = getattr(pkg, checksum + 'sum')
        if a is None or a != b:
          yield pkg
          break
      else:
        continue
      break


# TODO
# Use readline, curses or dialog to improve this.
def select_grp(grpname, pkgs, ignored):
  """
  Present the user with a dialogue to select packages from a group.
  """
  if not pkgs.pkgs:
    return pkgs
  selected = dict()
  for p in pkgs.pkgs:
    if p in ignored:
      selected[p] = False
    else:
      selected[p] = True
  names = sorted(selected)
  n = len(names)
  fmt = '[%s] %' + str(len(str(n+1))) + 'd %s'
  while True:
    print('Select packages from group "%s"' % (grpname,))
    for i in range(n):
      name = names[i]
      if selected[name]:
        marker = '*'
      else:
        marker = ' '
      print(fmt % (marker, i+1, name))
    changes = input('Use +n to select and -n to deselect, where n is the package number.\nEnter nothing or "x" to finalize selection.\nMultiple entries are permitted.\nModify current selection: ')
    finalized = not changes
    for number in changes.split():
      if number == 'x':
        finalized = True
        continue
      try:
        number = int(number)
        index = abs(number) - 1
        if index >= n:
          raise ValueError
      except ValueError:
        sys.stderr.write('error: invalid number [%s]\n' % number)
        finalized = False
        break
      selected[names[index]] = (number > 0)
    print()
    if finalized:
      break

  for k, v in selected.items():
    if not v:
      del pkgs.pkgs[k]
  return pkgs




def needs_sig(siglevel, insistence, prefix):
  """
  Determine if a signature should be downloaded. The siglevel is the pacman.conf
  SigLevel for the given repo. The insistence is an integer. Anything below 1
  will return false, anything above 1 will return true, and 1 will check if the
  siglevel is required or optional. The prefix is either "Database" or
  "Package".
  """
  if insistence > 1:
    return True
  elif insistence == 1 and siglevel:
    for sl in ('Required', 'Optional'):
      if siglevel == sl or siglevel == prefix + sl:
        return True
  return False




def build_download_queue(args=None, conf=None):
  pargs = parse_args(args)
  if not conf:
    conf = PacmanConfig(conf=pargs.conf)
  handle = conf.initialize_alpm()


  requested = set(pargs.pkgs)
  ignored = set(pargs.ignore)
  ignoredgroups = set(pargs.ignoregroup)
  official = PkgSet()
  other = PkgSet()
  foreign_names = set()
  missing_deps = list()
  found = set()
  not_found = set()

  global REPOSITORIES

  if pargs.aur_only:
    pargs.aur = True
  else:
    for pkg in requested:
      official_grp = PkgSet()
      other_grp = PkgSet()
      for db in handle.get_syncdbs():
        syncpkg = db.get_pkg(pkg)
        if syncpkg:
          if db.name in REPOSITORIES:
            official.add(syncpkg)
          else:
            other.add(syncpkg)
          break
        else:
          syncgrp = db.read_grp(pkg)
          if syncgrp:
            found.add(pkg)
            if db.name in REPOSITORIES:
              official_grp |= PkgSet(syncgrp[1])
            else:
              other_grp |= PkgSet(syncgrp[1])
      else:
        if pargs.ask and not pargs.noconfirm:
          selected = select_grp(pkg, official_grp | other_grp, ignored)
          official |= (official_grp & selected)
          other |= (other_grp & selected)
        else:
          official |= official_grp
          other |= other_grp

  foreign_names = requested - set(x.name for x in (official | other))


  if pargs.upgrade:
    a, b, c = determine_upgradable(
      handle,
      check_aur=pargs.aur,
      aur_only=pargs.aur_only,
      aur_names=foreign_names
    )
    official |= a
    other |= b
    aur = c
  elif pargs.aur:
    aur = list(search_aur(foreign_names))
  else:
    aur = []

  # Ignore packages before parsing deps.
  official.ignore(ignored, ignoredgroups)
  other.ignore(ignored, ignoredgroups)

  aur = [pkg for pkg in aur if pkg['Name'] not in ignored]

  # Resolve dependencies.
  if (official or other) and not pargs.nodeps:
    queue = deque(official | other)
    local_cache = handle.get_localdb().pkgcache
    syncdbs = handle.get_syncdbs()
    seen = set(queue)
    while queue:
      pkg = queue.popleft()
      for dep in pkg.depends:
        if pyalpm.find_satisfier(local_cache, dep) is None \
        or pargs.alldeps:
          for db in syncdbs:
            prov = pyalpm.find_satisfier(db.pkgcache, dep)
            if prov is not None:
              if db.name in REPOSITORIES:
                official.add(prov)
              else:
                other.add(prov)
              if prov.name not in seen:
                seen.add(prov.name)
                queue.append(prov)
              break
          else:
            missing_deps.append(dep)
    # Ignore packages after parsing deps.
    official.ignore(ignored, ignoredgroups)
    other.ignore(ignored, ignoredgroups)


  found |= set(official.pkgs) | set(other.pkgs) | set(p['Name'] for p in aur)
  not_found = requested - found
  if pargs.needed:
    official = PkgSet(check_cache(conf, official))
    other = PkgSet(check_cache(conf, other))

  download_queue = DownloadQueue()

  if pargs.db:
    for db in handle.get_syncdbs():
      try:
        siglevel = conf[db.name]['SigLevel'].split()[0]
      except KeyError:
        siglevel = None
      download_sig = needs_sig(siglevel, pargs.sigs, 'Database')
      download_queue.add_db(db, download_sig)

  if official:
    if pargs.reflector:
      from Reflector import parse_args as parse_reflector_args, process_options, MirrorStatusError
      reflector_options = parse_reflector_args(pargs.reflector)
      try:
        mirrorstatus, mirrors = process_options(reflector_options)
        mirrors = list(m['url'] for m in mirrors)
      except MirrorStatusError as e:
        sys.stderr.write(str(e))
        mirrors = []
    else:
      mirrors = []
    for pkg in official:
      # This preserves the order of the user's mirrorlist files and prevents
      # duplicates from being added by Reflector.
      urls = list(join(url,pkg.filename) for url in pkg.db.servers)
      urls.extend(
        set(
          join(MIRROR_URL_FORMAT.format(
            m, pkg.db.name, pkg.arch), pkg.filename
          ) for m in mirrors
        ) - set(urls)
      )

      try:
        siglevel = conf[pkg.db.name]['SigLevel'].split()[0]
      except KeyError:
        siglevel = None
      download_sig = needs_sig(siglevel, pargs.sigs, 'Package')
      download_queue.add_sync_pkg(pkg, urls, download_sig)

  for pkg in other:
    try:
      siglevel = conf[pkg.db.name]['SigLevel'].split()[0]
    except KeyError:
      siglevel = None
    download_sig = needs_sig(siglevel, pargs.sigs, 'Package')
    urls = set(join(url, pkg.filename) for url in pkg.db.servers)
    download_queue.add_sync_pkg(pkg, urls, download_sig)


  for pkg in aur:
    download_queue.add_aur_pkg(pkg)

  return pargs, conf, download_queue, not_found, missing_deps





# The intermediate DownloadQueue object is used to allow scripts to hook into
# the code.
def download_queue_to_metalink(download_queue, output_dir=None, set_preference=False):
  impl = getDOMImplementation()
  metalink = Metalink(impl, output_dir=output_dir, set_preference=set_preference)

  for db, sigs in download_queue.dbs:
    metalink.add_db(db, sigs)

  for pkg, urls, sigs in download_queue.sync_pkgs:
    metalink.add_sync_pkg(pkg, urls, sigs)

  for pkg in download_queue.aur_pkgs:
    metalink.append_aur_pkg(pkg)

  return metalink





def main(args=None):
  pargs, conf, download_queue, not_found, missing_deps = build_download_queue(args)
  metalink = download_queue_to_metalink(
    download_queue,
    output_dir=pargs.output_dir,
    set_preference=pargs.preference
  )
  print(metalink)

  if not_found:
    sys.stderr.write('Not found:\n')
    for nf in sorted(not_found):
      sys.stderr.write('  %s\n' % nf)
  if missing_deps:
    sys.stderr.write('Unresolved dependencies:\n')
    for md in sorted(missing_deps):
      sys.stderr.write('  %s\n' % md)



def run_main(args=None):
  try:
    main(args)
  except (KeyboardInterrupt, BrokenPipeError):
    pass


if __name__ == '__main__':
  run_main()
