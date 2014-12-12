from random import randint
from urlparse import urlparse

import logging

from auslib.global_state import cache, dbo
from auslib.log import cef_event, CEF_ALERT


def isSpecialURL(url, specialForceHosts):
    if not specialForceHosts:
        return False
    for s in specialForceHosts:
        if url.startswith(s):
            return True
    return False

def isForbiddenUrl(url, whitelistedDomains):
    domain = urlparse(url)[1]
    if domain not in whitelistedDomains:
        cef_event("Forbidden domain", CEF_ALERT, domain=domain)
        return True
    return False

def getFallbackChannel(channel):
    return channel.split('-cck-')[0]


class AUSRandom:
    """Abstract getting a randint to make it easier to test the range of
    possible values"""
    def __init__(self, min=0, max=99):
        self.min = min
        self.max = max

    def getInt(self):
        return randint(self.min, self.max)

    def getRange(self):
        return range(self.min, self.max+1)

class AUS:
    def __init__(self):
        self.specialForceHosts = None
        self.rand = AUSRandom()
        self.log = logging.getLogger(self.__class__.__name__)

    def evaluateRules(self, updateQuery):
        # The cache key needs to be hashable, so we can't use the updateQuery
        # object. Sorting the values of updateQuery makes sure we don't have
        # cache misses if the natural "order" of the updateQuery dict changes
        # from request to request
        # This is a complex statement, so here's an unpacked explanation
        # from the inner most portion to outer:
        # * Start with all of the values in the updateQuery
        # * Sort them, for consistency across requests
        # * Coerce them to strings, because some may not be
        # * Join them into a single string, delimited by "-"
        #cache_key = "-".join([str(v) for v in sorted(updateQuery.values())])
        #cached = cache.get("evaluated_rules", cache_key)
        cached = False
        if cached:
            self.log.debug("Using evaluated rules from cache.")
            rule = cached
        else:
            self.log.debug("Looking for rules that apply to:")
            self.log.debug(updateQuery)
            rules = dbo.rules.getRulesMatchingQuery(
                updateQuery,
                fallbackChannel=getFallbackChannel(updateQuery['channel'])
            )

            ### XXX throw any N->N update rules and keep the highest priority remaining one
            if len(rules) < 1:
                return None, None

            rules = sorted(rules,key=lambda rule: rule['priority'], reverse=True)
            rule = rules[0]
            #cache.put("evaluated_rules", cache_key, rule)

        self.log.debug("Matching rule: %s" % rule)
        # There's a few cases where we have a matching rule but don't want
        # to serve an update:
        # 1) No mapping.
        if not rule['mapping']:
            self.log.debug("Matching rule points at null mapping.")
            return None, None

        # 2) For background checks (force=1 missing from query), we might not
        # serve every request an update
        # backgroundRate=100 means all requests are served
        # backgroundRate=25 means only one quarter of requests are served
        if not updateQuery['force'] and rule['backgroundRate'] < 100:
            self.log.debug("backgroundRate < 100, rolling the dice")
            if self.rand.getInt() >= rule['backgroundRate']:
                self.log.debug("request was dropped")
                return None, None

        # 3) Incoming release is older than the one in the mapping, defined as one of:
        #    * version decreases
        #    * version is the same and buildID doesn't increase
        blob = dbo.releases.getReleaseBlob(name=rule["mapping"])
        if not blob.shouldServeUpdate(updateQuery):
            return None, None

        self.log.debug("Returning release %s", blob["name"])
        return blob, rule['update_type']
