import mock
import simplejson as json

from auslib.test.web.views.base import ViewTest, JSONTestMixin

class TestCSRFEndpoint(ViewTest, JSONTestMixin):
    def testCsrfGet(self):
        with mock.patch('flaskext.wtf._generate_csrf_token') as g:
            g.return_value = 111
            ret = self._get('/csrf')
            self.assertEquals(ret.status_code, 200)
            self.assertEquals(json.loads(ret.data), dict(csrf_token=111))
