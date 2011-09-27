from flask.views import MethodView

from auslib.client.base import app, AUS

class ClientRequestView(MethodView):
    def getQueryFromURL(self, url):
        """ Use regexp to turn
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
                      'name': ''
                     }
        """
        # TODO support older URL versions. catlee suggests splitting on /, easy to use conditional assignment then
        # TODO support force queries to void throttling, and pass through to downloads
        query = url.copy()
        # TODO: Better way of dispatching different versions when we actually have to deal with them.
        if queryVersion == 3:
            query['name'] = AUS.identifyRequest(query)
            if query['buildTarget'].startswith('Darwin'):
                ua = self.headers.getfirstmatchingheader('User-Agent')
                if ua and 'PPC' in ua[0]:
                    query['headerArchitecture'] = 'PPC'
                else:
                    query['headerArchitecture'] = 'Intel'
            else:
                query['headerArchitecture'] = 'Intel'
            return query
        return {}

    """/update/3/<product>/<version>/<buildid>/<build target>/<locale>/<channel>/<os version>/<distribution>/<distribution version>"""
    def get(self, queryVersion, **url):
        query = self.getQueryFromURL(url)
        if query:
            rule = AUS.evaluateRules(query)
        else:
            rule = {}
        # passing {},{} returns empty xml
        return AUS.createXML(query, rule)

app.add_url_rule('/update/<int:queryVersion>/<product>/<version>/<buildid>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/update.xml', view_func=ClientRequestView.as_view('clientrequest'))
# TODO: How can we make Flask serve empty XML files instead of 404s for non-matching URLs?
