import unittest

from auslib.blobs.apprelease import ReleaseBlobBase, ReleaseBlobV1, ReleaseBlobV2

class SimpleBlob(ReleaseBlobBase):
    format_ = {'foo': None}


class TestReleaseBlobBase(unittest.TestCase):
    def testGetResolvedPlatform(self):
        blob = SimpleBlob(platforms=dict(a=dict(), b=dict(alias='a')))
        self.assertEquals('a', blob.getResolvedPlatform('a'))
        self.assertEquals('a', blob.getResolvedPlatform('b'))

    def testGetPlatformData(self):
        blob = SimpleBlob(platforms=dict(a=dict(foo=1)))
        self.assertEquals(blob.getPlatformData('a'), dict(foo=1))

    def testGetLocaleOrTopLevelParamTopLevelOnly(self):
        blob = SimpleBlob(foo=5)
        self.assertEquals(5, blob.getLocaleOrTopLevelParam('a', 'b', 'foo'))

    def testGetLocaleOrTopLevelParamLocaleOnly(self):
        blob = SimpleBlob(platforms=dict(f=dict(locales=dict(g=dict(foo=6)))))
        self.assertEquals(6, blob.getLocaleOrTopLevelParam('f', 'g', 'foo'))

    def testGetLocaleOrTopLevelParamMissing(self):
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(g=dict(foo=6)))))
        self.assertEquals(None, blob.getLocaleOrTopLevelParam('a', 'b', 'c'))

    def testGetBuildIDPlatformOnly(self):
        blob = SimpleBlob(platforms=dict(a=dict(buildID=1, locales=dict(b=dict()))))
        self.assertEquals(1, blob.getBuildID('a', 'b'))

    def testGetBuildIDLocaleOnly(self):
        blob = SimpleBlob(platforms=dict(c=dict(locales=dict(d=dict(buildID=9)))))
        self.assertEquals(9, blob.getBuildID('c', 'd'))

    def testGetBuildIDMissingLocale(self):
        blob = SimpleBlob(platforms=dict(c=dict(locales=dict(d=dict(buildID=9)))))
        self.assertRaises(KeyError, blob.getBuildID, 'c', 'a')

    def testGetBuildIDMissingLocaleBuildIDAtPlatform(self):
        blob = SimpleBlob(platforms=dict(c=dict(buildID=9, locales=dict(d=dict()))))
        self.assertRaises(KeyError, blob.getBuildID, 'c', 'a')
    # XXX: should we support the locale overriding the platform? this should probably be invalid


class TestReleaseBlobV1(unittest.TestCase):
    def testGetAppv(self):
        blob = ReleaseBlobV1(appv=1)
        self.assertEquals(1, blob.getAppv('p', 'l'))
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(g=dict(appv=2)))))
        self.assertEquals(2, blob.getAppv('f', 'g'))

    def testGetExtv(self):
        blob = ReleaseBlobV1(extv=3)
        self.assertEquals(3, blob.getExtv('p', 'l'))
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(g=dict(extv=4)))))
        self.assertEquals(4, blob.getExtv('f', 'g'))

    def testApplicationVersion(self):
        blob = ReleaseBlobV1(platforms=dict(f=dict(locales=dict(g=dict(extv=4)))))
        self.assertEquals(blob.getExtv('f', 'g'), blob.getApplicationVersion('f', 'g'))


class TestNewStyleVersionBlob(unittest.TestCase):
    def testGetAppVersion(self):
        blob = ReleaseBlobV2(appVersion=1)
        self.assertEquals(1, blob.getAppVersion('p', 'l'))
        blob = ReleaseBlobV2(platforms=dict(f=dict(locales=dict(g=dict(appVersion=2)))))
        self.assertEquals(2, blob.getAppVersion('f', 'g'))

    def testGetDisplayVersion(self):
        blob = ReleaseBlobV2(displayVersion=3)
        self.assertEquals(3, blob.getDisplayVersion('p', 'l'))
        blob = ReleaseBlobV2(platforms=dict(f=dict(locales=dict(g=dict(displayVersion=4)))))
        self.assertEquals(4, blob.getDisplayVersion('f', 'g'))

    def testGetPlatformVersion(self):
        blob = ReleaseBlobV2(platformVersion=5)
        self.assertEquals(5, blob.getPlatformVersion('p', 'l'))
        blob = ReleaseBlobV2(platforms=dict(f=dict(locales=dict(g=dict(platformVersion=6)))))
        self.assertEquals(6, blob.getPlatformVersion('f', 'g'))

    def testApplicationVersion(self):
        blob = ReleaseBlobV2(platforms=dict(f=dict(locales=dict(g=dict(appVersion=6)))))
        self.assertEquals(blob.getAppVersion('f', 'g'), blob.getApplicationVersion('f', 'g'))
