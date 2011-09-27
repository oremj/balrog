from ConfigParser import RawConfigParser
import sys

from auslib.client.base import app as application
from auslib.client.base import AUS

CONFIG_FILE = 'config.ini'

cfg = RawConfigParser()
cfg.read(CONFIG_FILE)

activate_this = path.join(cfg.get('paths', 'virtualenv'), 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

dburi = cfg.get('database', 'dburi')
AUS.setDb(dburi)
