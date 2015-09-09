import mock
import unittest
from xml.dom import minidom

from auslib.blobs.whitelist import WhitelistBlobV1


class TestWhitelistBlobV1(unittest.TestCase):
    # TODO: test shouldServeUpdates in a bunch of ways. see other blob tests for examples.
