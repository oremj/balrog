#!/usr/bin/env python

import logging
import os.path
import site
import sys

site.addsitedir(os.path.join(os.path.dirname(__file__), "../lib/python"))
site.addsitedir(os.path.join(os.path.dirname(__file__), "../lib/python/vendor"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from auslib.blobs.apprelease import ReleaseBlobV4
from auslib.db import AUSDatabase

log = logging.getLogger(__name__)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--db", dest="db", required=True)
    parser.add_argument("--name", dest="name", required=True)
    parser.add_argument("releases", metavar="release", nargs="+")

    args = parser.parse_args()

    db = AUSDatabase(args.db)

    for release in args.releases:
        try:
            rel = db.releases.getReleases(name=release)[0]
            blob = rel["data"]
        except:
            log.debug("No such release '%s', skipping", release)

        if blob["schema_version"] == 4:
            log.debug("%s is already schema 4, skipping", release)
            continue
        elif blob["schema_version"] != 3:
            log.debug("%s is not schema 3, can't upgrade it", release)
            continue

        try:
            v4Blob = ReleaseBlobV4.fromV3(blob)
            db.release.updateRelease(release, args.name, rel["data_version"], blob=v4Blob)
        except:
            log.exception("Failed to upgrade %s", release)
