from functools import wraps

from flask import request, Response

def requirelogin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        username = request.headers.get('X-Remote-User')
        if not username:
            return Response(status=401)
        return f(*args, changed_by=username, **kwargs)
    return decorated
