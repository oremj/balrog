from flask import Response
from flask_wtf import Form

from auslib.admin.views.base import AdminView

__all__ = ["CSRFView"]


def get_csrf_headers():
    # Instantiating a Form makes sure there's a CSRF token available
    # and puts an hmac key in the session.
    form = Form()
    return {'X-CSRF-Token': form.csrf_token._value()}


def get_csrf_headers2():
    return Response(headers=get_csrf_headers())


class CSRFView(AdminView):
    """/csrf_token"""

    def get(self):
        return Response(headers=get_csrf_headers())
