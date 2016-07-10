#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  ${file.fileName}
#
#  Copyright ©  Antergos
#
#  This file is part of The Antergos Build Server, (AntBS).
#
#  AntBS is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  AntBS is distributed in the hope that it will be useful,
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
#  along with AntBS; If not, see <http://www.gnu.org/licenses/>.

__all__ = ['ALL_PAGES']

from ._01_language.language import LanguagePage
from ._02_welcome.welcome import WelcomePage
from ._03_check.check import CheckPage
from ._04_location.location import LocationPage
from ._05_desktop.desktop import DesktopPage
from ._06_features.features import FeaturesPage
from ._07_disk_setup.disk_setup import DiskSetupPage


class AllPages:
    pass

ALL_PAGES = AllPages()
ALL_PAGES.language = LanguagePage
ALL_PAGES.welcome = WelcomePage
ALL_PAGES.check = CheckPage
ALL_PAGES.location = LocationPage
ALL_PAGES.desktop = DesktopPage
ALL_PAGES.features = FeaturesPage
ALL_PAGES.disk_setup = DiskSetupPage

