import simplejson as json

from flask import request, Response, jsonify
from flask.views import MethodView

from buildtools.retry import retry

from auslib.blob import ReleaseBlobV1, CURRENT_SCHEMA_VERSION
from auslib.db import OutdatedDataError
from auslib.web.base import app, db
from auslib.web.views.base import requirelogin, requirepermission

import logging
log = logging.getLogger(__name__)

class SingleLocaleView(MethodView):
    """/releases/[release]/builds/[platform]/[locale]"""
    def get(self, release, platform, locale):
        locale = db.releases.getLocale(release, platform, locale)
        return jsonify(locale)

    @requirelogin
    @requirepermission()
    def put(self, release, platform, locale, changed_by):
        try:
            # Collect all of the release names that we should put the data into
            releases = [release]
            releases.extend(json.loads(request.form.get('copyTo', '[]')))
            # XXX: what do we do with product and version when the release already exists,
            #      but they don't match? update them? maybe we should require the client
            #      to create the release via a separate method?
            product = request.form['product']
            version = request.form['version']
            existed = False
            for rel in releases:
                # If the release doesn't exist, create it.
                if not db.releases.getReleases(name=rel):
                    releaseBlob = ReleaseBlobV1(name=rel, schema_version=CURRENT_SCHEMA_VERSION)
                    db.releases.addRelease(rel, product, version, releaseBlob, changed_by)
                # If it does exist, and this is this is the first release (aka, the one in the URL),
                # see if the locale exists, for purposes of setting the correct Response code.
                elif rel == release:
                    try:
                        db.releases.getLocale(rel, platform, locale)
                        existed = True
                    except:
                        pass
                localeBlob = json.loads(request.form['details'])
                # We need to wrap this in order to make it retry-able.
                def updateLocale():
                    old_data_version = db.releases.getReleases(name=rel)[0]['data_version']
                    log.debug("SingleLocaleView.put: old_data_version is %s" % old_data_version)
                    db.releases.addLocaleToRelease(rel, platform, locale, localeBlob, old_data_version, changed_by)
                retry(updateLocale, sleeptime=0, retry_exceptions=(OutdatedDataError,))
            if existed:
                return Response(status=200)
            else:
                return Response(status=201)
        except (KeyError, json.JSONDecodeError), e:
            return Response(status=400, response=e.message)
        except Exception, e:
            return Response(status=500, response=e.message)

app.add_url_rule('/releases/<release>/builds/<platform>/<locale>', view_func=SingleLocaleView.as_view('single_locale'))
