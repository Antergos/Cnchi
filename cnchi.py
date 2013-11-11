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

from gi.repository import Gtk, Gdk, GObject, GLib
import os
import sys
import getopt
import gettext
import locale
import multiprocessing
import logging

# Insert the src directory at the front of the path.
base_dir = os.path.dirname(__file__) or '.'
src_dir = os.path.join(base_dir, 'src')
sys.path.insert(0, src_dir)

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
import misc
import info
import updater
import show_message as show

# Enabled desktops (remember to update features_by_desktop in features.py if this is changed)
#_desktops = [ "nox", "gnome", "cinnamon", "xfce", "razor", "openbox", "lxde", "enlightenment", "kde" ]
_desktops = [ "nox", "gnome", "cinnamon", "xfce", "razor", "openbox", "kde" ]

# Command line options
_alternate_package_list = ""
_cache_dir = ""
_debug = False
_force_grub_type = False
_force_update = False
_log_level = logging.INFO
_update = False
_use_aria2 = False
_verbose = False
_disable_tryit = False

# Useful vars for gettext (translations)
APP_NAME = "cnchi"
LOCALE_DIR = "/usr/share/locale"

_main_window_width = 800
_main_window_height = 500

# At least this GTK version is needed
_gtk_version_needed = "3.9.6"

class Main(Gtk.Window):

    def __init__(self):
        # This allows to translate all py texts (not the glade ones)
        gettext.textdomain(APP_NAME)
        gettext.bindtextdomain(APP_NAME, LOCALE_DIR)

        locale_code, encoding = locale.getdefaultlocale()
        lang = gettext.translation(APP_NAME, LOCALE_DIR, [locale_code], None, True)
        lang.install()

        # With this we can use _("string") to translate
        gettext.install(APP_NAME, localedir=LOCALE_DIR, codeset=None, names=[locale_code])

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
        
        logging.info("Cnchi installer version %s" % info.cnchi_VERSION)
        
        p = multiprocessing.current_process()
        logging.debug("[%d] %s started" % (p.pid, p.name))
        
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
        self.settings.set("desktops", _desktops)
        
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
        
        # TODO: There's no exit button. We should add an Install button and hide it.
        self.exit_button = None
        
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
        params['exit_button'] = self.exit_button
        params['callback_queue'] = self.callback_queue
        params['settings'] = self.settings
        params['main_progressbar'] = self.ui.get_object('progressbar1')
        params['alternate_package_list'] = _alternate_package_list
        params['disable_tryit'] = _disable_tryit
        
        if len(_alternate_package_list) > 0:
            logging.info(_("Using '%s' file as package list") % _alternate_package_list)
        
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
        self.set_size_request(_main_window_width, _main_window_height);

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

        # We drop privileges, but where we should do it? before this? ¿?
        misc.drop_privileges()

        with open(tmp_running, "wt") as tmp_file:
            tmp_file.write("Cnchi %d\n" % 1234)

        GLib.timeout_add(1000, self.pages["slides"].manage_events_from_cb_queue)

    # TODO: some of these tmp files are created with sudo privileges
    # (this should be fixed) meanwhile, we need sudo privileges to remove them
    @misc.raise_privileges
    def remove_temp_files(self):
        tmp_files = [".setup-running", ".km-running", "setup-pacman-running", \
                "setup-mkinitcpio-running", ".tz-running", ".setup", "Cnchi.log" ]
        for t in tmp_files:
            p = os.path.join("/tmp", t)
            if os.path.exists(p):
                os.remove(p)
         
    def on_exit_button_clicked(self, widget, data=None):
        self.remove_temp_files()
        logging.info(_("Quiting installer..."))
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
    logger = logging.getLogger()
    logger.setLevel(_log_level)
    # Log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Create file handler
    fh = logging.FileHandler('/tmp/cnchi.log', mode='w')
    fh.setLevel(_log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if _verbose:
        # Show log messages to stdout
        sh = logging.StreamHandler()
        sh.setLevel(_log_level)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        

def show_help():
    print("Cnchi Antergos Installer")
    print("Advanced options:")
    print("-a, --aria2 : Use aria2 to download Antergos packages (EXPERIMENTAL)")
    print("-c, --cache : Use pre-downloaded xz packages (Cnchi will download them anyway if a new version is found)")
    print("-d, --debug : Set debug log level")
    print("-g type, --force-grub-type type : force grub type to install, type can be bios, efi, ask or none")
    print("-h, --help : Show this help message")
    print("-p file.xml, --packages file.xml : Antergos will install the packages referenced by file.xml instead of the default ones")
    print("-v, --verbose : Show logging messages to stdout")

def check_gtk_version():
    # Check desired GTK Version
    major_needed = int(_gtk_version_needed.split(".")[0])
    minor_needed = int(_gtk_version_needed.split(".")[1])
    micro_needed = int(_gtk_version_needed.split(".")[2])
    
    # Check system GTK Version
    major = Gtk.get_major_version()
    minor = Gtk.get_minor_version()
    micro = Gtk.get_micro_version()

    if major_needed > major or (major_needed == major and minor_needed > minor) or \
      (major_needed == major and minor_needed == minor and micro_needed > micro):
        print("Detected GTK %d.%d.%d but %s is needed. Can't run this installer." % (major, minor, micro, _gtk_version_needed))
        return False
    else:
        print("Using GTK v%d.%d.%d" % (major, minor, micro))
    
    return True

if __name__ == '__main__':
    
    # Check for hwinfo
    if not os.path.exists("/usr/bin/hwinfo"):
        print("Please install hwinfo before running this installer")
        sys.exit(1)

    if not check_gtk_version():
        sys.exit(1)

    # Check program args
    argv = sys.argv[1:]
    
    try:
        opts, args = getopt.getopt(argv, "ac:dp:ufvg:h",
         ["aria2", "cache=", "debug", "packages=", "update",
          "force-update", "verbose", "force-grub=", "disable-tryit", "help"])
    except getopt.GetoptError as e:
        show_help()
        print(str(e))
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-d', '--debug'):
            _log_level = logging.DEBUG
        elif opt in ('-v', '--verbose'):
            _verbose = True
        elif opt in ('-u', '--update'):
            _update = True
        elif opt in ('-f', '--force-update'):
            _force_update = True
            _update = True
        elif opt in ('-p', '--packages'):
            _alternate_package_list = arg
        elif opt in ('-a', '--aria2'):
            _use_aria2 = True
        elif opt in ('-c', '--cache'):
            _cache_dir = arg
        elif opt in ('-g', '--force-grub-type'):
            if arg in ('bios', 'efi', 'ask', 'none'):
                _force_grub_type = arg
        elif opt in ('--disable-tryit'):
            _disable_tryit = True
        elif opt in ('-h', '--help'):
            show_help()
            sys.exit(0)
        else:
            assert False, "unhandled option"
        
    if _update:
        setup_logging()
        # Check if program needs to be updated
        upd = updater.Updater(_force_update)
        if upd.update():
            # Remove /tmp/.setup-running to be able to run another
            # instance of Cnchi
            p = "/tmp/.setup-running"
            if os.path.exists(p):
                os.remove(p)
            if not _force_update:
                print("Program updated! Restarting...")
                # Run another instance of Cnchi (which will be the new version)
                os.execl(sys.executable, *([sys.executable] + sys.argv))
            else:
                print("Program updated! Please restart Cnchi.")

            # Exit and let the new instance do all the hard work
            sys.exit(0)

    # Start Gdk stuff and main window app 
    GObject.threads_init()

    app = Main()

    Gtk.main()
