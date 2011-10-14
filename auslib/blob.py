import simplejson as json

import logging
log = logging.getLogger(__name__)

def isValidBlob(format, data):
    # If there's no format at all, we assume the data is valid.
    if not format:
        return True
    for key in data.keys():
        # A '*' key in the format means that all key names in the data are accepted.
        if '*' in format:
            # But we still need to validate the sub-blob, if it exists.
            if format['*'] and not isValidBlob(format['*'], data[key]):
                log.debug("blob is not valid because of key '%s'" % key)
                return False
        # If there's no '*' key, we need to make sure the key name is valid
        # and the sub-blob is valid, if it exists.
        elif key not in format or not isValidBlob(format[key], data[key]):
            log.debug("blob is not valid because of key '%s'" % key)
            return False
    return True

class Blob(dict):
    format = {}

    def isValid(self):
        return isValidBlob(self.format, self)

    def loadJSON(self, blob):
        self.clear()
        self.update(json.loads(blob))

    def getJSON(self):
        return json.dumps(self)

class ReleaseBlobV1(Blob):
    """Format is used in validating a blob. Validation follows these rules:
       1) If there's no format at all, the blob is valid.
       2) If the format contains a '*' key, all key names are accepted.
       3) If the value for the key is None, all values for that key are valid.
       4) If the value for the key is a dictionary, validate it.
    """
    format = {
        'name': None,
        'schema_version': None,
        'detailsUrl': None,
        'fileUrls': {
            '*': None
        },
        'ftpFilenames': {
            '*': None
        },
        'bouncerProducts': {
            '*': None
        },
        'hashFunction': None,
        'fakePartials': None,
        'extv': None,
        'appv': None,
        'platforms': {
            '*': {
                'alias': None,
                'buildID': None,
                'OS_BOUNCER': None,
                'OS_FTP': None,
                'locales': {
                    '*': {
                        'partial': {
                            'filesize': None,
                            'from': None,
                            'hashValue': None,
                            'fileUrl': None
                        },
                        'complete': {
                            'filesize': None,
                            'from': None,
                            'hashValue': None,
                            'fileUrl': None
                        }
                    }
                }
            }
        }
    }

