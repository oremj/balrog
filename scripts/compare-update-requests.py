#!/usr/bin/env python

from multiprocessing import Pool
import os.path
import site
import sys

site.addsitedir(os.path.join(os.path.dirname(__file__), "../lib/python"))
site.addsitedir(os.path.join(os.path.dirname(__file__), "../lib/python/vendor"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import requests

from auslib.util.testing import compare_snippets


def do_compare_wrapper(args):
    return compare_snippets(*args)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('aus_servers', metavar='aus_server', nargs=2,
        help='AUS Servers to make requests against. There must be two.')
    parser.add_argument('--paths-file', dest='paths_file', required=True)
    parser.add_argument('-j', dest='concurrency', default=1, type=int)

    args = parser.parse_args()

    server1, server2 = args.aus_servers

    try:
        paths = requests.get(args.paths_file).content.splitlines()
    # Should be catching MissingSchema here, but our requests doesn't have it.
    except ValueError:
        paths = open(args.paths_file).readlines()

    p = Pool(processes=args.concurrency)

    worker_args = []
    for path in paths:
        url1 = '%s/%s' % (server1, path)
        url2 = '%s/%s' % (server2, path)
        worker_args.append((url1, url2))

    rc = 0

    for res in p.map(do_compare_wrapper, worker_args):
        url1, _, url2, _, diff = res
        if diff:
            rc = 1
            print 'Unmatched snippets:'
            print url1.strip()
            print url2.strip()
            for line in diff:
                print line
            print '---- end of diff\n'

    sys.exit(rc)
