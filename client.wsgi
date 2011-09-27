from ConfigParser import RawConfigParser
import sys

from auslib.client.base import app as application
from auslib.client.base import AUS

CONFIG_FILE = 'config.ini'

cfg = RawConfigParser()
cfg.read(CONFIG_FILE)

try:
    dburi = cfg.get('database', 'dburi')
    AUS.setDb(dburi)
except:
    print >> sys.stderr, "Can't find dburi in %s" % CONFIG_FILE
    raise
