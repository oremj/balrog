import mock
import os
from tempfile import mkstemp
import unittest
from xml.dom import minidom

import auslib.log
from auslib import dbo
from auslib.web.base import app
from auslib.web.views.client import ClientRequestView

class ClientTest(unittest.TestCase):
    maxDiff = 2000

    @classmethod
    def setUpClass(cls):
        # Error handlers are removed in order to give us better debug messages
        cls.error_spec = app.error_handler_spec
        # Ripped from https://github.com/mitsuhiko/flask/blob/1f5927eee2288b4aaf508af5dc1f148aa2140d91/flask/app.py#L394
        app.error_handler_spec = {None: {}}

    @classmethod
    def tearDownClass(cls):
        app.error_handler_spec = cls.error_spec

    def setUp(self):
        self.cef_fd, self.cef_file = mkstemp()
        app.config['DEBUG'] = True
        app.config['SPECIAL_FORCE_HOSTS'] = ('http://a.com',)
        app.config['WHITELISTED_DOMAINS'] = ('a.com', 'boring.com')
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.setDomainWhitelist(('a.com', 'boring.com'))
        self.client = app.test_client()
        self.view = ClientRequestView()
        auslib.log.cef_config = auslib.log.get_cef_config(self.cef_file)
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='b', update_type='minor', product='b', data_version=1)
        dbo.releases.t.insert().execute(name='b', product='b', version='1.0', data_version=1, data="""
{
    "name": "b",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "2",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/z"
                    }
                }
            }
        }
    }
}
""")
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='c', update_type='minor', product='c',
                                     distribution='default', data_version=1)
        dbo.releases.t.insert().execute(name='c', product='c', version='10.0', data_version=1, data="""
{
    "name": "c",
    "schema_version": 1,
    "appv": "10.0",
    "extv": "10.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "11",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "12",
                        "from": "*",
                        "hashValue": "13",
                        "fileUrl": "http://a.com/y"
                    }
                }
            }
        }
    }
}
""")
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='d', update_type='minor', product='d', data_version=1)
        dbo.releases.t.insert().execute(name='d', product='d', version='20.0', data_version=1, data="""
{
    "name": "d",
    "schema_version": 1,
    "appv": "20.0",
    "extv": "20.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "21",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 22,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://evil.com/y"
                    }
                }
            }
        }
    }
}
""")

        dbo.rules.t.insert().execute(backgroundRate=100, mapping='e', update_type='minor', product='e', data_version=1)
        dbo.releases.t.insert().execute(name='e', product='e', version='22.0', data_version=1, data="""
{
    "name": "e",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "25",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 22,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://a.com/y"
                    }
                }
            }
        }
    }
}
""")

        dbo.rules.t.insert().execute(backgroundRate=100, mapping='f3', update_type='minor', product='f', data_version=1)
        dbo.releases.t.insert().execute(name='f1', product='f', version='22.0', data_version=1, data="""
{
    "name": "f1",
    "schema_version": 3,
    "platforms": {
        "p": {
            "buildID": "5",
            "locales": {
                "l": {}
            }
        }
    }
}
""")
        dbo.releases.t.insert().execute(name='f2', product='f', version='23.0', data_version=1, data="""
{
    "name": "f2",
    "schema_version": 3,
    "platforms": {
        "p": {
            "buildID": "6",
            "locales": {
                "l": {}
            }
        }
    }
}
""")
        dbo.releases.t.insert().execute(name='f3', product='f', version='25.0', data_version=1, data="""
{
    "name": "f3",
    "schema_version": 3,
    "hashFunction": "sha512",
    "appVersion": "25.0",
    "displayVersion": "25.0",
    "platformVersion": "25.0",
    "platforms": {
        "p": {
            "buildID": "29",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 2,
                            "from": "f1",
                            "hashValue": 3,
                            "fileUrl": "http://a.com/p1"
                        },
                        {
                            "filesize": 4,
                            "from": "f2",
                            "hashValue": 5,
                            "fileUrl": "http://a.com/p2"
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 29,
                            "from": "f2",
                            "hashValue": 6,
                            "fileUrl": "http://a.com/c1"
                        },
                        {
                            "filesize": 30,
                            "from": "*",
                            "hashValue": "31",
                            "fileUrl": "http://a.com/c2"
                        }
                    ]
                }
            }
        }
    }
}
""")
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='g2', update_type='minor', product='g', data_version=1)
        dbo.releases.t.insert().execute(name='g1', product='g', version='23.0', data_version=1, data="""
{
    "name": "g1",
    "schema_version": 3,
    "platforms": {
        "p": {
            "buildID": "8",
            "locales": {
                "l": {}
            }
        }
    }
}
""")
        dbo.releases.t.insert().execute(name='g2', product='g', version='26.0', data_version=1, data="""
{
    "name": "g2",
    "schema_version": 3,
    "hashFunction": "sha512",
    "appVersion": "26.0",
    "displayVersion": "26.0",
    "platformVersion": "26.0",
    "fileUrls": {
        "c1": "http://a.com/%FILENAME%",
        "c2": "http://a.com/%PRODUCT%"
    },
    "ftpFilenames": {
        "partials": {
            "g1": "g1-partial.mar"
        },
        "completes": {
            "*": "complete.mar"
        }
    },
    "bouncerProducts": {
        "partials": {
            "g1": "g1-partial"
        },
        "completes": {
            "*": "complete"
        }
    },
    "platforms": {
        "p": {
            "buildID": "40",
            "OS_FTP": "o",
            "OS_BOUNCER": "o",
            "locales": {
                "l": {
                    "partials": [
                        {
                            "filesize": 4,
                            "from": "g1",
                            "hashValue": 5
                        }
                    ],
                    "completes": [
                        {
                            "filesize": 34,
                            "from": "*",
                            "hashValue": "35"
                        }
                    ]
                }
            }
        }
    }
}
""")
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='h', update_type='minor', product='h', data_version=1)
        dbo.releases.t.insert().execute(name='h', product='h', version='1.0', data_version=1, data="""
{
    "name": "h",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "detailsUrl": "http://example.org/details",
    "licenseUrl": "http://example.org/license",
    "platforms": {
        "p": {
            "buildID": 1,
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 1,
                        "from": "*",
                        "hashValue": "1",
                        "fileUrl": "http://a.com/?foo=a"
                    }
                },
                "m": {
                    "complete": {
                        "filesize": 1,
                        "from": "*",
                        "hashValue": "1",
                        "fileUrl": "http://boring.com/a"
                    }
                }
            }
        }
    }
}
""")
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='j2', update_type='minor', product='j', data_version=1)
        dbo.releases.t.insert().execute(name='j1', product='j', version='39.0', data_version=1, data="""
{
    "name": "j1",
    "schema_version": 2,
    "platforms": {
        "p": {
            "buildID": "28",
            "locales": {
                "l": {}
            }
        }
    }
}
""")
        dbo.releases.t.insert().execute(name='j2', product='j', version='40.0', data_version=1, data="""
{
    "name": "j2",
    "schema_version": 2,
    "hashFunction": "sha512",
    "appVersion": "40.0",
    "displayVersion": "40.0",
    "platformVersion": "40.0",
    "fileUrls": {
        "c1": "http://a.com/%FILENAME%"
    },
    "ftpFilenames": {
        "partial": "j1-partial.mar",
        "complete": "complete.mar"
    },
    "platforms": {
        "p": {
            "buildID": "30",
            "OS_FTP": "o",
            "OS_BOUNCER": "o",
            "locales": {
                "l": {
                    "partial": {
                        "filesize": 6,
                        "from": "j1",
                        "hashValue": 5
                    },
                    "complete": {
                        "filesize": 38,
                        "from": "*",
                        "hashValue": "34"
                    }
                }
            }
        }
    }
}
""")
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='k', update_type='minor', product='k', data_version=1)
        dbo.releases.t.insert().execute(name='k', product='k', version='50.0', data_version=1, data="""
{
    "name": "k",
    "schema_version": 2,
    "hashFunction": "sha512",
    "appVersion": "50.0",
    "displayVersion": "50.0",
    "platformVersion": "50.0",
    "detailsUrl": "http://example.org/details",
    "licenseUrl": "http://example.org/license",
    "actions": "silent",
    "billboardURL": "http://example.org/billboard",
    "openURL": "http://example.org/url",
    "notificationURL": "http://example.org/notification",
    "alertURL": "http://example.org/alert",
    "showPrompt": "false",
    "showNeverForVersion": "true",
    "showSurvey": "false",
    "fileUrls": {
        "c1": "http://a.com/%FILENAME%"
    },
    "ftpFilenames": {
        "complete": "complete.mar"
    },
    "platforms": {
        "p": {
            "buildID": "35",
            "OS_FTP": "o",
            "OS_BOUNCER": "o",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 40,
                        "from": "*",
                        "hashValue": "35"
                    }
                },
                "l2": {
                    "isOSUpdate": true,
                    "complete": {
                        "filesize": 50,
                        "from": "*",
                        "hashValue": "45"
                    }
                }
            }
        }
    }
}
""")

    def tearDown(self):
        os.close(self.cef_fd)
        os.remove(self.cef_file)

    def testGetHeaderArchitectureWindows(self):
        self.assertEqual(self.view.getHeaderArchitecture('WINNT_x86-msvc', 'Firefox Intel Windows'), 'Intel')

    def testGetHeaderArchitectureMacIntel(self):
        self.assertEqual(self.view.getHeaderArchitecture('Darwin_x86-gcc3-u-ppc-i386', 'Firefox Intel Mac'), 'Intel')

    def testGetHeaderArchitectureMacPPC(self):
        self.assertEqual(self.view.getHeaderArchitecture('Darwin_ppc-gcc3-u-ppc-i386', 'Firefox PPC Mac'), 'PPC')

    def testDontUpdateToYourself(self):
        ret = self.client.get('/update/3/b/1.0/2/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testDontUpdateBackwards(self):
        ret = self.client.get('/update/3/b/1.0/5/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testDontDecreaseVersion(self):
        ret = self.client.get('/update/3/c/15.0/1/p/l/a/a/default/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testVersion3Get(self):
        ret = self.client.get('/update/3/a/1.0/1/a/a/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # An empty update contains an <updates> tag with a newline, which is what we're expecting here
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testVersion3GetWithUpdate(self):
        ret = self.client.get('/update/3/b/1.0/1/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testVersion2Get(self):
        ret = self.client.get('/update/2/b/1.0/0/p/l/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testVersion2GetIgnoresRuleWithDistribution(self):
        ret = self.client.get('/update/2/c/10.0/1/p/l/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testVersion4Get(self):
        ret = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testGetURLNotInWhitelist(self):
        ret = self.client.get('/update/3/d/20.0/1/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testEmptySnippetMissingExtv(self):
        ret = self.client.get('/update/3/e/20.0/1/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testRobotsExists(self):
        ret = self.client.get('/robots.txt')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/plain')
        self.assertTrue('User-agent' in ret.data)

    def testSchema2CompleteOnly(self):
        ret = self.client.get('/update/3/j/35.0/4/p/l/c1/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="40.0" appVersion="40.0" platformVersion="40.0" buildID="30">
        <patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="34" size="38"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema2WithPartial(self):
        ret = self.client.get('/update/3/j/39.0/28/p/l/c1/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="40.0" appVersion="40.0" platformVersion="40.0" buildID="30">
        <patch type="partial" URL="http://a.com/j1-partial.mar" hashFunction="sha512" hashValue="5" size="6"/>
        <patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="34" size="38"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema2WithOptionalAttributes(self):
        ret = self.client.get('/update/3/k/35.0/4/p/l/c1/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="50.0" appVersion="50.0" platformVersion="50.0" buildID="35" detailsURL="http://example.org/details" licenseURL="http://example.org/license" billboardURL="http://example.org/billboard" showPrompt="false" showNeverForVersion="true" showSurvey="false" actions="silent" openURL="http://example.org/url" notificationURL="http://example.org/notification" alertURL="http://example.org/alert">
        <patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="35" size="40"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema2WithIsOSUpdate(self):
        ret = self.client.get('/update/3/k/35.0/4/p/l2/c1/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="50.0" appVersion="50.0" platformVersion="50.0" buildID="35" detailsURL="http://example.org/details" licenseURL="http://example.org/license" billboardURL="http://example.org/billboard" showPrompt="false" showNeverForVersion="true" showSurvey="false" actions="silent" openURL="http://example.org/url" notificationURL="http://example.org/notification" alertURL="http://example.org/alert" isOSUpdate="true">
        <patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="45" size="50"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema3MultipleUpdates(self):
        ret = self.client.get('/update/3/f/22.0/5/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
        <patch type="partial" URL="http://a.com/p1" hashFunction="sha512" hashValue="3" size="2"/>
        <patch type="complete" URL="http://a.com/c2" hashFunction="sha512" hashValue="31" size="30"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

        ret = self.client.get('/update/3/f/23.0/6/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
        <patch type="partial" URL="http://a.com/p2" hashFunction="sha512" hashValue="5" size="4"/>
        <patch type="complete" URL="http://a.com/c1" hashFunction="sha512" hashValue="6" size="29"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema3NoPartial(self):
        ret = self.client.get('/update/3/f/20.0/1/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="25.0" appVersion="25.0" platformVersion="25.0" buildID="29">
        <patch type="complete" URL="http://a.com/c2" hashFunction="sha512" hashValue="31" size="30"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema3FtpSubstitutions(self):
        ret = self.client.get('/update/3/g/23.0/8/p/l/c1/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="26.0" appVersion="26.0" platformVersion="26.0" buildID="40">
        <patch type="partial" URL="http://a.com/g1-partial.mar" hashFunction="sha512" hashValue="5" size="4"/>
        <patch type="complete" URL="http://a.com/complete.mar" hashFunction="sha512" hashValue="35" size="34"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSchema3BouncerSubstitutions(self):
        ret = self.client.get('/update/3/g/23.0/8/p/l/c2/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="26.0" appVersion="26.0" platformVersion="26.0" buildID="40">
        <patch type="partial" URL="http://a.com/g1-partial" hashFunction="sha512" hashValue="5" size="4"/>
        <patch type="complete" URL="http://a.com/complete" hashFunction="sha512" hashValue="35" size="34"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSpecialQueryParam(self):
        ret = self.client.get('/update/3/h/0.5/0/p/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://a.com/?foo=a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testSpecialQueryParamForced(self):
        ret = self.client.get('/update/3/h/0.5/0/p/l/a/a/a/a/update.xml?force=1')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://a.com/?foo=a&amp;force=1" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testNonSpecialQueryParam(self):
        ret = self.client.get('/update/3/h/0.5/0/p/m/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testNonSpecialQueryParamForced(self):
        ret = self.client.get('/update/3/h/0.5/0/p/m/a/a/a/a/update.xml?force=1')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testNoSpecialDefined(self):
        app.config['SPECIAL_FORCE_HOSTS'] = None
        ret = self.client.get('/update/3/h/0.5/0/p/m/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://boring.com/a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())


class ClientTestWithErrorHandlers(unittest.TestCase):
    """Most of the tests are run without the error handler because it gives more
       useful output when things break. However, we still need to test that our
       error handlers works!"""
    def setUp(self):
        app.config['DEBUG'] = True
        app.config['WHITELISTED_DOMAINS'] = ('a.com',)
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        self.client = app.test_client()
        self.view = ClientRequestView()

    def testEmptySnippetOn404(self):
        ret = self.client.get('/whizzybang')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testEmptySnippetOn500(self):
        with mock.patch('auslib.web.views.client.ClientRequestView.get') as m:
            m.side_effect = Exception('I break!')
            ret = self.client.get('/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml')
            self.assertEqual(ret.status_code, 200)
            self.assertEqual(ret.mimetype, 'text/xml')
            self.assertEqual(minidom.parseString(ret.data).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')


class GMPClientTest(unittest.TestCase):
    maxDiff = 2000

    @classmethod
    def setUpClass(cls):
        # Error handlers are removed in order to give us better debug messages
        cls.error_spec = app.error_handler_spec
        # Ripped from https://github.com/mitsuhiko/flask/blob/1f5927eee2288b4aaf508af5dc1f148aa2140d91/flask/app.py#L394
        app.error_handler_spec = {None: {}}

    @classmethod
    def tearDownClass(cls):
        app.error_handler_spec = cls.error_spec

    def setUp(self):
        self.cef_fd, self.cef_file = mkstemp()
        app.config['DEBUG'] = True
        app.config['SPECIAL_FORCE_HOSTS'] = ('http://a.com',)
        app.config['WHITELISTED_DOMAINS'] = ('a.com', 'boring.com')
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.setDomainWhitelist(('a.com', 'boring.com'))
        self.client = app.test_client()
        self.view = ClientRequestView()
        auslib.log.cef_config = auslib.log.get_cef_config(self.cef_file)
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='gg', update_type='minor', product='gg', data_version=1)
        dbo.releases.t.insert().execute(name='gg', product='gg', version='1.0', data_version=1, data="""
{
    "name": "gg",
    "schema_version": 1000,
}
""")

    def test


# TODO: kill this with fire, brimstone, and extreme prejudice when bug 1013354 is fixed.
class HackyH264Tests(unittest.TestCase):
    maxDiff = 2000
    @classmethod
    def setUpClass(cls):
        # Error handlers are removed in order to give us better debug messages
        cls.error_spec = app.error_handler_spec
        # Ripped from https://github.com/mitsuhiko/flask/blob/1f5927eee2288b4aaf508af5dc1f148aa2140d91/flask/app.py#L394
        app.error_handler_spec = {None: {}}

    @classmethod
    def tearDownClass(cls):
        app.error_handler_spec = cls.error_spec

    def setUp(self):
        app.config['DEBUG'] = True
        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        self.client = app.test_client()
        dbo.rules.t.insert().execute(backgroundRate=100, mapping='HackyH264Blob', update_type='minor', product='GMP', data_version=1)
        dbo.releases.t.insert().execute(name='HackyH264Blob', product='GMP', version='1.0', data_version=1, data="""
{
    "name": "HackyH264Blob",
    "schema_version": 3,
    "hashFunction": "sha512",
    "ftpFilenames": {
        "completes": {
            "crap": "<updates><addons><addon id=\\"openh264-plugin@cisco.com\\" URL=\\"http://download.cdn.cisco.com/openh264/win32/openh264-1.1.zip\\" hashFunction=\\"SHA512\\" hashValue=\\"ABCDEF123456\\" size=\\"123\\" version=\\"1.1\\" /></addons></updates>"
        }
    }
}
""")

    def testCrapWorks(self):
        ret = self.client.get('/update/3/GMP/20.0/1/crap/l/a/a/a/a/update.xml')
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, 'text/xml')
        returned = minidom.parseString(ret.data)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates><addons><addon id="openh264-plugin@cisco.com" URL="http://download.cdn.cisco.com/openh264/win32/openh264-1.1.zip" hashFunction="SHA512" hashValue="ABCDEF123456" size="123" version="1.1"/></addons></updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())
