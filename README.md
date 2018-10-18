# Cnchi
**A modern, flexible system installer for Linux**

[![Codacy](https://img.shields.io/codacy/04b4ac624a0149efb8b4e9d143167660.svg?style=flat-square)](https://www.codacy.com/app/Antergos/Cnchi)&nbsp;&nbsp;[![Code Health](https://landscape.io/github/Antergos/Cnchi/master/landscape.svg?style=flat-square)](https://landscape.io/github/Antergos/Cnchi/master)
&nbsp;&nbsp;![Python 3.5](https://img.shields.io/badge/Python-3.5-blue.svg?style=flat-square)

*You are viewing the* ***`master`*** *branch*.

## Current Status

This is the latest, unreleased version of Cnchi, AKA: **Cnchi Next**.

|Development Stage|Branch|Version| Code Status|
----------------- | -------------- | -------------- | -------- |
|*Cnchi Legacy*|*0.12.x*|*v0.12.46*|*Frozen*|
|Cnchi Stable|[0.14.x](https://github.com/Antergos/Cnchi/tree/0.14.x)|v0.16.201|Bug Fixes Only|
|**Cnchi Next**|**master**|**v0.15.334**|**Development**|


## Usage:

```sh
$ cnchi
```

### Optional parameters:

|Command|Description|
----------------- | -------------- |
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
$ cnchi -dv -s bugsnag
```

## Reporting bugs:

Please report any issues with Cnchi in the issue tracker. Provide all log files along with a detailed description:

* `/tmp/cnchi.log`
* `/tmp/postinstall.log` (if it exists)
* `/tmp/pacman.log` (if it exists)

## Translations

We manage our translations via [Transifex](https://www.transifex.com/projects/p/antergos)

## Dependencies
Dependency information is available [here](https://github.com/Antergos/Cnchi/wiki/Dependencies).
