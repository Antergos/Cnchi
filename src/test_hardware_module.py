import logging

APP_NAME = "cnchi"
LOCALE_DIR = "/usr/share/locale"

import gettext
import locale
locale_code, encoding = locale.getdefaultlocale()
lang = gettext.translation(APP_NAME, LOCALE_DIR, [locale_code], None, True)
lang.install()

def setup_logging():
    """ Configure our logger """
    logger = logging.getLogger()
    
    log_level = logging.DEBUG
    
    logger.setLevel(log_level)
    
    # Log format
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s() - %(levelname)s: %(message)s')
    
    # Show log messages to stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

if __name__ == '__main__':
    setup_logging()

    # Get packages needed for detected hardware
    try:
        import hardware.hardware as hardware
        hardware_install = hardware.HardwareInstall()
        hardware_pkgs = hardware_install.get_packages()
        print("Hardware module added these packages : ", hardware_pkgs)
    except ImportError:
        print("Can't import hardware module.")
    except Exception as err:
        print("Unknown error in hardware module. Output: %s" % err)
