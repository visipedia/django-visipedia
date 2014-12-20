from django.conf import settings
from django.shortcuts import redirect
from django_visipedia import client


def login(request):
    if request.user.is_authenticated():
        return redirect(getattr(settings, 'LOGIN_REDIRECT_URL', '/'))
    else:
        next_page = request.GET.get('next', '')
        uri = request.build_absolute_uri('/').rstrip('/') + next_page
        return redirect(client.get_visipedia_signin_url(uri))


def logout(request):
    if request.user.is_authenticated():
        return redirect(client.get_visipedia_signout_url())
    else:
        return redirect(client.site)

