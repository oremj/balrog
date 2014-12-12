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
    def __init__(self):
        self.caches = {}

    def make_cache(self, name, maxsize, timeout):
        if name in self.caches:
            raise Exception()
        self.caches[name] = ExpiringLRUCache(maxsize, timeout)

    def reset(self):
        self.caches.clear()

    def get(self, name, key, get_value=None):
        if name not in self.caches:
            if callable(get_value):
                return get_value()
            else:
                return None

        value = self.caches[name].get(key)
        if not value and callable(get_value):
            value = get_value()
            self.put(name, key, value)

        return value

    def put(self, name, key, value):
        if name not in self.caches:
            return

        return self.caches[name].put(key, value)

    def clear(self, name=None):
        if name and name not in self.caches:
            return

        if not name:
            for c in self.caches.values():
                c.clear()

        self.caches[name].clear()

    def invalidate(self, name, key):
        if name not in self.caches:
            return

        self.caches[name].invalidate(key)
