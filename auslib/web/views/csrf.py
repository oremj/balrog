from flask import jsonify
from flaskext.wtf import Form

from auslib.web.base import app
from auslib.web.views.base import AdminView

import logging
log = logging.getLogger(__name__)

__all__ = ["CSRFView"]

class CSRFView(AdminView):
    """/csrf"""
    def get(self):
        form = Form()
        return jsonify(csrf_token=form.csrf_token._value())

app.add_url_rule('/csrf_token', view_func=CSRFView.as_view('csrf'))
