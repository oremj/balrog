import simplejson as json
import unittest

from auslib.json import Blob, UnknownKeyError, ReleaseBlobSchema1

class SimpleBlob(Blob):
    validation_keys = dict(foo=None, bar=None)

class BlobWithChild(Blob):
    validation_keys = dict(baz=None, children=SimpleBlob)

class TestBlob(unittest.TestCase):
    def testBlob(self):
        expected = dict(foo='bar')
        sb = SimpleBlob()
        sb.loadJSON(json.dumps(expected))
        self.assertEquals(sb, expected)

    def testBlobWithChild(self):
        data = json.dumps(dict(baz='abc', children=dict(foo='foo')))
        bwc = BlobWithChild()
        bwc.loadJSON(data)
        self.assertEquals(bwc['baz'], 'abc')
        self.assertEquals(bwc['children'], dict(foo='foo'))

    def testRaisesOnBadJSON(self):
        sb = SimpleBlob()
        self.assertRaises(json.JSONDecodeError, sb.loadJSON, 'bad')

    def testInstanceVariables(self):
        sb = SimpleBlob()
        sb.loadDict(dict(foo='bar'))
        self.assertEqual(sb['foo'], 'bar')

    def testGetJSON(self):
        expected = json.dumps(dict(foo=123))
        sb = SimpleBlob()
        sb.loadJSON(expected)
        self.assertEquals(sb.getJSON(), expected)

nightly_blob = """
{
    "name": "somename",
    "platforms": {
        "someplatform": {
            "locales": {
                "en-US": {
                    "buildID": "9999",
                    "complete": {
                        "filesize": "1234"
                    }
                }
            }
        }
    }
}
"""

class TestRealBlob(unittest.TestCase):
    def testNightlyBlob(self):
        blob = ReleaseBlobSchema1()
        blob.loadJSON(nightly_blob)
        self.assertEquals(blob['name'], 'somename')
        self.assertEquals(blob['platforms']['someplatform']['locales']['en-US']['buildID'], '9999')
        self.assertEquals(blob['platforms']['someplatform']['locales']['en-US']['complete']['filesize'], '1234')
