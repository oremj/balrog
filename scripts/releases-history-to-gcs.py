#!/usr/bin/env python3

import base64
from collections import defaultdict
import hashlib
import sys

import requests

from google.cloud import storage

skip_patterns = ("-nightly-",)

balrog_api = sys.argv[1]

releases = {}
for r in requests.get("{}/releases".format(balrog_api)).json()["releases"]:
    # Take note of the highest data version, so we can sanity check later
    releases[r["name"]] = r["data_version"]

client = storage.Client()
bucket = client.get_bucket(sys.argv[2])

uploads = defaultdict(int)

for n, r in enumerate(releases):
    print("Processing {}, {}% complete".format(r, int(n / len(releases) * 100)))
    if any(pat in r for pat in skip_patterns):
        print("  Skipping because it matches a skip pattern")
    n += 1
    if n == 10:
        break
    for rev in requests.get("{}/releases/{}/revisions".format(balrog_api, r)).json()["revisions"]:
        old_version = requests.get("{}/history/view/release/{}/data".format(balrog_api, rev["change_id"])).text
        old_version_hash = hashlib.md5(old_version.encode("ascii")).digest()
        current_blob = bucket.get_blob("{}/{}-{}-{}.json".format(r, rev["data_version"], rev["timestamp"], rev["changed_by"]))
        current_blob_hash = None
        if current_blob:
            current_blob_hash = base64.b64decode(current_blob.md5_hash)
        if old_version_hash != current_blob_hash:
            print("  Uploading data version {}".format(rev["data_version"]))
            blob = bucket.blob("{}/{}-{}-{}.json".format(r, rev["data_version"], rev["timestamp"], rev["changed_by"]))
            blob.upload_from_string(old_version, content_type="application/json")
        else:
            print("  Skipping data version {} because its md5 matches".format(rev["data_version"]))
        uploads[r] += 1

for r in releases:
    if r not in uploads:
        print("WARNING: {} was found in the Balrog API but does not exist in GCS".format(r))
    elif releases[r] != uploads[r]:
        print("WARNING: {} has a data version of {} in the Balrog API, but only {} revisions in GCS".format(r, releases[r], uploads[r]))
