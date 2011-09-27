from ConfigParser import RawConfigParser
import logging
from os import path
import sys


CONFIG_FILE = '/var/www/aus/config.ini'

cfg = RawConfigParser()
cfg.read(CONFIG_FILE)

logging.basicConfig(filename=cfg.get('logging', 'logfile'))

activate_this = path.join(cfg.get('paths', 'virtualenv'), 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from auslib.client.base import app as application
from auslib.client.base import AUS

dburi = cfg.get('database', 'dburi')
AUS.setDb(dburi)
