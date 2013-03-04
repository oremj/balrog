import logging
from os import path
import site

from paste.auth.basic import AuthBasicHandler

mydir = path.dirname(path.abspath(__file__))
site.addsitedir(mydir)
site.addsitedir(path.join(mydir, 'vendor/lib/python'))

from raven.contrib.flask import Sentry
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_defaults(
        db='sqlite:///update.db',
        port=9000,
    )

    parser.add_option("-d", "--db", dest="db", help="database to use, relative to inputdir")
    parser.add_option("-p", "--port", dest="port", type="int", help="port for server")
    parser.add_option("--host", dest="host", default='127.0.0.1', help="host to listen on. for example, 0.0.0.0 binds on all interfaces.")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
        help="Verbose output")
    options, args = parser.parse_args()

    from auslib import log_format
    from auslib.admin.base import app, db
    from migrate.exceptions import DatabaseAlreadyControlledError

    log_level = logging.INFO
    if options.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format=log_format)

    db.setDburi(options.db)
    try:
        db.create()
    except DatabaseAlreadyControlledError:
        pass

    app.config['SECRET_KEY'] = 'abc123'
    app.config['DEBUG'] = True
    app.config['SENTRY_PROCESSORS'] = ['auslib.util.sentry.SanitizeHeadersProcessor']
    app.config['SENTRY_DSN'] = 'https://c980e68b8a0c456583a165d570770e51:8ce74a0adbb0461694b925a271bc2532@errormill.mozilla.org/12'

    if app.config['SENTRY_DSN']:
        sentry = Sentry(app)
    def auth(environ, username, password):
        return username == password
    app.wsgi_app = AuthBasicHandler(app.wsgi_app, "Balrog standalone auth", auth)
    app.run(port=options.port, host=options.host)
