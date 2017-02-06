#!/usr/bin/env python3.5
import asyncio
import aiohttp
from collections import defaultdict

async def check_url(url):
    resp = await aiohttp.head(url)
    resp.close()
    return url, resp.status == 200


async def main(release_urls):
    failures = defaultdict(set)
    in_process = []
    # TODO: this ||ization might not work right? when bhearsum ran this, there appeared to be 100s of connections in TIME_WAIT at once
    n = 16

    for release, urls in release_urls.items():
        print("Checking {} URLs from {}".format(len(urls), release))
        while urls:
            url = urls.pop()
            in_process.append(asyncio.ensure_future(check_url(url)))
            if len(in_process) >= n:
                done, pending = await asyncio.wait(in_process, return_when=asyncio.FIRST_COMPLETED)
                for d in done:
                    in_process.remove(d)
                    url, result = d.result()
                    if not result:
                        failures[release].add(url)

    done, pending = await asyncio.wait(in_process)
    for d in done:
        in_process.remove(d)
        url, result = d.result()
        if not result:
            failures[release].add(url)

    for release, urls in failures.items():
        # TODO: the release here often ends up wrong. maybe the loops above override the variable before the failures are seen?
        print("Failed URLs for {}".format(release))
        print("\n".join(urls))

if __name__ == '__main__':
    import sys, json
    release_urls = json.loads(open(sys.argv[1]).read())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(release_urls))
    loop.close()
