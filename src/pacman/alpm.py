#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  alpm.py
#
#  Copyright © 2013,2014 Antergos
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

""" ALPM Events from alpm.h """

# Dependencies will be computed for a package.
ALPM_EVENT_CHECKDEPS_START = 1

# Dependencies were computed for a package.
ALPM_EVENT_CHECKDEPS_DONE = 2

# File conflicts will be computed for a package.
ALPM_EVENT_FILECONFLICTS_START = 3

# File conflicts were computed for a package.
ALPM_EVENT_FILECONFLICTS_DONE = 4

# Dependencies will be resolved for target package.
ALPM_EVENT_RESOLVEDEPS_START = 5

# Dependencies were resolved for target package.
ALPM_EVENT_RESOLVEDEPS_DONE = 6

# Inter-conflicts will be checked for target package.
ALPM_EVENT_INTERCONFLICTS_START = 7

# Inter-conflicts were checked for target package.
ALPM_EVENT_INTERCONFLICTS_DONE = 8

# Package will be installed.
# A pointer to the target package is passed to the callback.
ALPM_EVENT_ADD_START = 9

# Package was installed.
# A pointer to the new package is passed to the callback.
ALPM_EVENT_ADD_DONE = 10

# Package will be removed.
# A pointer to the target package is passed to the callback.
ALPM_EVENT_REMOVE_START = 11

# Package was removed.
# A pointer to the removed package is passed to the callback.
ALPM_EVENT_REMOVE_DONE = 12

# Package will be upgraded.
# A pointer to the upgraded package is passed to the callback.
ALPM_EVENT_UPGRADE_START = 13

# Package was upgraded.
# A pointer to the new package, and a pointer to the old package is passed to the callback, respectively.
ALPM_EVENT_UPGRADE_DONE = 14

# Package will be downgraded.
# A pointer to the downgraded package is passed to the callback.
ALPM_EVENT_DOWNGRADE_START = 15

# Package was downgraded.
# A pointer to the new package, and a pointer to the old package is passed to the callback, respectively.
ALPM_EVENT_DOWNGRADE_DONE = 16

# Package will be reinstalled.
# A pointer to the reinstalled package is passed to the callback.
ALPM_EVENT_REINSTALL_START = 17

# Package was reinstalled.
# A pointer to the new package, and a pointer to the old package is passed to the callback, respectively.
ALPM_EVENT_REINSTALL_DONE = 18

# Target package's integrity will be checked.
ALPM_EVENT_INTEGRITY_START = 19

# Target package's integrity was checked.
ALPM_EVENT_INTEGRITY_DONE = 20

# Target package will be loaded.
ALPM_EVENT_LOAD_START = 21

# Target package is finished loading.
ALPM_EVENT_LOAD_DONE = 22

# Target delta's integrity will be checked.
ALPM_EVENT_DELTA_INTEGRITY_START = 23

# Target delta's integrity was checked.
ALPM_EVENT_DELTA_INTEGRITY_DONE = 24

# Deltas will be applied to packages.
ALPM_EVENT_DELTA_PATCHES_START = 25

# Deltas were applied to packages.
ALPM_EVENT_DELTA_PATCHES_DONE = 26

# Delta patch will be applied to target package.
# The filename of the package and the filename of the patch is passed to the callback.
ALPM_EVENT_DELTA_PATCH_START = 27

# Delta patch was applied to target package.
ALPM_EVENT_DELTA_PATCH_DONE = 28

# Delta patch failed to apply to target package.
ALPM_EVENT_DELTA_PATCH_FAILED = 29

# Scriptlet has printed information.
# A line of text is passed to the callback.
ALPM_EVENT_SCRIPTLET_INFO = 30

# Files will be downloaded from a repository.
# The repository's tree name is passed to the callback.
ALPM_EVENT_RETRIEVE_START = 31

# Disk space usage will be computed for a package
ALPM_EVENT_DISKSPACE_START = 32

# Disk space usage was computed for a package
ALPM_EVENT_DISKSPACE_DONE = 33

# An optdepend for another package is being removed
# The requiring package and its dependency are passed to the callback
ALPM_EVENT_OPTDEP_REQUIRED = 34

# A configured repository database is missing
ALPM_EVENT_DATABASE_MISSING = 35

# Checking keys used to create signatures are in keyring.
ALPM_EVENT_KEYRING_START = 36

# Keyring checking is finished.
ALPM_EVENT_KEYRING_DONE = 37

# Downloading missing keys into keyring.
ALPM_EVENT_KEY_DOWNLOAD_START = 38

# Key downloading is finished.
ALPM_EVENT_KEY_DOWNLOAD_DONE = 39

# Progress
ALPM_PROGRESS_ADD_START = 0
ALPM_PROGRESS_UPGRADE_START = 1
ALPM_PROGRESS_DOWNGRADE_START = 2
ALPM_PROGRESS_REINSTALL_START = 3
ALPM_PROGRESS_REMOVE_START = 4
ALPM_PROGRESS_CONFLICTS_START = 5
ALPM_PROGRESS_DISKSPACE_START = 6
ALPM_PROGRESS_INTEGRITY_START = 7
ALPM_PROGRESS_LOAD_START = 8
ALPM_PROGRESS_KEYRING_START = 9
