from auslib.AUS import isSpecialURL, containsForbiddenDomain
from auslib.blobs.base import Blob


class GMPBlobV1(Blob):
    format_ = {
        "name": None,
        "schema_version": None,
        "hashFunction": None,
        "vendors": {
            "*": {
                "version": "*",
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

    def createXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        buildTarget = updateQuery["buildTarget"]

        vendorXML = []
        for id_, vendorInfo in self.get("vendors", {}).iteritems():
            for platformInfo in vendorInfo.get("platforms", {}).get(buildTarget):
                vendorXML.append('        <addon id="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%d" version="%s">' % \
                    (id_, platformInfo["fileUrl"], self["hashFunction"], platformInfo["hashValue"],
                     platformInfo["filesize"], vendorInfo["version"]))

        xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xml.append('<updates>')
        if vendorXML:
            xml.append('    <addons>')
            for x in vendorXML:
                xml.append(x)
                xml.append("\n")
            xml.append('    </addons>')
        xml.append('</updates>')
