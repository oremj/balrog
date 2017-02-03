#!/usr/bin/env python

from collections import defaultdict
import multiprocessing
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

failures = defaultdict(set)

def check_url(release, urls):
    failed = set()
    for url in urls:
        r = session.get(url)
        if r.status_code != 200:
            failed.add(url)
    return (release, failed)

def analyze(result):
    release, failed_urls = result
    failures[release] = failed_urls

pool = multiprocessing.Pool(32)
async_results = []
i = 0
for release, urls in mar_urls.iteritems():
    i += 1
    if i > 10:
        break
    async_results.append(pool.apply_async(check_url, (release, urls), {}, analyze))

pool.close()
pool.join()

for release, urls in failures.iteritems():
    print "Failed URLs for %s" % release
    print "\n".join(urls)

# check for exceptions in workers
[r.get() for r in async_results]
