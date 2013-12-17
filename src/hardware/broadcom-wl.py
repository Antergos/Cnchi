#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  broadcom-wl.py
#
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

""" Broadcom-wl driver installation """

from hardware import Hardware

class Broadcom-wl(Hardware):
    def __init__(self):
        pass
        
    def get_packages(self):
        pkgs = [ "broadcom-wl" ]
    
    def postinstall(self):
        pass

    def check_pci(self, pci):
        # check that vendor and pciid are ok
        pass
