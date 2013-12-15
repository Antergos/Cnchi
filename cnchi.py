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
import installation_ask
import installation_automatic
import installation_alongside
import installation_advanced
import user_info
import slides
import canonical.misc as misc
import info
import updater
import show_message as show
import desktop_environments as desktops

# Command line options
_alternate_package_list = ""
_cache_dir = ""
_force_grub_type = False
_force_update = False
_log_level = logging.INFO
_update = False
_use_aria2 = False
_verbose = False
_disable_tryit = False
_testing = False

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
            show.fatal_error(_('This installer must be run with administrative'
                         ' privileges, and cannot continue without them.'))

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

        self.settings.set('cache', _cache_dir)

        # Set enabled desktops
        self.settings.set("desktops", desktops.DESKTOPS)

        # Set if a grub type must be installed (user choice)
        self.settings.set("force_grub_type", _force_grub_type)

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
        self.settings.set("use_aria2", _use_aria2)
        if _use_aria2:
            logging.info(_("Using Aria2 to download packages - EXPERIMENTAL"))

        # Load all pages
        # (each one is a screen, a step in the install process)

        self.pages = dict()

        params = dict()
        params['header'] = self.header
        params['ui_dir'] = self.ui_dir
        params['forward_button'] = self.forward_button
        params['backwards_button'] = self.backwards_button
        params['callback_queue'] = self.callback_queue
        params['settings'] = self.settings
        params['main_progressbar'] = self.ui.get_object('progressbar1')
        params['alternate_package_list'] = _alternate_package_list
        params['disable_tryit'] = _disable_tryit
        params['testing'] = _testing

        if len(_alternate_package_list) > 0:
            logging.info("Using '%s' file as package list", _alternate_package_list)

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

        #self.connect("delete-event", Gtk.main_quit)
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

        self.header.set_title("Cnchi")
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
    logger.setLevel(_log_level)
    # Log format
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s')
    # Create file handler
    file_handler = logging.FileHandler('/tmp/cnchi.log', mode='w')
    file_handler.setLevel(_log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if _verbose:
        # Show log messages to stdout
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(_log_level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)


def show_help():
    """ Show Cnchi command line options """
    print("Cnchi Antergos Installer")
    print("Advanced options:")
    print("-a, --aria2 : Use aria2 to download Antergos packages (EXPERIMENTAL)")
    print("-c, --cache : Use pre-downloaded xz packages (Cnchi will download them anyway if a new version is found)")
    print("-d, --debug : Set debug log level")
    print("-g type, --force-grub-type type : force grub type to install, type can be bios, efi, ask or none")
    print("-h, --help : Show this help message")
    print("-p file.xml, --packages file.xml : Install the packages referenced by file.xml instead of the default ones")
    print("-t, --testing : Do not perform any changes (useful for developers)")
    print("-v, --verbose : Show logging messages to stdout")

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

def init_cnchi():
    """ This function initialises Cnchi """

    # Command line options
    global _alternate_package_list
    global _cache_dir
    global _force_grub_type
    global _force_update
    global _log_level
    global _update
    global _use_aria2
    global _verbose
    global _disable_tryit
    global _testing

    # Check for hwinfo
    # (this check is just for developers, in our liveCD hwinfo will always be installed)
    if not os.path.exists("/usr/bin/hwinfo"):
        print("Please install hwinfo before running this installer")
        sys.exit(1)

    if not check_gtk_version():
        sys.exit(1)

    # Check program args
    arguments_vector = sys.argv[1:]

    try:
        options, arguments = getopt.getopt(arguments_vector, "ac:dp:ufvg:nht",
         ["aria2", "cache=", "debug", "packages=", "update",
          "force-update", "verbose", "force-grub=", "disable-tryit", "help", "testing"])
    except getopt.GetoptError as e:
        show_help()
        print(str(e))
        sys.exit(2)

    for option, argument in options:
        if option in ('-a', '--aria2'):
            _use_ari2 = True
        elif option in ('-c', '--cache'):
            _cache_dir = argument
        elif option in ('-d', '--debug'):
            _log_level = logging.DEBUG
        elif option in ('-f', '--force-update'):
            _force_update = True
            _update = True
        elif option in ('-g', '--force-grub-type'):
            if argument in ('bios', 'efi', 'ask', 'none'):
                _force_grub_type = argument
        elif option in ('-h', '--help'):
            show_help()
            sys.exit(0)
        elif option in ('-n', '--disable-tryit'):
            _disable_tryit = True
        elif option in ('-p', '--packages'):
            _alternate_package_list = argument
        elif option in ('-t', '--testing'):
            _testing = True
        elif option in ('-u', '--update'):
            _update = True
        elif option in ('-v', '--verbose'):
            _verbose = True
        else:
            assert False, "Unhandled option"

    if _update:
        setup_logging()
        # Check if program needs to be updated
        upd = updater.Updater(_force_update)
        if upd.update():
            remove_temp_files()
            if not _force_update:
                print("Program updated! Restarting...")
                # Run another instance of Cnchi (which will be the new version)
                os.execl(sys.executable, *([sys.executable] + sys.argv))
            else:
                print("Program updated! Please restart Cnchi.")

            # Exit and let the new instance do all the hard work
            sys.exit(0)

    # Drop root privileges
    misc.drop_privileges()

    # Start Gdk stuff and main window app
    GObject.threads_init()

    myapp = Main()

    Gtk.main()

if __name__ == '__main__':
    init_cnchi()
