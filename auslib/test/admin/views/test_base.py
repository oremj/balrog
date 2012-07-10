from auslib.test.admin.views.base import ViewTest

class TestRequirepermission(ViewTest):
    def testAdmin(self):
        ret = self._put('/users/foo/permissions/admin')
        self.assertStatusCode(ret, 201)

    def testGranular(self):
        ret = self._put('/users/foo/permissions/admin', username='bob')
        self.assertStatusCode(ret, 201)

class TestTestsView(ViewTest):
    # The TestsView shouldn't be enabled, except when running through admin.py
    def testTestsNotEnabled(self):
        ret = self.client.get('/tests.html')
        self.assertStatusCode(ret, 404)

    def testResetNotEnabled(self):
        ret = self.client.get('/tests.html')
        self.assertStatusCode(ret, 404)
