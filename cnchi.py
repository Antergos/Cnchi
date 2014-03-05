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

# TODO: Remove all force_grub code


# Useful vars for gettext (translations)
APP_NAME = "cnchi"
LOCALE_DIR = "/usr/share/locale"

# This allows to translate all py texts (not the glade ones)
import gettext
gettext.textdomain(APP_NAME)
gettext.bindtextdomain(APP_NAME, LOCALE_DIR)

import locale
locale_code, encoding = locale.getdefaultlocale()
lang = gettext.translation(APP_NAME, LOCALE_DIR, [locale_code], None, True)
lang.install()

from gi.repository import Gtk, Gdk, GObject, GLib
import os
import sys
import getopt
import locale
import multiprocessing
import logging

# Insert the src directory at the front of the path
BASE_DIR = os.path.dirname(__file__) or '.'
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)

import config
import welcome
import language
import location
import check
import desktop
import features
import keymap
import timezone
import user_info
import slides
import canonical.misc as misc
import info
import updater
import show_message as show
import desktop_environments as desktops

from installation import ask as installation_ask
from installation import automatic as installation_automatic
from installation import alongside as installation_alongside
from installation import advanced as installation_advanced

# Command line options
cmd_line = None

# Constants (must be uppercase)
MAIN_WINDOW_WIDTH = 800
MAIN_WINDOW_HEIGHT = 500

# At least this GTK version is needed
_gtk_version_needed = "3.9.6"

# Some of these tmp files are created with sudo privileges
# (this should be fixed) meanwhile, we need sudo privileges to remove them
@misc.raise_privileges
def remove_temp_files():
    """ Remove Cnchi temporary files """
    temp_files = [".setup-running", ".km-running", "setup-pacman-running", \
        "setup-mkinitcpio-running", ".tz-running", ".setup", "Cnchi.log" ]
    for temp in temp_files:
        path = os.path.join("/tmp", temp)
        if os.path.exists(path):
            os.remove(path)

class Main(Gtk.Window):
    """ Cnchi main window """
    def __init__(self):
        ## This allows to translate all py texts (not the glade ones)
        #gettext.textdomain(APP_NAME)
        #gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
        #
        #locale_code, encoding = locale.getdefaultlocale()
        #lang = gettext.translation(APP_NAME, LOCALE_DIR, [locale_code], None, True)
        #lang.install()
        #
        ## With this we can use _("string") to translate
        #gettext.install(APP_NAME, localedir=LOCALE_DIR, codeset=None, names=[locale_code])

        # Check if we have administrative privileges
        if os.getuid() != 0:
            show.error(_('This installer must be run with administrative'
                         ' privileges, and cannot continue without them.'))
            sys.exit(1)

        setup_logging()

        # Check if we're already running
        tmp_running = "/tmp/.setup-running"
        if os.path.exists(tmp_running):
            show.error(_('You cannot run two instances of this installer.\n\n'
                          'If you are sure that the installer is not already running\n'
                          'you can manually delete the file %s\n'
                          'and run this installer again.') % tmp_running)
            sys.exit(1)

        super().__init__()

        logging.info(_("Cnchi installer version %s"), info.CNCHI_VERSION)

        current_process = multiprocessing.current_process()
        logging.debug("[%d] %s started", current_process.pid, current_process.name)

        self.settings = config.Settings()
        self.ui_dir = self.settings.get('ui')

        if not os.path.exists(self.ui_dir):
            cnchi_dir = os.path.join(os.path.dirname(__file__), './')
            self.settings.set('cnchi', cnchi_dir)

            ui_dir = os.path.join(os.path.dirname(__file__), 'ui/')
            self.settings.set('ui', ui_dir)

            data_dir = os.path.join(os.path.dirname(__file__), 'data/')
            self.settings.set('data', data_dir)

            self.ui_dir = self.settings.get('ui')

        if cmd_line.cache:
            self.settings.set('cache', cmd_line.cache)

        if cmd_line.copycache:
            self.settings.set('cache', cmd_line.copycache)
            self.settings.set('copy_cache', True)

        # For things we are not ready for users to test
        self.settings.set('z_hidden', cmd_line.z_hidden)

        # Set enabled desktops
        if self.settings.get('z_hidden'):
            self.settings.set("desktops", desktops.DESKTOPS_DEV)
        else:
            self.settings.set("desktops", desktops.DESKTOPS)

        self.ui = Gtk.Builder()
        self.ui.add_from_file(self.ui_dir + "cnchi.ui")

        self.add(self.ui.get_object("main"))

        self.header = self.ui.get_object("header")

        self.logo = self.ui.get_object("logo")
        data_dir = self.settings.get('data')
        logo_dir = os.path.join(data_dir, "antergos-logo-mini2.png")
        self.logo.set_from_file(logo_dir)

        # To honor our css
        self.header.set_name("header")
        self.logo.set_name("logo")

        self.main_box = self.ui.get_object("main_box")
        self.progressbar = self.ui.get_object("progressbar1")
        self.progressbar.set_name('process_progressbar')

        self.forward_button = self.ui.get_object("forward_button")
        self.backwards_button = self.ui.get_object("backwards_button")

        image1 = Gtk.Image()
        image1.set_from_icon_name("go-next", Gtk.IconSize.BUTTON)
        self.forward_button.set_label("")
        self.forward_button.set_image(image1)

        image2 = Gtk.Image()
        image2.set_from_icon_name("go-previous", Gtk.IconSize.BUTTON)
        self.backwards_button.set_label("")
        self.backwards_button.set_image(image2)

        # Create a queue. Will be used to report pacman messages (pac.py)
        # to the main thread (installer_*.py)
        self.callback_queue = multiprocessing.JoinableQueue()

        # Save in config if we have to use aria2 to download pacman packages
        self.settings.set("use_aria2", cmd_line.aria2)
        if cmd_line.aria2:
            logging.info(_("Using Aria2 to download packages - EXPERIMENTAL"))

        # Load all pages
        # (each one is a screen, a step in the install process)

        params = dict()
        params['header'] = self.header
        params['ui_dir'] = self.ui_dir
        params['forward_button'] = self.forward_button
        params['backwards_button'] = self.backwards_button
        params['callback_queue'] = self.callback_queue
        params['settings'] = self.settings
        params['main_progressbar'] = self.ui.get_object('progressbar1')
        
        if cmd_line.packagelist:
            params['alternate_package_list'] = cmd_line.packagelist
            logging.info("Using '%s' file as package list", params['alternate_package_list'])
        else:
            params['alternate_package_list'] = ""
            
        params['disable_tryit'] = cmd_line.disable_tryit
        params['testing'] = cmd_line.testing
        
        self.pages = dict()
        self.pages["welcome"] = welcome.Welcome(params)
        self.pages["language"] = language.Language(params)
        self.pages["location"] = location.Location(params)
        self.pages["check"] = check.Check(params)
        self.pages["desktop"] = desktop.DesktopAsk(params)
        self.pages["features"] = features.Features(params)
        self.pages["keymap"] = keymap.Keymap(params)
        self.pages["timezone"] = timezone.Timezone(params)
        self.pages["installation_ask"] = installation_ask.InstallationAsk(params)
        self.pages["installation_automatic"] = installation_automatic.InstallationAutomatic(params)
        self.pages["installation_alongside"] = installation_alongside.InstallationAlongside(params)
        self.pages["installation_advanced"] = installation_advanced.InstallationAdvanced(params)
        self.pages["user_info"] = user_info.UserInfo(params)
        self.pages["slides"] = slides.Slides(params)

        self.connect('delete-event', self.on_exit_button_clicked)
        self.ui.connect_signals(self)

        self.set_title(_('Cnchi - Antergos Installer'))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.set_size_request(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        # Set window icon
        icon_dir = os.path.join(data_dir, 'antergos-icon.png')

        self.set_icon_from_file(icon_dir)

        # Set the first page to show
        self.current_page = self.pages["welcome"]

        self.main_box.add(self.current_page)

        # Header style testing

        style_provider = Gtk.CssProvider()

        style_css = os.path.join(data_dir, "css", "gtk-style.css")

        with open(style_css, 'rb') as css:
            css_data = css.read()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Show main window
        self.show_all()

        self.header.set_title("Cnchi v%s" % info.CNCHI_VERSION)
        self.header.set_subtitle(_("Antergos Installer"))
        self.header.set_show_close_button(True)

        self.current_page.prepare('forwards')

        # Hide backwards button
        self.backwards_button.hide()

        # Hide titlebar but show border decoration
        self.get_window().set_accept_focus(True)
        self.get_window().set_decorations(Gdk.WMDecoration.BORDER)

        # Hide progress bar as it's value is zero
        self.progressbar.set_fraction(0)
        self.progressbar.hide()
        self.progressbar_step = 1.0 / (len(self.pages) - 2)

        with open(tmp_running, "w") as tmp_file:
            tmp_file.write("Cnchi %d\n" % 1234)

        GLib.timeout_add(1000, self.pages["slides"].manage_events_from_cb_queue)

    def on_exit_button_clicked(self, widget, data=None):
        """ Quit Cnchi """
        remove_temp_files()
        logging.info(_("Quiting installer..."))
        while Gtk.events_pending():
            Gtk.main_iteration()
        logging.shutdown()
        Gtk.main_quit()

    def set_progressbar_step(self, add_value):
        new_value = self.progressbar.get_fraction() + add_value
        if new_value > 1:
            new_value = 1
        if new_value < 0:
            new_value = 0
        self.progressbar.set_fraction(new_value)
        if new_value > 0:
            self.progressbar.show()
        else:
            self.progressbar.hide()

    def on_forward_button_clicked(self, widget, data=None):
        """ Show next screen """
        next_page = self.current_page.get_next_page()

        if next_page != None:
            stored = self.current_page.store_values()

            if stored != False:
                self.set_progressbar_step(self.progressbar_step)
                self.main_box.remove(self.current_page)

                self.current_page = self.pages[next_page]

                if self.current_page != None:
                    self.current_page.prepare('forwards')
                    self.main_box.add(self.current_page)

                    if self.current_page.get_prev_page() != None:
                        # There is a previous page, show button
                        self.backwards_button.show()
                        self.backwards_button.set_sensitive(True)
                    else:
                        self.backwards_button.hide()

    def on_backwards_button_clicked(self, widget, data=None):
        """ Show previous screen """
        prev_page = self.current_page.get_prev_page()

        if prev_page != None:
            self.set_progressbar_step(-self.progressbar_step)

            # If we go backwards, don't store user changes
            # self.current_page.store_values()

            self.main_box.remove(self.current_page)
            self.current_page = self.pages[prev_page]

            if self.current_page != None:
                self.current_page.prepare('backwards')
                self.main_box.add(self.current_page)

                if self.current_page.get_prev_page() == None:
                    # We're at the first page
                    self.backwards_button.hide()

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
    major_needed = int(_gtk_version_needed.split(".")[0])
    minor_needed = int(_gtk_version_needed.split(".")[1])
    micro_needed = int(_gtk_version_needed.split(".")[2])

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
    Gtk.main() or Gio/Gtk.Application.run()."""
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
        # Start Gdk stuff and main window app
        GObject.threads_init()
    
    #Gdk.threads_init()

def init_cnchi():
    """ This function initialises Cnchi """

    # Check for hwinfo
    # (this check is just for developers, in our liveCD hwinfo will always be installed)
    if not os.path.exists("/usr/bin/hwinfo"):
        print(_("Please install hwinfo before running this installer"))
        #sys.exit(1)

    if not check_gtk_version():
        sys.exit(1)

    # Command line options
    global cmd_line
    cmd_line = parse_options()

    #setup_logging()

    if cmd_line.update is not None:
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
    
    # Drop root privileges
    misc.drop_privileges()
    
    # Init PyObject Threads
    threads_init()
    
    # Create Gtk Application    
    myapp = Main()
    Gtk.main()

if __name__ == '__main__':
    init_cnchi()
