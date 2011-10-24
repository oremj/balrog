from functools import wraps

from flask import request, Response

from auslib.web.base import db

# TODO: check_auth and authenticate probably need to be completely reworked
# for deployment into production -- where the web server should be doing the
# authentication. In that scenario, we should only need to look for REMOTE_USER.
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'bill' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requirelogin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, changed_by=auth.username, **kwargs)
    return decorated

def requirepermission(f, options=['product']):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            username = request.authorization.username
            url = request.path
            method = request.method
            extra = dict()
            for opt in options:
                extra[opt] = request.form[opt]
            if not db.permissions.hasUrlPermission(username, url, method, urlOptions=extra):
                return Response(status=401,
                    response="%s is not allowed to access %s by %s" % (username, url, method))
            return f(*args, **kwargs)
        except KeyError:
            return Response(status=400, response="Couldn't find 'product' in form")
    return decorated

