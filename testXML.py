#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  testXML.py
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

import xml.etree.ElementTree as etree
import subprocess
import os

def select_packages(desktop, fs_devices, lang_code, install_bootloader, bootloader_type):
    '''The list of packages is retrieved from an online XML to let us
    control the pkgname in case of any modification'''
    
    print("Getting package list...")

    data_dir = 'data'
    packages_xml = os.path.join(data_dir, 'packages.xml')

    tree = etree.parse(packages_xml)
    root = tree.getroot()

    print("Adding all desktops common packages")

    packages = []
    conflicts = []

    for child in root.iter('common_system'):
        for pkg in child.iter('pkgname'):
            packages.append(pkg.text)

    if desktop != "nox":
        for child in root.iter('graphic_system'):
            for pkg in child.iter('pkgname'):
                packages.append(pkg.text)

        print("Adding '%s' desktop packages" % desktop)

        for child in root.iter(desktop + '_desktop'):
            for pkg in child.iter('pkgname'):
                # If package is Desktop Manager, save name to 
                # activate the correct service
                if pkg.attrib.get('dm'):
                    desktop_manager = pkg.attrib.get('name')
                if pkg.attrib.get('nm'):
                    network_manager = pkg.attrib.get('name')
                if pkg.attrib.get('conflicts'):
                    conflicts.append(pkg.attrib.get('conflicts'))
                packages.append(pkg.text)
    else:
        # Add specific NoX/Base packages
        for child in root.iter('nox'):
            for pkg in child.iter('pkgname'):
                if pkg.attrib.get('nm'):
                    network_manager = pkg.attrib.get('name')
                if pkg.attrib.get('conflicts'):
                    conflicts.append(pkg.attrib.get('conflicts'))
                packages.append(pkg.text)
    
    # Always install ntp as the user may want to activate it
    # later (or not) in the timezone screen
    for child in root.iter('ntp'):
        for pkg in child.iter('pkgname'):
            packages.append(pkg.text)

    # Install graphic cards drivers except in NoX installs
    if desktop != "nox":
        print("Getting graphics card drivers")

        graphics = "nvidia"
        card = []

        if "ati " in graphics:
            for child in root.iter('ati'):
                for pkg in child.iter('pkgname'):
                    packages.append(pkg.text)
            card.append('ati')
        
        if "nvidia" in graphics:
            for child in root.iter('nvidia'):
                for pkg in child.iter('pkgname'):
                    packages.append(pkg.text)
            card.append('nvidia')
        
        if "intel" in graphics or "lenovo" in graphics:
            for child in root.iter('intel'):
                for pkg in child.iter('pkgname'):
                    packages.append(pkg.text)
            card.append('intel')
        
        if "virtualbox" in graphics:
            for child in root.iter('virtualbox'):
                for pkg in child.iter('pkgname'):
                    packages.append(pkg.text)
        
        if "vmware" in graphics:
            for child in root.iter('vmware'):
                for pkg in child.iter('pkgname'):
                    packages.append(pkg.text)
        
        if "via " in graphics:
            for child in root.iter('via'):
                for pkg in child.iter('pkgname'):
                    packages.append(pkg.text)

        # Add xorg-drivers group if cnchi can't figure it out
        # the graphic card driver.
        if graphics not in ('ati ', 'nvidia', 'intel', 'virtualbox' \
                            'vmware', 'via '):
            packages.append('xorg-drivers')
    
    # Add filesystem packages
    
    print("Adding filesystem packages")
    
    fs_types = subprocess.check_output(\
        ["blkid", "-c", "/dev/null", "-o", "value", "-s", "TYPE"]).decode()
    
    for iii in fs_devices:
        fs_types += fs_devices[iii]
    
    if "ntfs" in fs_types:
        for child in root.iter('ntfs'):
            for pkg in child.iter('pkgname'):
                packages.append(pkg.text)
    
    if "btrfs" in fs_types:
        for child in root.iter('btrfs'):
            for pkg in child.iter('pkgname'):
                packages.append(pkg.text)

    if "nilfs2" in fs_types:
        for child in root.iter('nilfs2'):
            for pkg in child.iter('pkgname'):
                packages.append(pkg.text)

    if "ext" in fs_types:
        for child in root.iter('ext'):
            for pkg in child.iter('pkgname'):
                packages.append(pkg.text)

    if "reiserfs" in fs_types:
        for child in root.iter('reiserfs'):
            for pkg in child.iter('pkgname'):
                packages.append(pkg.text)

    if "xfs" in fs_types:
        for child in root.iter('xfs'):
            for pkg in child.iter('pkgname'):
                packages.append(pkg.text)

    if "jfs" in fs_types:
        for child in root.iter('jfs'):
            for pkg in child.iter('pkgname'):
                packages.append(pkg.text)

    if "vfat" in fs_types:
        for child in root.iter('vfat'):
            for pkg in child.iter('pkgname'):
                packages.append(pkg.text)

    # Check for user desired features and add them to our installation
    print("Check for user desired features and add them to our installation")
    features = ["aur", "bluetooth", "cups", "gnome_extra", "office", "visual", "firewall", "third_party"]
   
    lib = {'gtk':["gnome", "cinnamon", "xfce", "openbox" ], 'qt':[ "razor", "kde" ]}

    # TODO: Test this (KDE is not working)
    for feature in features:
        # Add necessary packages for all features (for testing purposes)
        print('Adding packages for "%s" feature.' % feature)
        for child in root.iter(feature):
            for pkg in child.iter('pkgname'):
                # If it's a specific gtk or qt package we have to check it
                # against our chosen desktop.
                plib = pkg.attrib.get('lib')
                
                if plib is None or (plib in lib and desktop in lib[plib]):
                    print(pkg.text)
                    packages.append(pkg.text)

    '''
    # Add libreoffice language package
    pkg = ""
    lang_name = "catalan"
    if lang_name == "english":
        # There're some English variants available but not all of them.
        lang_packs = [ 'en-GB', 'en-US', 'en-ZA' ]
        locale = self.settings.get('locale').split('.')[0]
        locale = locale.replace('_', '-')
        if locale in lang_packs:
            pkg = "libreoffice-%s" % locale
        else:
            # Install American English if there is not an specific
            # language package available.
            pkg = "libreoffice-en-US"
    else:
        # All the other language packs use their language code
        lang_code = self.settings.get('language_code')
        lang_code = lang_code.replace('_', '-')
        pkg = "libreoffice-%s" % lang_code
    packages.append(pkg)
    '''
    
    # Add chinese fonts
    if lang_code == "zh_TW" or lang_code == "zh_CN":
        print('Selecting chinese fonts.')
        for child in root.iter('chinese'):
            for pkg in child.iter('pkgname'):
                packages.append(pkg.text)

    # Add bootloader packages if needed
    print("Adding bootloader packages if needed")
    if install_bootloader:
        bt = bootloader_type
        if bt == "GRUB2":
            for child in root.iter('grub'):
                for pkg in child.iter('pkgname'):
                    packages.append(pkg.text)
        elif bt == "UEFI_x86_64":
            for child in root.iter('grub-efi'):
                if root.attrib.get('uefiarch') == "x86_64":
                    for pkg in child.iter('pkgname'):
                        packages.append(pkg.text)
        elif bt == "UEFI_i386":
            for child in root.iter('grub-efi'):
                if root.attrib.get('uefiarch') == "i386":
                    for pkg in child.iter('pkgname'):
                        packages.append(pkg.text)

if __name__ == '__main__':
    select_packages(desktop="kde", fs_devices={'0':"ext4"}, lang_code="ca_ES", install_bootloader=True, bootloader_type="GRUB2")
    
