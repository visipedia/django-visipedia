import base64
from django.http import HttpResponse
from django_visipedia import VISIPEDIA_APP_ID, VISIPEDIA_APP_SECRET
from functools import wraps

try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import json


def _basic_auth(request):
    auth = request.META.get('HTTP_AUTHORIZATION', None)
    if not auth:
        return False
    auth_type, auth_string = auth.split(' ')
    if auth_type != 'Basic' or not auth_string:
        return False

    encoding = request.encoding or 'utf-8'  # TODO: how in Django?

    auth_string_decoded = base64.b64decode(auth_string).decode(encoding)
    client_id, client_secret = auth_string_decoded.split(':', 1)

    if not VISIPEDIA_APP_ID or VISIPEDIA_APP_ID != client_id:
        return False

    if not VISIPEDIA_APP_SECRET or VISIPEDIA_APP_SECRET != client_secret:
        return False

    return True


def visipedia_server_only(func):
    def decorator(request, *args, **kwargs):
        if not _basic_auth(request):
            return HttpResponse(json.dumps({'error': 'access_denied'}), 'application/json', 403)
        return func(request, *args, **kwargs)

    return wraps(func)(decorator)
