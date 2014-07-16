from auslib.AUS import isSpecialURL, containsForbiddenDomain, getFallbackChannel
from auslib.blobs.base import Blob


class GMPBlob(Blob):
    format_ = {
        "name": None,
        "schema_version": None,
        "version": None,
        "vendor_id": None,
        "hashFunction": None,
        "platforms": {
            "*": {
                "filesize": None,
                "hashValue": None,
                "fileUrl": None,
            }
        }
    }

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 1000

    def createXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
