import os, sys
import logging
from mock import Mock

logging.basicConfig(level=10)
logger = logging.getLogger(__name__)

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)
sys.path.append(os.path.join(parentdir, 'src'))

logger.debug("parentdir: %s" % parentdir)

from installation_process import InstallationProcess

# set needed config options
settings = dict()
settings['data'] = os.path.join(parentdir, 'data')

# create mock object to test just one method and not the __init__
mobject = Mock(InstallationProcess)

mobject.settings = settings
mobject.dest_dir = '/tmp'
mobject.arch = 'x86_64'

mobject.write_file = InstallationProcess.write_file.__get__(mobject)

InstallationProcess.create_pacman_conf_file(mobject)

logger.debug('Done')

assert os.path.isfile('/tmp/pacman.conf')
