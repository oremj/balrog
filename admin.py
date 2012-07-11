import logging
from os import path
import site

from flask import Response, render_template
from flask.views import MethodView

from paste.auth.basic import AuthBasicHandler

mydir = path.dirname(path.abspath(__file__))
site.addsitedir(mydir)
site.addsitedir(path.join(mydir, 'vendor/lib/python'))

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
    parser.add_option("--auth", dest="auth", default="bob:bob")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
        help="Verbose output")
    options, args = parser.parse_args()
    username, password = options.auth.split(':')

    from auslib import log_format
    from auslib.admin.base import app, db

    app.config['SECRET_KEY'] = 'abc123'
    app.config['DEBUG'] = True

    class TestsView(MethodView):
        """/tests.html"""
        def get(self):
            return render_template("tests.html")

    class ResetView(MethodView):
        """/reset"""
        def get(self):
            db.permissions.t.delete().execute()
            db.releases.t.delete().execute()
            db.rules.t.delete().execute()
            db.permissions.t.insert().execute(username=username, permission='admin', data_version=1)
            return Response(status=200)

    app.add_url_rule('/tests.html', view_func=TestsView.as_view('tests'))
    app.add_url_rule('/reset', view_func=ResetView.as_view('reset'))

    log_level = logging.INFO
    if options.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format=log_format)

    db.setDburi(options.db)
    db.createTables()

    def auth(environ, u, p):
        return u == username and p == password
    app.wsgi_app = AuthBasicHandler(app.wsgi_app, "Balrog standalone auth", auth)
    app.run(port=options.port, host=options.host)
