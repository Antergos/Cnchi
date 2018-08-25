#!/usr/bin/python

import os
import subprocess
import sys

XML_URL="https://raw.githubusercontent.com/Antergos/Cnchi/master/data/packages.xml"
XML_FILE="packages.xml"

def get_pkg_names():
    """ Get pkg names from packages.xml """
    if os.path.exists(XML_FILE):
        os.remove(XML_FILE)

    cmd = ["curl", "-O", XML_URL, "--silent"]
    try:
        subprocess.call(cmd)
    except subprocess.CalledProcessError as err:
        print(err)

    if not os.path.exists(XML_FILE):
        print("Could not download xml file!")
        sys.exit(1)

    with open(XML_FILE, 'r') as myfile:
        lines = myfile.readlines()
    
    l1 = len("<pkgname>")
    l2 = len("</pkgname>")
    pkgs = []
    for line in lines:
        line = line.strip()
        if not "<!--" in line and not "-->" in line and "<pkgname>" in line:
            pkgs.append(line[l1:-l2])

    return sorted(list(set(pkgs)))

def check_names(pkgs):
    """ Checks if package exists calling pacman """
    not_found = []
    for pkg_name in pkgs:
        cmd = ["pacman", "-Ss", pkg_name]
        try:
            output = subprocess.check_output(cmd).decode()
        except subprocess.CalledProcessError:
            output = ""
        
        if pkg_name in output:
            print("{}...OK!".format(pkg_name))
        else:
            not_found.append(pkg_name)
            print("{}...NOT FOUND!".format(pkg_name))

    if not_found:
        print("These packages were not found:")
        print(" ".join(not_found))

if __name__ == '__main__':
    pkgs = get_pkg_names()
    check_names(pkgs)
