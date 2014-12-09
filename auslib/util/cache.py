from collections import defaultdict

from repoze.lru import ExpiringLRUCache


class MaybeCacher(object):
    # TODO: Add docs
    def __init__(self, maxsize=0, timeout=0):
        self._maxsize = maxsize
        self._timeout = timeout
        self.cache = defaultdict(lambda: ExpiringLRUCache(self._maxsize, self._timeout))

    def get(self, name, key):
        if self._maxsize < 1:
            return

        return self.cache[name].get(key)

    def put(self, name, key, value):
        # Nothing to do if we have no cache!
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
