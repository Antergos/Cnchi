#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cnchi.py
#
#  Copyright © 2013-2017 Antergos
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

""" Main Cnchi (Antergos Installer) module """


import os
import sys
import shutil
import logging
import logging.handlers
import gettext
import locale
import gi


CNCHI_PATH = "/usr/share/cnchi"
sys.path.append(CNCHI_PATH)
sys.path.append(os.path.join(CNCHI_PATH, "src"))
sys.path.append(os.path.join(CNCHI_PATH, "src/download"))
sys.path.append(os.path.join(CNCHI_PATH, "src/hardware"))
sys.path.append(os.path.join(CNCHI_PATH, "src/installation"))
sys.path.append(os.path.join(CNCHI_PATH, "src/misc"))
sys.path.append(os.path.join(CNCHI_PATH, "src/pacman"))
sys.path.append(os.path.join(CNCHI_PATH, "src/pages"))
sys.path.append(os.path.join(CNCHI_PATH, "src/pages/dialogs"))
sys.path.append(os.path.join(CNCHI_PATH, "src/parted3"))


gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk, GObject

import misc.extra as misc
import show_message as show
import info

from logging_utils import ContextFilter

try:
    from bugsnag.handlers import BugsnagHandler
    import bugsnag
    BUGSNAG_ERROR = None
except ImportError as err:
    BUGSNAG_ERROR = str(err)

# When testing, no _() is available
try:
    _("")
except NameError as err:
    def _(message):
        return message

# Useful vars for gettext (translations)
APP_NAME = "cnchi"
LOCALE_DIR = "/usr/share/locale"

# Command line options
cmd_line = None

# At least this GTK version is needed
GTK_VERSION_NEEDED = "3.18.0"


class CnchiApp(Gtk.Application):
    """ Main Cnchi App class """

    def __init__(self):
        """ Constructor. Call base class """
        Gtk.Application.__init__(self,
                                 application_id="com.antergos.cnchi",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.tmp_running = "/tmp/.setup-running"

    def do_activate(self):
        """ Override the 'activate' signal of GLib.Application.
            Shows the default first window of the application (like a new document).
            This corresponds to the application being launched by the desktop environment. """
        try:
            import main_window
        except ImportError as err:
            msg = "Cannot create Cnchi main window: {0}".format(err)
            logging.error(msg)
            sys.exit(1)

        # Check if we have administrative privileges
        if os.getuid() != 0:
            msg = _('This installer must be run with administrative privileges, '
                    'and cannot continue without them.')
            show.error(None, msg)
            return

        # Check if we're already running
        if self.already_running():
            msg = _("You cannot run two instances of this installer.\n\n"
                    "If you are sure that the installer is not already running\n"
                    "you can run this installer using the --force option\n"
                    "or you can manually delete the offending file.\n\n"
                    "Offending file: '{0}'").format(self.tmp_running)
            show.error(None, msg)
            return

        window = main_window.MainWindow(self, cmd_line)
        self.add_window(window)
        window.show()

        with open(self.tmp_running, "w") as tmp_file:
            txt = "Cnchi {0}\n{1}\n".format(info.CNCHI_VERSION, os.getpid())
            tmp_file.write(txt)

        # This is unnecessary as show_all is called in MainWindow
        # window.show_all()

        # def do_startup(self):
        # """ Override the 'startup' signal of GLib.Application. """
        # Gtk.Application.do_startup(self)

        # Application main menu (we don't need one atm)
        # Leaving this here for future reference
        # menu = Gio.Menu()
        # menu.append("About", "win.about")
        # menu.append("Quit", "app.quit")
        # self.set_app_menu(menu)

    def already_running(self):
        """ Check if we're already running """
        if os.path.exists(self.tmp_running):
            logging.debug("File %s already exists.", self.tmp_running)
            with open(self.tmp_running) as setup:
                lines = setup.readlines()
            if len(lines) >= 2:
                try:
                    pid = int(lines[1].strip('\n'))
                except ValueError as err:
                    logging.debug(err)
                    logging.debug("Cannot read PID value.")
                    return True
            else:
                logging.debug("Cannot read PID value.")
                return True

            if misc.check_pid(pid):
                logging.info("Cnchi with pid '%d' already running.", pid)
                return True
            else:
                # Cnchi with pid 'pid' is no longer running, we can safely
                # remove the offending file and continue.
                os.remove(self.tmp_running)
        return False


def setup_logging():
    """ Configure our logger """
    logger = logging.getLogger()

    logger.handlers = []

    if cmd_line.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger.setLevel(log_level)

    context_filter = ContextFilter()
    logger.addFilter(context_filter.filter)

    # Log format
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(filename)s(%(lineno)d) %(funcName)s(): %(message)s")
        #datefmt="%Y-%m-%d %H:%M:%S")

    # File logger
    try:
        file_handler = logging.FileHandler('/tmp/cnchi.log', mode='w')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except PermissionError as permission_error:
        print("Can't open /tmp/cnchi.log : ", permission_error)

    # Stdout logger
    if cmd_line.verbose:
        # Show log messages to stdout
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    if cmd_line.log_server == 'bugsnag':
        if not BUGSNAG_ERROR:
            # Bugsnag logger
            bugsnag_api = context_filter.api_key
            if bugsnag_api is not None:
                bugsnag.configure(
                    api_key=bugsnag_api,
                    app_version=info.CNCHI_VERSION,
                    project_root='/usr/share/cnchi/cnchi',
                    release_stage=info.CNCHI_RELEASE_STAGE)
                bugsnag_handler = BugsnagHandler(api_key=bugsnag_api)
                bugsnag_handler.setLevel(logging.WARNING)
                bugsnag_handler.setFormatter(formatter)
                bugsnag_handler.addFilter(context_filter.filter)
                bugsnag.before_notify(
                    context_filter.bugsnag_before_notify_callback)
                logger.addHandler(bugsnag_handler)
                logging.info(
                    "Sending Cnchi log messages to bugsnag server (using python-bugsnag).")
            else:
                logging.warning(
                    "Cannot read the bugsnag api key, logging to bugsnag is not possible.")
        else:
            logging.warning(BUGSNAG_ERROR)


def check_gtk_version():
    """ Check GTK version """
    # Check desired GTK Version
    major_needed = int(GTK_VERSION_NEEDED.split(".")[0])
    minor_needed = int(GTK_VERSION_NEEDED.split(".")[1])
    micro_needed = int(GTK_VERSION_NEEDED.split(".")[2])

    # Check system GTK Version
    major = Gtk.get_major_version()
    minor = Gtk.get_minor_version()
    micro = Gtk.get_micro_version()

    # Cnchi will be called from our liveCD that already
    # has the latest GTK version. This is here just to
    # help testing Cnchi in our environment.
    wrong_gtk_version = False
    if major_needed > major:
        wrong_gtk_version = True
    if major_needed == major and minor_needed > minor:
        wrong_gtk_version = True
    if major_needed == major and minor_needed == minor and micro_needed > micro:
        wrong_gtk_version = True

    if wrong_gtk_version:
        text = "Detected GTK version {0}.{1}.{2} but version >= {3} is needed."
        text = text.format(major, minor, micro, GTK_VERSION_NEEDED)
        try:
            show.error(None, text)
        except ImportError as import_error:
            logging.error(import_error)
        return False
    else:
        logging.info("Using GTK v%d.%d.%d", major, minor, micro)

    return True


def check_pyalpm_version():
    """ Checks python alpm binding and alpm library versions """
    try:
        import pyalpm

        txt = "Using pyalpm v{0} as interface to libalpm v{1}"
        txt = txt.format(pyalpm.version(), pyalpm.alpmversion())
        logging.info(txt)
    except (NameError, ImportError) as err:
        try:
            show.error(None, err)
            logging.error(err)
        except ImportError as import_error:
            logging.error(import_error)
        return False

    return True


def check_iso_version():
    """ Hostname contains the ISO version """
    from socket import gethostname
    hostname = gethostname()
    # antergos-year.month-iso
    prefix = "ant-"
    suffix = "-min"
    if hostname.startswith(prefix) or hostname.endswith(suffix):
        # We're running form the ISO, register which version.
        if suffix in hostname:
            version = hostname[len(prefix):-len(suffix)]
        else:
            version = hostname[len(prefix):]
        logging.debug("Running from ISO version %s", version)
        # Delete user's chromium cache (just in case)
        cache_dir = "/home/antergos/.cache/chromium"
        if os.path.exists(cache_dir):
            shutil.rmtree(path=cache_dir, ignore_errors=True)
            logging.debug("User's chromium cache deleted")
        # If we're running from sonar iso force a11y parameter to true
        if hostname.endswith("sonar"):
            cmd_line.a11y = True
    else:
        logging.debug("Not running from ISO")
    return True


def parse_options():
    """ argparse http://docs.python.org/3/howto/argparse.html """

    import argparse

    desc = _("Cnchi v{0} - Antergos Installer").format(info.CNCHI_VERSION)
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        "-a", "--a11y",
        help=_("Set accessibility feature on by default"),
        action="store_true")
    parser.add_argument(
        "-c", "--cache",
        help=_("Use pre-downloaded xz packages when possible"),
        nargs='?')
    parser.add_argument(
        "-d", "--debug",
        help=_("Sets Cnchi log level to 'debug'"),
        action="store_true")
    parser.add_argument(
        "-e", "--environment",
        help=_("Sets the Desktop Environment that will be installed"),
        nargs='?')
    parser.add_argument(
        "-f", "--force",
        help=_("Runs cnchi even if it detects that another instance is running"),
        action="store_true")
    parser.add_argument(
        "-i", "--disable-tryit",
        help=_("Disables first screen's 'try it' option"),
        action="store_true")
    parser.add_argument(
        "-n", "--no-check",
        help=_("Makes checks optional in check screen"),
        action="store_true")
    parser.add_argument(
        "-p", "--packagelist",
        help=_(
            "Install the packages referenced by a local xml instead of the default ones"),
        nargs='?')
    parser.add_argument(
        "-s", "--log-server",
        help=_("Choose to which log server send Cnchi logs."
               " Expects a hostname or an IP address"),
        nargs='?')
    parser.add_argument(
        "-v", "--verbose",
        help=_("Show logging messages to stdout"),
        action="store_true")
    parser.add_argument(
        "-V", "--version",
        help=_("Show Cnchi version and quit"),
        action="store_true")
    parser.add_argument(
        "-z", "--z_hidden",
        help=_("Show options in development (for developers only, do not use this!)"),
        action="store_true")

    return parser.parse_args()


def threads_init():
    """
    For applications that wish to use Python threads to interact with the GNOME platform,
    GObject.threads_init() must be called prior to running or creating threads and starting
    main loops (see notes below for PyGObject 3.10 and greater). Generally, this should be done
    in the first stages of an applications main entry point or right after importing GObject.
    For multi-threaded GUI applications Gdk.threads_init() must also be called prior to running
    Gtk.main() or Gio/Gtk.Application.run().
    """
    minor = Gtk.get_minor_version()
    micro = Gtk.get_micro_version()

    if minor == 10 and micro < 2:
        # Unfortunately these versions of PyGObject suffer a bug
        # which require a workaround to get threading working properly.
        # Workaround: Force GIL creation
        import threading
        threading.Thread(target=lambda: None).start()

    # Since version 3.10.2, calling threads_init is no longer needed.
    # See: https://wiki.gnome.org/PyGObject/Threading
    if minor < 10 or (minor == 10 and micro < 2):
        GObject.threads_init()
        # Gdk.threads_init()


def setup_gettext():
    """ This allows to translate all py texts (not the glade ones) """

    gettext.textdomain(APP_NAME)
    gettext.bindtextdomain(APP_NAME, LOCALE_DIR)

    locale_code, _encoding = locale.getdefaultlocale()
    lang = gettext.translation(APP_NAME, LOCALE_DIR, [locale_code], None, True)
    lang.install()


def check_for_files():
    """ Check for some necessary files. Cnchi can't run without them """
    paths = [
        "/usr/share/cnchi",
        "/usr/share/cnchi/ui",
        "/usr/share/cnchi/data",
        "/usr/share/cnchi/data/locale"]

    for path in paths:
        if not os.path.exists(path):
            print(_("Cnchi files not found. Please, install Cnchi using pacman"))
            return False

    return True


def init_cnchi():
    """ This function initialises Cnchi """

    # Sets SIGTERM handler, so Cnchi can clean up before exiting
    # signal.signal(signal.SIGTERM, sigterm_handler)

    # Configures gettext to be able to translate messages, using _()
    setup_gettext()

    # Command line options
    global cmd_line
    cmd_line = parse_options()

    if cmd_line.version:
        print(_("Cnchi (Antergos Installer) version {0}").format(
            info.CNCHI_VERSION))
        sys.exit(0)

    if cmd_line.force:
        misc.remove_temp_files()

    # Drop root privileges
    misc.drop_privileges()

    # Setup our logging framework
    setup_logging()

    # Check Cnchi is correctly installed
    if not check_for_files():
        sys.exit(1)

    # Check installed GTK version
    if not check_gtk_version():
        sys.exit(1)

    # Check installed pyalpm and libalpm versions
    if not check_pyalpm_version():
        sys.exit(1)

    # Check ISO version where Cnchi is running from
    if not check_iso_version():
        sys.exit(1)

    # Init PyObject Threads
    threads_init()


if __name__ == '__main__':
    init_cnchi()

    # Create Gtk Application
    my_app = CnchiApp()
    status = my_app.run(None)
    sys.exit(status)
