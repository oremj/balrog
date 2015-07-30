from flask import make_response
from flask.views import MethodView

from auslib.global_state import dbo

import logging


class HealthCheckView(MethodView):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        MethodView.__init__(self, *args, **kwargs)

    def get(self):
        # Perform a database operation to make sure that connection is working fine.
        # This will bubble an Exception if something goes wrong. Otherwise, a normal
        # response will be returned.
        dbo.rules.countRules()
        return make_response("All is well.")
