import re

from auslib.blobs.base import Blob
from auslib.errors import BadDataError


class WhitelistBlobV1(Blob):
    format_ = {
        "name": None,
        "schema_version": None,
        # TODO: add data structure for storing whitelisted values
    }

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 3000

    def shouldServeUpdate(self, updateQuery):
        # TODO: return True only if value in updateQuery matches something in whitelist

    def createXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        # No-op function, because updates are not actually served by this class. Maybe raise an exception here?
