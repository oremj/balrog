import simplejson as json

from flask import request, Response, jsonify
from flask.views import MethodView

from auslib.blob import ReleaseBlobV1, CURRENT_SCHEMA_VERSION
from auslib.web.base import app, db
from auslib.web.views.base import requirelogin

class SingleLocaleView(MethodView):
    """/releases/[release]/builds/[platform]/[locale]"""
    def get(self, release, platform, build):
        build = db.releases.getLocale(release, platform, build)
        return jsonify(build)

    @requirelogin
    def put(self, release, platform, build, changed_by):
        try:
            product = request.form['product']
            version = request.form['version']
            if not db.releases.getReleases(name=release):
                releaseBlob = ReleaseBlobV1(name=release, schema_version=CURRENT_SCHEMA_VERSION)
                db.releases.addRelease(release, product, version, releaseBlob, changed_by)
                existed = False
            else:
                try:
                    db.releases.getLocale(release, platform, build)
                    existed = True
                except:
                    existed = False
            buildBlob = json.loads(request.form['details'])
            old_data_version = db.releases.getReleases(name=release)[0]['data_version']
            db.releases.addLocaleToRelease(release, platform, build, buildBlob, old_data_version, changed_by)
            if existed:
                return Response(status=200)
            else:
                return Response(status=201)
        except (KeyError, json.JSONDecodeError), e:
            return Response(status=400, response=e.message)
        except Exception, e:
            return Response(status=500, response=e.message)

app.add_url_rule('/releases/<release>/builds/<platform>/<build>', view_func=SingleLocaleView.as_view('single_build'))
