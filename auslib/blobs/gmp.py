from auslib.AUS import containsForbiddenDomain
from auslib.blobs.base import Blob


class GMPBlobV1(Blob):
    format_ = {
        "name": None,
        "schema_version": None,
        "hashFunction": None,
        "vendors": {
            "*": {
                "version": None,
                "platforms": {
                    "*": {
                        "filesize": None,
                        "hashValue": None,
                        "fileUrl": None,
                    }
                }
            }
        }
    }

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 1000

    def shouldServeUpdate(self, updateQuery):
        # GMP updates should always be returned. It is the responsibility
        # of the client to decide whether or not any action needs to be taken.
        return True

    def createXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        buildTarget = updateQuery["buildTarget"]

        vendorXML = []
        for id_, vendorInfo in self.get("vendors", {}).iteritems():
            platformInfo = vendorInfo.get("platforms", {}).get(buildTarget)
            if not platformInfo:
                continue

            url = platformInfo["fileUrl"]
            if updateQuery["force"]:
                url = self.processSpecialForceHosts(url, specialForceHosts)
            if containsForbiddenDomain(url, whitelistedDomains):
                continue
            vendorXML.append('        <addon id="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%d" version="%s"/>' % \
                (id_, url, self["hashFunction"], platformInfo["hashValue"],
                    platformInfo["filesize"], vendorInfo["version"]))

        xml = ['<?xml version="1.0"?>']
        xml.append('<updates>')
        if vendorXML:
            xml.append('    <addons>')
            xml.extend(vendorXML)
            xml.append('    </addons>')
        xml.append('</updates>')
        return xml
