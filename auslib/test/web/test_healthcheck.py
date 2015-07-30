import mock
import unittest

from auslib.global_state import dbo
from auslib.web.base import app
from auslib.web.views.client import ClientRequestView


class HealthCheckTest(unittest.TestCase):
    """Most of the tests are run without the error handler because it gives more
       useful output when things break. However, we still need to test that our
       error handlers works!"""
    def setUp(self):
        app.config['DEBUG'] = True
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        self.client = app.test_client()
        self.view = ClientRequestView()

    def testHealthCheckNormal(self):
        ret = self.client.get("/healthcheck")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.data, "All is well.")

    @mock.patch("auslib.web.views.healthcheck.HealthCheckView.get")
    def testHealthCheckReturns500(self, healthcheck):
        class MyException(Exception):
            pass
        healthcheck.side_effect = MyException("KABOOM!")
        with self.assertRaises(MyException):
            self.client.get("/healthcheck")
