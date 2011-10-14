import simplejson as json

import logging
log = logging.getLogger(__name__)

class UnknownKeyError(Exception):
    """Raised when an unknown key is found in a blob."""

class Blob(dict):
    """A class that represents a JSON blob that is stored in the database.
       A Blob provides facility to do simple validation of incoming data
       by adjusting validation_keys. The validation algorithm is as follows:
       * If validation_keys is None/empty, all keys are considered valid.
       * Otherwise, all keys in incoming data must be present in validation_keys,
         or a KeyError will be raised.
       * If a key's value in validation_keys is None, no further validation is
         done.
       * If a key's value in validation_keys is a callable, it will be instantiated,
         have its loadDict() method called and passed the value of the key in the
         incoming data, and finally, have its validate() method called.
       """
    validation_keys = None

    def __init__(self):
        self.json = None

    def _load(self):
        for key in self.keys():
            klass = self.getClassFor(key)
            log.debug("Blob._load: getClassFor(%s) returned %s" % (key, klass))
            if not klass:
                continue
            newsection = klass()
            newsection.loadDict(self[key])
            self[key] = newsection
        self.validate()

    def loadJSON(self, data):
        log.debug("Blob.loadJSON: loading %s" % data)
        self.clear()
        self.update(json.loads(data))
        self._load()

    def loadDict(self, data):
        log.debug("Blob.loadDict: loading %s" % data)
        self.clear()
        self.update(data)
        self._load()

    def getJSON(self):
        return json.dumps(self)

    def getClassFor(self, key):
        """Try to find the class for a given key."""
        try:
            return self.validation_keys[key]
        except KeyError:
            return None

    def validate(self):
        log.debug("Blob.validate: validation_keys is: %s" % self.validation_keys)
        if not self.validation_keys or len(self) == 0:
            return
        for k in self.keys():
            if k not in self.validation_keys:
                raise UnknownKeyError("Blob.validate: Unknown key '%s'" % k)
            if callable(self[k]):
                self[k].validate()

class FileUrlsBlob(Blob):
    def getClassFor(self, key):
        return None

class FtpFilenamesBlob(Blob):
    validation_keys = dict(partial=None, complete=None)

class BouncerProductsBlob(Blob):
    validation_keys = dict(partial=None, complete=None)

class UpdateBlob(Blob):
    validation_keys = {'filesize': None, 'from': None, 'hashValue': None, 'fileUrl': None}

class SingleBuildBlob(Blob):
    validation_keys = dict(partial=UpdateBlob, complete=UpdateBlob)

class BuildsBlob(Blob):
    def getClassFor(self, key):
        return SingleBuildBlob

class SinglePlatformBlob(Blob):
    validation_keys = dict(alias=None, buildID=None, OS_BOUNCER=None, OS_FTP=None, locales=BuildsBlob)

class PlatformsBlob(Blob):
    def getClassFor(self, key):
        return SinglePlatformBlob

class ReleaseBlobSchema1(Blob):
    validation_keys = dict(name=None, schema_version=None, detailsUrl=None, fileUrls=FileUrlsBlob,
                ftpFilenames=FtpFilenamesBlob, bouncerProducts=BouncerProductsBlob,
                hashFunction=None, fakePartials=None, platforms=PlatformsBlob,
                extv=None, appv=None)
