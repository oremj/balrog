from flask import Response
from flaskext.wtf import Form

from auslib.web.base import app
from auslib.web.views.base import AdminView

import logging
log = logging.getLogger(__name__)

__all__ = ["CSRFView"]

def get_csrf_headers():
    # Instantiating a Form makes sure there's a CSRF token available
    # and puts an hmac key in the session.
    form = Form()
    return {'X-CSRF-Token': form.csrf_token._value()}

class CSRFView(AdminView):
    """/csrf"""
    def get(self):
        return Response(headers=get_csrf_headers())

app.add_url_rule('/csrf_token', view_func=CSRFView.as_view('csrf'))
