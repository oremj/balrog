import difflib
from multiprocessing import Pool

import requests


def compare_snippets(url1, url2, retries=3, timeout=10, diff=True):
    cfg = {'max_retries': retries}
    xml1 = requests.get(url1, timeout=timeout, config=cfg).content.splitlines()
    xml2 = requests.get(url2, timeout=timeout, config=cfg).content.splitlines()
    ret = [url1, xml1, url2, xml2]
    if xml1 != xml2:
        if diff:
            difflines = []
            for line in difflib.unified_diff(xml1, xml2, lineterm=""):
                difflines.append(line)
            ret.append(difflines)
        else:
            ret.append(True)
    else:
        ret.append(False)
    return ret
