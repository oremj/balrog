from flask import make_response, request
from flask.views import MethodView

from auslib.web.base import AUS

import logging

queryVersionParams = {
    3: ['product', 'version', 'buildID', 'buildTarget', 'locale', 'channel',
          'osVersion', 'distribution', 'distVersion',],
    4: ['product', 'version', 'buildID', 'buildTarget', 'locale', 'channel',
          'osVersion', 'distribution', 'distVersion', 'platformVersion'],
}

def getHeaderArchitecture(buildTarget, ua):
    if buildTarget.startswith('Darwin'):
        if ua and 'PPC' in ua:
            return 'PPC'
        else:
            return 'Intel'
    else:
        return 'Intel'

def getQueryFromURL(queryVersion, url):
    """ Turn
            "update/3/Firefox/4.0b13pre/20110303122430/Darwin_x86_64-gcc-u-i386-x86_64/en-US/nightly/Darwin%2010.6.0/default/default/update.xml?force=1"
        into
            testUpdate = {
                    'product': 'Firefox',
                    'version': '4.0b13pre',
                    'buildID': '20110303122430',
                    'buildTarget': 'Darwin_x86_64-gcc-u-i386-x86_64',
                    'locale': 'en-US',
                    'channel': 'nightly',
                    'osVersion': 'Darwin%2010.6.0',
                    'distribution': 'default',
                    'distVersion': 'default',
                    'headerArchitecture': 'Intel',
                    'force': True,
                    'name': ''
                    }
    """
    if queryVersion not in queryVersionParams:
        return {}
    query = {}
    for param in queryVersionParams[queryVersion]:
        query[param] = url[param]
    query['name'] = AUS.identifyRequest(query)
    query['force'] = (int(request.args.get('force', 0)) == 1)
    if 'buildTarget' in queryVersionParams[queryVersion]:
        ua = request.headers.get('User-Agent')
        query['headerArchitecture'] = getHeaderArchitecture(query['buildTarget'], ua)
    return query

class ClientRequestView(MethodView):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        MethodView.__init__(self, *args, **kwargs)

    """/update/<queryVersion>/<product>/<version>/<buildID>/<build target>/<locale>/<channel>/<os version>/<distribution>/<distribution version>"""
    def get(self, queryVersion, **url):
        query = getQueryFromURL(queryVersion, url)
        self.log.debug("Got query: %s", query)
        if query:
            rule = AUS.evaluateRules(query)
        else:
            rule = {}
        # passing {},{} returns empty xml
        self.log.debug("Got rule: %s", rule)
        xml = AUS.createXML(query, rule)
        self.log.debug("Sending XML: %s", xml)
        response = make_response(xml)
        response.mimetype = 'text/xml'
        return response
