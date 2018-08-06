# Cnchi ![GitHub release](https://img.shields.io/github/release/antergos/cnchi.svg)

**Graphical Installer for Antergos Linux**

![Read the docs](https://readthedocs.org/projects/cnchi/badge/?version=latest) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/141e37590a9e4a2da3b3d84c0a6241ac)](https://www.codacy.com/project/karasu/Cnchi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Antergos/Cnchi&amp;utm_campaign=Badge_Grade_Dashboard) ![License](https://img.shields.io/github/license/antergos/cnchi.svg)

![GitHub issues](https://img.shields.io/github/issues/antergos/cnchi.svg)
![Github commits](https://img.shields.io/github/commits-since/antergos/cnchi/latest.svg)

![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)

You are viewing the `0.16.x` branch (development).

## Current Status

|Development Stage|Branch|Version| Code Status|
----------------- | -------------- | -------------- | -------- |
|Cnchi Stable|0.14.x|![0.14.473](https://img.shields.io/github/release/antergos/cnchi.svg)|Frozen|
|Cnchi Development|0.16.x|![0.16.201](https://img.shields.io/github/release/antergos/cnchi/all.svg)|Development|
|Cnchi Next (UI agnostic)|master|0.17.x|Development|


## Usage:

```sh
sudo -E cnchi.py
```

#### Optional parameters:

|Command|Description|
----------------- | -------------- |
|```-a``` or ```--a11y```|*Set accessibility feature on by default*|
|```-c``` or ```--cache```|*Use pre-downloaded xz packages when possible*|
|```-d``` or ```--debug```|*Sets Cnchi log level to 'debug'*|
|```-e``` or ```--environment```|*Sets the Desktop Environment that will be installed, see [desktop_info.py](cnchi/desktop_info.py) for options*|
|```-f``` or ```--force```|*Runs cnchi even if it detects that another instance is running*|
|```-i``` or ```--disable-tryit```|*Disables first screen's 'try it' option*|
|```-n``` or ```--no-check```|*Makes checks optional in check screen*|
|```-p``` or ```--packagelist```|*Install the packages referenced by a local xml instead of the defaults, see [#617](https://github.com/Antergos/Cnchi/issues/617) for proper usage*|
|```-s``` or ```--log-server```|*Choose to which log server send Cnchi logs.  Expects a hostname or an IP address*|
|```-u``` or ```--update```|*Upgrade/downgrade Cnchi to the web version*|
|```--disable-update```|*Do not search for new Cnchi versions online*|
|```-v``` or ```--verbose```|*Show logging messages to stdout*|
|```-V``` or ```--version```|*Show Cnchi version and quit*|
|```-z``` or ```--z_hidden```|*Show options in development (for developers only, do not use this!)*|

To create logs to help debug problems:
```sh
sudo -E cnchi.py -dv -s bugsnag
```

## Reporting bugs:

Please report any issues with Cnchi in the issue tracker. Provide all log files along with a detailed description:

* /tmp/cnchi.log
* /tmp/postinstall.log (if it exists)
* /tmp/pacman.log (if it exists)

## Translations

We manage our translations via [Transifex](https://www.transifex.com/projects/p/antergos)

<a name="dependencies">Dependencies</a>

 - gtk3
 - python3
 - python-cairo
 - python-dbus
 - python-defusedxml
 - python-feedparser
 - python-gobject
 - python-mako
 - python-requests
 - geoip (python-geoip2, python-maxminddb, geoip2-database)
 - pyparted (parted, dosfstools, mtools, ntfs-3g, ntfsprogs)
 - pyalpm (alpm)
 - webkit2gtk
 - upower
 - gocryptfs
 - iso-codes
 - clutter, clutter-gtk, clutter-gst
 - gsteamer1.0

## Unit tests
 - python-mock

## Fonts needed by the keyboard widget
 - ttf-aboriginal-sans
 - ttf-indic-otf
 - ttf-khmer
 - ttf-lohit-fonts
 - ttf-myanmar3
 - ttf-thaana-fonts
 - ttf-tlwg

## Building Cnchi

[PKGBUILD](https://raw.githubusercontent.com/Antergos/antergos-packages/master/antergos/cnchi-dev/PKGBUILD)

## Development

### Getting started

You will need to install all [dependencies](#dependencies).

- Fork Cnchi
- Do your changes (use 0.16.x branch as base!)

Then, you can use the run script to test Cnchi. As this is a Installer, you will need to use a [Virtual Machine](http://virtualbox.org) or an additional harddisk to test it.

How to easy prepare a sane testing environment:
1. Download Antergos ISO
2. Create a new VM in Virtualbox, add the live iso and a virtual harddisk (two harddisks if you want to cache the downloaded packages)
3. Run the VM
4. Cnchi will open, close it.
5. Remove Cnchi ISO version: `sudo rm -rf /usr/share/cnchi`
6. Install git: `sudo pacman -S git`
7. Install - Install your Cnchi version from your own repository:
```
cd /home/antergos
git clone https://github.com/<username>/cnchi
cd cnchi
sudo ln -s /home/antergos/cnchi /usr/share/cnchi
```
8. Create a screenshot of the VM (so you don't have to redo all this each time you want to test your changes).
9. Run Cnchi and start testing!

If your tests are OK, you can then create your PR and push it here (against development branch, which now it's 0.16.x)

### Development Tips

When creating a Pull Request (PR), please check that you follow the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide (you have a stylized presentation at [pep8.org](http://pep8.org)). You can use [pycodestyle](https://github.com/pycqa/pycodestyle) (former pep8) or [pylint.org](https://www.pylint.org) or whatever you prefer to check your python3 files.

#### Spaces are the preferred indentation method.

### Documented classes

To start tinkering, we would recommend to check all open [#issues](https://github.com/Antergos/Cnchi/issues) and find one you find you will be able to start with (choose something that seems easy to do), so you feel familiar with cnchi's structure. You can find info about it at [readthedocs](https://cnchi.readthedocs.io/en/latest/)
