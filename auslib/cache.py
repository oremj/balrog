from collections import defaultdict

from repoze.lru import ExpiringLRUCache


class MaybeCacher(object):
    # TODO: Add docs
    def __init__(self, maxsize=0, timeout=0):
        self._maxsize = maxsize
        self._timeout = timeout
        self.cache = defaultdict(lambda: ExpiringLRUCache(self._maxsize, self._timeout))

    def __getattr__(self, name):
        # TODO: is do_nothing too much of a hack? maybe it's better to override specific methods instead?
        def do_nothing(*args, **kwargs):
            return None

        # Nothing to do if we have no cache!
        if self._maxsize < 1:
            return do_nothing

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
