from collections import defaultdict

from repoze.lru import ExpiringLRUCache


class MaybeCacher(object):
    # TODO: Add docs
    def __init__(self, maxsize=None, timeout=None):
        self._maxsize = maxsize
        self._timeout = timeout
        self.cache = defaultdict(lambda: ExpiringLRUCache(self._maxsize, self._timeout))

    def __getattr__(self, name):
        # Nothing to do if we have no cache!
        if self._maxsize < 1:
            return None

        # Otherwise, delegate to the real cache object.
        return getattr(self.cache, name)


#    def get(self, name, key):
#        if self._maxsize < 1:
#            return None
#
#        return self.cache[name].get(key)
#
#    def put(self, name, key, value):
#        # Nothing to do if we have no cache!
#        if self._maxsize < 1:
#            return
#
#        return self.cache[name].put(key, value)
#
#    def clear(self, name):
#        self.cache[name].clear()
#
#    def invalidate(self, name, key):
#        self.cache[name].invalidate(key)
