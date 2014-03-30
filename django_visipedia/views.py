from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_visipedia import visipedia

def login(request):

	if request.user.is_authenticated():
		return redirect(getattr(settings, 'LOGIN_REDIRECT_URL', '/'))
	else:
		next = request.GET.get('next', '')
		uri = request.build_absolute_uri('/').rstrip('/') + next
		return redirect(visipedia.get_visipedia_signin_url(uri))

def logout(request):

	if request.user.is_authenticated():
		return redirect(visipedia.get_visipedia_signout_url())
	else:
		return redirect(visipedia.site)
		
