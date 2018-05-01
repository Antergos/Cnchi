#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  alpm_events.py
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
# Processing the package transaction is starting.
ALPM_EVENT_TRANSACTION_START = 9
# Processing the package transaction is finished.
ALPM_EVENT_TRANSACTION_DONE = 10
# Package will be installed/upgraded/downgraded/re-installed/removed; See
# alpm_event_package_operation_t for arguments.
ALPM_EVENT_PACKAGE_OPERATION_START = 11
# Package was installed/upgraded/downgraded/re-installed/removed; See
# alpm_event_package_operation_t for arguments.
ALPM_EVENT_PACKAGE_OPERATION_DONE = 12
# Target package's integrity will be checked.
ALPM_EVENT_INTEGRITY_START = 13
# Target package's integrity was checked.
ALPM_EVENT_INTEGRITY_DONE = 14
# Target package will be loaded.
ALPM_EVENT_LOAD_START = 15
# Target package is finished loading.
ALPM_EVENT_LOAD_DONE = 16
# Target delta's integrity will be checked.
ALPM_EVENT_DELTA_INTEGRITY_START = 17
# Target delta's integrity was checked.
ALPM_EVENT_DELTA_INTEGRITY_DONE = 18
# Deltas will be applied to packages.
ALPM_EVENT_DELTA_PATCHES_START = 19
# Deltas were applied to packages.
ALPM_EVENT_DELTA_PATCHES_DONE = 20
# Delta patch will be applied to target package; See
# alpm_event_delta_patch_t for arguments..
ALPM_EVENT_DELTA_PATCH_START = 21
# Delta patch was applied to target package.
ALPM_EVENT_DELTA_PATCH_DONE = 22
# Delta patch failed to apply to target package.
ALPM_EVENT_DELTA_PATCH_FAILED = 23
# Scriptlet has printed information; See alpm_event_scriptlet_info_t for
# arguments.
ALPM_EVENT_SCRIPTLET_INFO = 24
# Files will be downloaded from a repository.
ALPM_EVENT_RETRIEVE_START = 25
# Files were downloaded from a repository.
ALPM_EVENT_RETRIEVE_DONE = 26
# Not all files were successfully downloaded from a repository.
ALPM_EVENT_RETRIEVE_FAILED = 27
# A file will be downloaded from a repository; See alpm_event_pkgdownload_t
# for arguments
ALPM_EVENT_PKGDOWNLOAD_START = 28
# A file was downloaded from a repository; See alpm_event_pkgdownload_t
# for arguments
ALPM_EVENT_PKGDOWNLOAD_DONE = 29
# A file failed to be downloaded from a repository; See
# alpm_event_pkgdownload_t for arguments
ALPM_EVENT_PKGDOWNLOAD_FAILED = 30
# Disk space usage will be computed for a package.
ALPM_EVENT_DISKSPACE_START = 31
# Disk space usage was computed for a package.
ALPM_EVENT_DISKSPACE_DONE = 32
# An optdepend for another package is being removed; See
# alpm_event_optdep_removal_t for arguments.
ALPM_EVENT_OPTDEP_REMOVAL = 33
# A configured repository database is missing; See
# alpm_event_database_missing_t for arguments.
ALPM_EVENT_DATABASE_MISSING = 34
# Checking keys used to create signatures are in keyring.
ALPM_EVENT_KEYRING_START = 35
# Keyring checking is finished.
ALPM_EVENT_KEYRING_DONE = 36
# Downloading missing keys into keyring.
ALPM_EVENT_KEY_DOWNLOAD_START = 37
# Key downloading is finished.
ALPM_EVENT_KEY_DOWNLOAD_DONE = 38
# A .pacnew file was created; See alpm_event_pacnew_created_t for arguments.
ALPM_EVENT_PACNEW_CREATED = 39
# A .pacsave file was created; See alpm_event_pacsave_created_t for
# arguments
ALPM_EVENT_PACSAVE_CREATED = 40
# Processing hooks will be started.
ALPM_EVENT_HOOK_START = 41
# Processing hooks is finished.
ALPM_EVENT_HOOK_DONE = 42
# A hook is starting
ALPM_EVENT_HOOK_RUN_START = 43
# A hook has finnished runnning
ALPM_EVENT_HOOK_RUN_DONE = 44

# Package (to be) installed. (No oldpkg)
ALPM_PACKAGE_INSTALL = 1,
# Package (to be) upgraded
ALPM_PACKAGE_UPGRADE = 2
# Package (to be) re-installed.
ALPM_PACKAGE_REINSTALL = 3
# Package (to be) downgraded.
ALPM_PACKAGE_DOWNGRADE = 4
# Package (to be) removed. (No newpkg)
ALPM_PACKAGE_REMOVE = 5

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
