from collections import defaultdict

from repoze.lru import ExpiringLRUCache


class MaybeCacher(object):
    """MaybeCacher is a very simple wrapper to work around the fact that we
    have two consumers of the auslib library (admin app, non-admin app) that
    require different caching behaviour. The admin app should never cache
    anything, but the non-admin app should. This class is intended to be
    instantiated as a global object, and then have its maxsize and timeout
    attributes set properly by the consumers.

    If maxsize is less than 1, this class' methods will always return nothing.
    If maxsize is 1 or more, caching will be performed. It is up to callers to
    cope with both cases. In a world where bug 1109295 is fixed, we may not
    need this anymore."""
    def __init__(self, maxsize=0, timeout=0):
        self._maxsize = maxsize
        self._timeout = timeout
        # By using a dict of caches, we can have multiple namespaces with
        # different sizes. This allows us to do things like have smaller cache
        # for blobs (which are very large) and a larger one for rules
        # (which are tiny). This idea is completely ripped off from repoze's
        # CacheMaker class.
        self.cache = defaultdict(lambda: ExpiringLRUCache(self._maxsize, self._timeout))

    def get(self, name, key):
        if self._maxsize < 1:
            return

        return self.cache[name].get(key)

    def put(self, name, key, value):
        if self._maxsize < 1:
            return

        return self.cache[name].put(key, value)

    def clear(self, name):
        if self._maxsize < 1:
            return

        self.cache[name].clear()

    def invalidate(self, name, key):
        if self._maxsize < 1:
            return

        self.cache[name].invalidate(key)
