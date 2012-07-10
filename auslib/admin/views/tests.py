from flask import render_template, request, Response
from flask.views import MethodView

from auslib.admin.base import app, db

__all__ = ["TestsView"]

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
        return Response(status=200)

# Unlike other views, we add this route here so that it's only enabled when
# this module is included.
if app.config['DEBUG']:
    app.add_url_rule('/tests.html', view_func=TestsView.as_view('tests'))
    app.add_url_rule('/reset', view_func=ResetView.as_view('reset'))
