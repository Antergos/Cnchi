#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cnchi.py
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

""" Main Cnchi (Antergos Installer) module """

# Useful vars for gettext (translations)
APP_NAME = "cnchi"
LOCALE_DIR = "/usr/share/locale"

from gi.repository import Gtk, Gdk, GObject, Gio
import os
import sys
import logging
import gettext
import locale

# Insert the src directory at the front of the path
BASE_DIR = os.path.dirname(__file__) or '.'
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)

import canonical.misc as misc
import info
import updater

# Command line options
cmd_line = None

# At least this GTK version is needed
GTK_VERSION_NEEDED = "3.9.6"

class CnchiApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        
    def do_activate(self):
        """ Override the 'activate' signal of GLib.Application. """
        try:
            import mainwindow
        except Exception as err:
            logging.exception(err)
            logging.error(_("Can't create Cnchi's main window. Exiting..."))
            sys.exit(1)
            
        window = mainwindow.MainWindow(self, cmd_line)
        
        # Some tutorials show that this line is needed, some don't
        # It seems to work ok without
        #self.add_window(window)
        
        # This is unnecessary as show_all is called in MainWindow
        #window.show_all()
    
    def do_startup(self):
        """ Override the 'startup' signal of GLib.Application. """
        Gtk.Application.do_startup(self)
        
        # Application main menu (we don't need one atm)
        # Leaving this here for future reference
        #menu = Gio.Menu()
        #menu.append("About", "win.about")
        #menu.append("Quit", "app.quit")
        #self.set_app_menu(menu)

def setup_logging():
    """ Configure our logger """
    logger = logging.getLogger()
    
    logger.handlers = []
   
    if cmd_line.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    logger.setLevel(log_level)
    
    # Log format
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s] %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    
    # Create file handler
    file_handler = logging.FileHandler('/tmp/cnchi.log', mode='w')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if cmd_line.verbose:
        # Show log messages to stdout
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

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

    # Cnchi will be called from our liveCD that already has the latest GTK version
    # This is here just to help testing Cnchi in our environment.
    if major_needed > major or (major_needed == major and minor_needed > minor) or \
      (major_needed == major and minor_needed == minor and micro_needed > micro):
        print("Detected GTK %d.%d.%d but %s is needed. Can't run this installer." \
            % (major, minor, micro, _gtk_version_needed))
        return False
    else:
        print("Using GTK v%d.%d.%d" % (major, minor, micro))

    return True

def parse_options():
    """ argparse http://docs.python.org/3/howto/argparse.html """

    import argparse
    parser = argparse.ArgumentParser(description="Cnchi v%s - Antergos Installer" % info.CNCHI_VERSION)
    parser.add_argument("-a", "--aria2", help=_("Use aria2 to download Antergos packages (EXPERIMENTAL)"), action="store_true")
    parser.add_argument("-c", "--cache", help=_("Use pre-downloaded xz packages (Cnchi will download them anyway if a new version is found)"), nargs='?')
    parser.add_argument("-cc", "--copycache", help=_("As --cache but before installing Cnchi copies all xz packages to destination"), nargs='?')
    parser.add_argument("-d", "--debug", help=_("Sets Cnchi log level to 'debug'"), action="store_true")
    parser.add_argument("-u", "--update", help=_("Update Cnchi to the latest version (-uu will force the update)"), action="count")
    parser.add_argument("-p", "--packagelist", help=_("Install the packages referenced by a local xml instead of the default ones"), nargs='?')
    parser.add_argument("-t", "--testing", help=_("Do not perform any changes (useful for developers)"), action="store_true")
    parser.add_argument("-v", "--verbose", help=_("Show logging messages to stdout"), action="store_true")
    parser.add_argument("--disable-tryit", help=_("Disables the tryit option (useful if Cnchi is not run from a liveCD)"), action="store_true")
    parser.add_argument("-z", "--z_hidden", help=_("Show options in development (DO NOT USE THIS!)"), action="store_true")

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
        # Unfortunately these versions of PyGObject suffer a bug which require a workaround to get
        # threading working properly. Workaround:
        # Force GIL creation
        import threading
        threading.Thread(target=lambda: None).start()

    # Since version 3.10.2, calling threads_init is no longer needed.
    # See: https://wiki.gnome.org/PyGObject/Threading
    if minor < 10 or (minor == 10 and micro < 2):
        GObject.threads_init()
    
    #Gdk.threads_init()

def update_cnchi():
    force = False
    if cmd_line.update == 2:
        force = True
    upd = updater.Updater(force)
    if upd.update():
        remove_temp_files()
        if force:
            # Remove -uu option
            new_argv = []
            for argv in sys.argv:
                if argv != "-uu":
                    new_argv.append(argv)
        else:
            new_argv = sys.argv
        print(_("Program updated! Restarting..."))
        # Run another instance of Cnchi (which will be the new version)
        os.execl(sys.executable, *([sys.executable] + new_argv))
        sys.exit(0)   

def setup_gettext():
    # This allows to translate all py texts (not the glade ones)
    gettext.textdomain(APP_NAME)
    gettext.bindtextdomain(APP_NAME, LOCALE_DIR)

    locale_code, encoding = locale.getdefaultlocale()
    lang = gettext.translation(APP_NAME, LOCALE_DIR, [locale_code], None, True)
    lang.install()

def check_for_files():
    # Check for hwinfo and hdparm
    # (this check is just for developers, in our liveCD hwinfo will always be installed)
    if not os.path.exists("/usr/bin/hwinfo"):
        print(_("Please install %s before running this installer") % "hwinfo")
        return False

    if not os.path.exists("/usr/bin/hdparm") and not os.path.exists("/sbin/hdparm"):
        print(_("Please install %s before running this installer") % "hdparm")
        return False
    
    return True

def init_cnchi():
    """ This function initialises Cnchi """

    # Configures gettext to be able to translate messages, using _()
    setup_gettext()
    
    if not check_for_files():
        sys.exit(1)
        
    # Check installed GTK version
    if not check_gtk_version():
        sys.exit(1)

    # Command line options
    global cmd_line
    cmd_line = parse_options()

    if cmd_line.update is not None:
        update_cnchi()
    
    # Drop root privileges
    misc.drop_privileges()
    
    # Init PyObject Threads
    threads_init()

    # Setup our logging framework
    setup_logging()
    

if __name__ == '__main__':
    init_cnchi()

    # Create Gtk Application    
    myapp = CnchiApp()
    exit_status = myapp.run(None)
    sys.exit(exit_status)
