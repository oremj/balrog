#!/usr/bin/env python3

import asyncio
import base64
from collections import defaultdict
import hashlib
import sys

import aiohttp

from gcloud.aio.storage import Storage


skip_patterns = ("-nightly-",)


async def get_revisions(r, session, balrog_api):
    async with session.get("{}/releases/{}/revisions".format(balrog_api, r)) as resp:
        return (await resp.json())["revisions"]


async def get_releases(session, balrog_api):
    async with session.get("{}/releases".format(balrog_api)) as resp:
        for r in (await resp.json())["releases"]:
            yield (r["name"], r["data_version"])


async def process_release(r, session, balrog_api, bucket):
    processed = 0

    # TODO: may need limiting or a semaphore when talking to balrog?
    for rev in await get_revisions(r, session, balrog_api):
        old_version = await (await session.get("{}/history/view/release/{}/data".format(balrog_api, rev["change_id"]))).text()
        old_version_hash = hashlib.md5(old_version.encode("ascii")).digest()
        try:
            current_blob = await bucket.get_blob("{}/{}-{}-{}.json".format(r, rev["data_version"], rev["timestamp"], rev["changed_by"]))
            current_blob_hash = base64.b64decode(current_blob.md5Hash)
        except aiohttp.ClientResponseError:
            current_blob_hash = None
        if old_version_hash != current_blob_hash:
            print("{}: Uploading data version {}".format(r, rev["data_version"]))
            blob = bucket.new_blob("{}/{}-{}-{}.json".format(r, rev["data_version"], rev["timestamp"], rev["changed_by"]))
            await blob.upload(old_version, session)
        else:
            print("{}: Skipping data version {} because its md5 matches".format(r, rev["data_version"]))

        processed += 1

    return r, processed

async def main(loop, balrog_api, bucket_name):
    uploads = defaultdict(int)
    releases = {}

    n = 0

    # TODO: ok to share the session between balrog and gcs?
    async with aiohttp.ClientSession(loop=loop) as session:
        storage = Storage(session=session)
        bucket = storage.get_bucket(bucket_name)

        async with session.get("{}/releases".format(balrog_api)) as resp:
            for r in (await resp.json())["releases"]:
                releases[r["name"]] = r["data_version"]

        release_futures = []
        for r in releases:
            if any(pat in r for pat in skip_patterns):
                print("Skipping {} because it matches a skip pattern".format(r))
            n += 1
            if n == 10:
                break

            release_futures.append(process_release(r, session, balrog_api, bucket))

        for (r, processed) in await asyncio.gather(*release_futures):
            uploads[r] = processed

    for r in releases:
        if r not in uploads:
            print("WARNING: {} was found in the Balrog API but does not exist in GCS".format(r))
        elif releases[r] != uploads[r]:
            print("WARNING: {} has a data version of {} in the Balrog API, but only {} revisions in GCS".format(r, releases[r], uploads[r]))

balrog_api = sys.argv[1]
bucket_name = sys.argv[2]
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop, balrog_api, bucket_name))
