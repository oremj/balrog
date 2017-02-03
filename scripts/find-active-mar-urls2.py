#!/usr/bin/env python

from collections import defaultdict
import json
import sys

import requests
import requests.adapters

from auslib.blobs.base import createBlob


base_url = sys.argv[1]

session = requests.Session()
retry_adapter = requests.adapters.HTTPAdapter(max_retries=3)
session.mount("http://", retry_adapter)
session.mount("https://", retry_adapter)

active_releases = set()
mar_urls = defaultdict(set)

# TODO: would be nice to be able to filter by channel. we'd have to
#       do this first by filtering rules, and then also enhance some of the
#       getAllFileUrls() methods to support it

for rule in session.get("{}/api/rules".format(base_url)).json()["rules"]:
    active_releases.add(rule["mapping"])
    active_releases.add(rule["fallbackMapping"])

for release in active_releases:
    if not release:
        continue
    raw_blob = session.get("{}/api/releases/{}".format(base_url, release)).json()
    blob = createBlob(raw_blob)
    for url in blob.getAllFileUrls():
        mar_urls[release].add(url)
    response_blobs = blob.getResponseBlobs()
    if response_blobs:
        raw_blob = session.get("{}/api/releases/{}".format(base_url, release)).json()
        blob = createBlob(raw_blob)
        for url in blob.getAllFileUrls():
            mar_urls[release].add(url)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

print json.dumps(mar_urls, default=set_default)
