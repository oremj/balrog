import simplejson as json

from sqlalchemy.exc import SQLAlchemyError

from flask import render_template, request, Response, jsonify
from flaskext.wtf import ValidationError

from auslib.blob import ReleaseBlobV1, CURRENT_SCHEMA_VERSION
from auslib.util.retry import retry
from auslib.web.base import app, db
from auslib.web.views.base import requirelogin, requirepermission, AdminView
from auslib.web.views.forms import ReleaseForm

import logging
log = logging.getLogger(__name__)

__all__ = ["SingleReleaseView", "SingleLocaleView", "ReleasesPageView"]

def createRelease(release, product, version, changed_by, transaction, blobInfo):
    blob = ReleaseBlobV1(schema_version=CURRENT_SCHEMA_VERSION, **blobInfo)
    retry(db.releases.addRelease, kwargs=dict(name=release, product=product, version=version, blob=blob, changed_by=changed_by, transaction=transaction))
    return retry(db.releases.getReleases, kwargs=dict(name=release, transaction=transaction))[0]

class SingleLocaleView(AdminView):
    """/releases/[release]/builds/[platform]/[locale]"""
    def get(self, release, platform, locale):
        locale = db.releases.getLocale(release, platform, locale)
        return jsonify(locale)

    @requirelogin
    @requirepermission()
    def _put(self, release, platform, locale, changed_by, transaction):
        new = True
        form = ReleaseForm()
        if not form.validate():
            return Response(status=400, response=form.errors)
        product = form.product.data
        version = form.version.data
        localeInfo = form.details.data
        copyTo = form.copyTo.data
        old_data_version = form.data_version.data

        for rel in [release] + copyTo:
            try:
                # See if the release already exists...
                releaseInfo = retry(db.releases.getReleases, kwargs=dict(name=rel, transaction=transaction))[0]
                # If the release named in the URL exists...
                if rel == release:
                    # Make sure that old_data_version is provided, because we need to verify it when updating.
                    if not old_data_version:
                        return Response(status=400, response="Release exists, data_version must be provided")
                    # And if the locale already exists for the release, make note of it so we can return the correct status code.
                    if retry(db.releases.localeExists, kwargs=dict(name=rel, platform=platform, locale=locale, transaction=transaction)):
                        new = False
                # If this isn't the release in the URL...
                else:
                    # Use the data_version we just grabbed from the db.
                    # XXX: We should probably require an old_data_version for this, too...
                    old_data_version = releaseInfo['data_version']
            except IndexError:
                # If the release doesn't already exist, create it, and set old_data_version appropriately.
                releaseInfo = createRelease(rel, product, version, changed_by, transaction, dict(name=rel))
                old_data_version = 1

            # If the product we're given doesn't match the one in the DB, panic.
            if product != releaseInfo['product']:
                return Response(status=400, response="Product name '%s' doesn't match the one on the release object ('%s') for release '%s'" % (product, releaseInfo['product'], rel))
            # But if the version doesn't match, just update it. This will be the case for nightlies
            # every time there's a version bump.
            if version != releaseInfo['version']:
                log.debug("SingleLocaleView.put: database version for %s is %s, updating it to %s", rel, releaseInfo['version'], version)
                retry(db.releases.updateRelease, kwargs=dict(name=rel, version=version, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction))
                old_data_version += 1
            # Finally, add the locale to the release, overwriting any existing mention of it.
            retry(db.releases.addLocaleToRelease, kwargs=dict(name=rel, platform=platform, locale=locale, blob=localeInfo, old_data_version=old_data_version, changed_by=changed_by, transaction=transaction))

        if new:
            return Response(status=201)
        else:
            return Response(status=200)


class ReleasesPageView(AdminView):
    """ /releases.html """
    def get(self):
        releases = db.releases.getReleases()
        return render_template('releases.html', releases=releases)

class SingleReleaseView(AdminView):
    """ /releases/[release]"""
    def get(self, release):
        release = db.releases.getReleaseBlob(release)
        return jsonify(release)

    @requirelogin
    @requirepermission()
    def _post(self, release, changed_by, transaction):
        new = True
        log.debug('in here')
        form = ReleaseForm()
        if not form.validate():
            return Response(status=400, response=form.errors)
        product = form.product.data
        version = form.version.data
        newReleaseInfo = form.details.data
        copyTo = form.copyTo.data
        old_data_version = form.data_version.data
        if db.releases.exists(name=release) and not old_data_version:
            return Response(status=400, response="Release exists, data_version must be provided")

        for rel in [release] + copyTo:
            try:
                # See if the release already exists...
                releaseInfo = retry(db.releases.getReleases, kwargs=dict(name=rel, transaction=transaction))[0]
                # If the release named in the URL exists...
                if rel == release:
                    new = False
                    # Make sure that old_data_version is provided, because we need to verify it when updating.
                    if not old_data_version:
                        return Response(status=400, response="Release exists, data_version must be provided")
                # If this isn't the release in the URL...
                else:
                    # Use the data_version we just grabbed from the db.
                    # XXX: We should probably require an old_data_version for this, too...
                    old_data_version = releaseInfo['data_version']
            except IndexError:
                # If the release doesn't already exist, create it, and that's it for this iteration!
                createRelease(rel, product, version, changed_by, transaction, newReleaseInfo)
                continue

            # If the product we're given doesn't match the one in the DB, panic.
            if product != releaseInfo['product']:
                return Response(status=400, response="Product name '%s' doesn't match the one on the release object ('%s') for release '%s'" % (product, releaseInfo['product'], rel))
            # But if the version doesn't match, just update it. This will be the case for nightlies
            # every time there's a version bump.
            if version != releaseInfo['version']:
                log.debug("SingleLocaleView.put: database version for %s is %s, updating it to %s", rel, releaseInfo['version'], version)
                retry(db.releases.updateRelease, kwargs=dict(name=rel, version=version, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction))
                old_data_version += 1
            releaseInfo['data'].update(newReleaseInfo)
            retry(db.releases.updateRelease, kwargs=dict(name=rel, blob=releaseInfo['data'], changed_by=changed_by, old_data_version=old_data_version, transaction=transaction))

        if new:
            return Response(status=201)
        else:
            return Response(status=200)


app.add_url_rule('/releases/<release>/builds/<platform>/<locale>', view_func=SingleLocaleView.as_view('single_locale'))
app.add_url_rule('/releases/<release>', view_func=SingleReleaseView.as_view('release'))
app.add_url_rule('/releases.html', view_func=ReleasesPageView.as_view('releases.html'))
