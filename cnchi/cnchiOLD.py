#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cnchi.py
#
#  Copyright © 2013-2016 Antergos
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

""" Cnchi Installer """

from _initial_imports import *

# Useful vars for gettext (translations)
APP_NAME = 'cnchi'
LOCALE_DIR = '/usr/share/locale'

# At least this GTK version is needed
GTK_VERSION_NEEDED = "3.22.0"

FLAGS = Gio.ApplicationFlags.FLAGS_NONE


class CnchiApp(CnchiObject):
    """ Cnchi Installer """

    TMP_PID_FILE = '/tmp/cnchi.pid'

    def __init__(self, cmd_line=None, name='cnchi_app', logger=None, *args, **kwargs):

        super().__init__(name=name, logger=logger, *args, **kwargs)

        self.widget = Gtk.Application(application_id='com.antergos.cnchi', flags=FLAGS)

        self.widget.connect('activate', self.activate_cb)

        # Command line options
        self.cmd_line = cmd_line
        self.settings.cmd_line = cmd_line

    def _enumerate_settings(self, obj, address=''):
        excluded = ['_lock', '_initialized']

        for attr in dir(obj):
            if attr in excluded or (attr.startswith('__') and attr.endswith('__')):
                continue

            value = getattr(obj, attr)

            if '' != address:
                _address = '{}.{}'.format(address, attr)
            else:
                _address = attr

            if 'DataObject' == value.__class__.__name__:
                self._enumerate_settings(value, _address)
                continue

            self.logger.debug('%s: %s', _address, value)

    def _initialize_settings(self):
        loader = ConfigLoader(self.logger)
        loader.load_config()

        for key, value in loader.config.items():
            setattr(self.settings, key, value)

        self._enumerate_settings(self.settings)

    def _maybe_clear_webkit_data(self):
        _dirs = [self.WK_CACHE_DIR, self.WK_DATA_DIR]

        for _dir in _dirs:
            if os.path.exists(_dir) and 'development' == info.CNCHI_RELEASE_STAGE:
                shutil.rmtree(_dir)

            os.makedirs(_dir, 0o777, exist_ok=True)

    def _pre_activation_checks(self):
        can_activate = True

        # Make sure we have administrative privileges
        if os.getuid() != 0 and not self.cmd_line.z_hidden:
            can_activate = False
            msg = _('This installer must be run with administrative privileges, '
                    'and cannot continue without them.')
            show.error(None, msg)

        # Make sure we're not already running
        if self.already_running():
            can_activate = False
            msg = _("You cannot run two instances of this installer.\n\n"
                    "If you are sure that the installer is not already running\n"
                    "you can run this installer using the --force option\n"
                    "or you can manually delete the offending file.\n\n"
                    "Offending file: '{0}'").format(self.TMP_PID_FILE)
            show.error(None, msg)

        return can_activate

    def activate_cb(self, app):
        if not self._pre_activation_checks():
            return

        # self._maybe_clear_webkit_data()
        self._initialize_settings()

        with open('/tmp/cnchi.pid', "w") as tmp_file:
            tmp_file.write(str(os.getpid()))

        CnchiUI()

        self._main_window.widget.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.widget.add_window(self._main_window.widget)
        self._main_window.widget.show_all()

    def already_running(self):
        """ Check to see if we're already running """
        if os.path.exists(self.TMP_PID_FILE):
            logging.debug("File %s already exists.", self.TMP_PID_FILE)
            with open(self.TMP_PID_FILE) as setup:
                line = setup.readline()
            try:
                pid = int(line.strip('\n'))
            except ValueError as err:
                logging.debug(err)
                logging.debug("Cannot read PID value.")
                return True

            if misc.check_pid(pid):
                logging.info("Cnchi with pid '%d' already running.", pid)
                return True
            else:
                # Cnchi with pid 'pid' is no longer running, we can safely
                # remove the offending file and continue.
                os.remove(self.TMP_PID_FILE)
        return False


def setup_logging(cmd_line):
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
    log_format = "%(asctime)s [%(levelname)s] %(filename)s(%(lineno)d) %(funcName)s(): %(message)s"
    formatter = logging.Formatter(
        fmt=log_format,
        datefmt="%Y-%m-%d %H:%M:%S")

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

    if cmd_line.log_server:
        log_server = cmd_line.log_server

        if log_server == 'bugsnag':
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
                    bugsnag.before_notify(context_filter.bugsnag_before_notify_callback)
                    logger.addHandler(bugsnag_handler)
                    logging.info(
                        "Sending Cnchi log messages to bugsnag server (using python-bugsnag).")
                else:
                    logging.warning(
                        "Cannot read the bugsnag api key, logging to bugsnag is not possible.")
            else:
                logging.warning(BUGSNAG_ERROR)
        else:
            # Socket logger
            socket_handler = logging.handlers.SocketHandler(
                log_server,
                logging.handlers.DEFAULT_TCP_LOGGING_PORT)
            socket_formatter = logging.Formatter(formatter)
            socket_handler.setFormatter(socket_formatter)
            logger.addHandler(socket_handler)

            # Also add uuid filter to requests logs
            logger_requests = logging.getLogger("requests.packages.urllib3.connectionpool")
            logger_requests.addFilter(context_filter.filter)

            uid = str(uuid.uuid1()).split("-")
            myuid = uid[3] + "-" + uid[1] + "-" + uid[2] + "-" + uid[4]
            logging.info("Sending Cnchi logs to {0} with id '{1}'".format(log_server, myuid))

    return logger


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
            import show_message as show
            show.error(None, text)
        except ImportError as import_error:
            logging.error(import_error)
        finally:
            return False
    else:
        logging.info("Using GTK v{0}.{1}.{2}".format(major, minor, micro))

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
            import show_message as show
            show.error(None, err)
        except ImportError as import_error:
            logging.error(import_error)
        finally:
            logging.error(err)
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
            shutil.rmtree(cache_dir)
    else:
        logging.debug("Not running from ISO")
        return False

    return True


def parse_options():
    """ argparse http://docs.python.org/3/howto/argparse.html """

    desc = _("Cnchi v{0} - Antergos Installer").format(info.CNCHI_VERSION)
    parser = argparse.ArgumentParser(description=desc)

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
        help=_("Install the packages referenced by a local xml instead of the default ones"),
        nargs='?')
    parser.add_argument(
        "-r", "--resolution",
        help=_("Specify Cnchi screen with and height (useful for low res screens) (format is widthxheight)"),
        nargs='?')
    parser.add_argument(
        "-s", "--log-server",
        help=_("Choose to which log server send Cnchi logs. Expects a hostname or an IP address"),
        nargs='?')
    parser.add_argument(
        "-u", "--update",
        help=_("Upgrade/downgrade Cnchi to the web version"),
        action="store_true")
    parser.add_argument(
        "--disable-update",
        help=_("Do not search for new Cnchi versions online"),
        action="store_true")
    parser.add_argument(
        "--disable-rank-mirrors",
        help=_("Do not try to rank Arch and Antergos mirrors during installation"),
        action="store_true")
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


def setup_gettext():
    """ This allows to translate all py texts (not the glade ones) """

    gettext.textdomain(APP_NAME)
    gettext.bindtextdomain(APP_NAME, LOCALE_DIR)

    locale_code, encoding = locale.getdefaultlocale()
    lang = gettext.translation(APP_NAME, LOCALE_DIR, [locale_code], None, True)
    lang.install()


def check_for_files():
    """ Check for some necessary files. Cnchi can't run without them """

    return  True

    paths = [
        "/usr/share/cnchi",
        "/usr/share/cnchi/cnchi/ui/tpl",
        "/usr/share/cnchi/data",
        "/usr/share/cnchi/data/locale"]

    for path in paths:
        if not os.path.exists(path):
            print(path)
            print(_("Cnchi files not found. Please, install Cnchi using pacman"))
            return False

    return True


def init_cnchi():
    """ This function prepares for Cnchi's initialization """

    # Configures gettext to be able to translate messages, using _()
    setup_gettext()

    # Command line options
    cmd_line = parse_options()

    if cmd_line.version:
        print(_("Cnchi (Antergos Installer) version {0}").format(info.CNCHI_VERSION))
        sys.exit(0)

    if cmd_line.force:
        misc.remove_temp_files()

    # Drop root privileges
    misc.drop_privileges()

    # Setup our logging framework
    logger = setup_logging(cmd_line)

    # Check Cnchi is correctly installed
    if not check_for_files():
        sys.exit(1)

    # Check installed GTK version
    if not check_gtk_version():
        sys.exit(1)

    # Check installed pyalpm and libalpm versions
    #if not check_pyalpm_version():
    #    sys.exit(1)

    # Check ISO version where Cnchi is running from
    # if not do_iso_check():
    #    sys.exit(1)

    # if not cmd_line.disable_update:
        # update_cnchi(cmd_line)

    # Init PyObject Threads
    # threads_init()
    return cmd_line, logger


if __name__ == '__main__':
    cmd_line, logger = init_cnchi()
    # Create Gtk Application
    app = CnchiApp(cmd_line=cmd_line, logger=logger)
    exit_status = app.widget.run(None)
    sys.exit(exit_status)
