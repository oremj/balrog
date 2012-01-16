import simplejson as json

from flask import render_template, request, Response, jsonify
from flask.views import MethodView

from auslib.web.base import app, db
from auslib.web.views.base import requirelogin, requirepermission
from auslib.web.views.forms import PermissionForm, ExistingPermissionForm

import logging
log = logging.getLogger(__name__)

def setpermission(f):
    def decorated(*args, **kwargs):
        if kwargs['permission'] != 'admin' and not kwargs['permission'].startswith('/'):
            kwargs['permission'] = '/%s' % kwargs['permission']
        return f(*args, **kwargs)
    return decorated
        
class UsersView(MethodView):
    """/users"""
    def get(self):
        users = db.permissions.getAllUsers()
        fmt = request.form.get('format')
        if fmt == 'json':
            # We don't return a plain jsonify'ed list here because of:
            # http://flask.pocoo.org/docs/security/#json-security
            return jsonify(dict(users=users))
        else:
            return render_template('snippets/users.html', users=users)

class PermissionsView(MethodView):
    """/users/[user]/permissions"""
    def get(self, username):
        permissions = db.permissions.getUserPermissions(username)
        fmt = request.form.get('format', 'html')
        if fmt == 'json':
            return jsonify(permissions)
        else:
            forms = []
            for perm, values in permissions.items():
                perm = perm.lstrip('/')
                forms.append(ExistingPermissionForm(permission=perm, options=values['options'], data_version=values['data_version']))
            return render_template('snippets/user_permissions.html', username=username, forms=forms)

class SpecificPermissionView(MethodView):
    """/users/[user]/permissions/[permission]"""
    def get(self, username, permission):
        perm = db.permissions.getUserPermissions(username)[permission]
        fmt = request.form.get('format', 'html')
        if fmt == 'json':
            return jsonify(perm)
        else:
            if permission == 'new':
                form = PermissionForm(permission='')
            else:
                form = ExistingPermissionForm(permission=permission, options=perm['options'], data_version=perm['data_version'])
            return render_template('snippets/permission.html', form=form)

    @setpermission
    @requirelogin
    @requirepermission(options=[])
    def put(self, username, permission, changed_by):
        try:
            form = PermissionForm()
            options = form.options
            if db.permissions.getUserPermissions(username).get(permission):
                # Raises ValueError if it can't convert the data, which (properly)
                # causes us to return 400 below.
                data_version = form.options.data_version
                db.permissions.updatePermission(changed_by, username, permission, data_version, options)
                return Response(status=200)
            else:
                db.permissions.grantPermission(changed_by, username, permission, options)
                return Response(status=201)
        except ValueError, e:
            return Response(status=400, response=e.args)
        except Exception, e:
            return Response(status=500, response=e.args)

    @setpermission
    @requirelogin
    @requirepermission(options=[])
    def post(self, username, permission, changed_by):
        if not db.permissions.getUserPermissions(username).get(permission):
            return Response(status=404)
        try:
            form = PermissionForm()
            options = form.options.data
            data_version = form.data_version.data
            db.permissions.updatePermission(changed_by, username, permission, data_version, options)
            return Response(status=200)
        except ValueError, e:
            return Response(status=400, response=e.args)
        except Exception, e:
            return Response(status=500, response=e.args)

    @setpermission
    @requirelogin
    @requirepermission(options=[])
    def delete(self, username, permission, changed_by):
        if not db.permissions.getUserPermissions(username).get(permission):
            return Response(status=404)
        try:
            data_version = int(request.args['data_version'])
            db.permissions.revokePermission(changed_by, username, permission, data_version)
            return Response(status=200)
        except ValueError, e:
            return Response(status=400, response=e.args)
        except Exception, e:
            return Response(status=500, response=e.args)

class PermissionsPageView(MethodView):
    """/permissions.html"""
    def get(self):
        users = db.permissions.getAllUsers()
        return render_template('permissions.html', users=users)

class UserPermissionsPageView(MethodView):
    """/user_permissions.html"""
    def get(self):
        username = request.args.get('username')
        if not username:
            return Response(status=404)
        permissions = db.permissions.getUserPermissions(username)
        return render_template('user_permissions.html', username=username, permissions=permissions)

app.add_url_rule('/users', view_func=UsersView.as_view('users'))
app.add_url_rule('/users/<username>/permissions', view_func=PermissionsView.as_view('permissions'))
app.add_url_rule('/users/<username>/permissions/<path:permission>', view_func=SpecificPermissionView.as_view('specific_permission'))
app.add_url_rule('/permissions.html', view_func=PermissionsPageView.as_view('permissions.html'))
app.add_url_rule('/user_permissions.html', view_func=UserPermissionsPageView.as_view('user_permissions.html'))
