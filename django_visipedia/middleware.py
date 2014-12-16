from django_visipedia import visipedia, PersistentStorage
from django_visipedia.models import VisipediaUser
from django.contrib.auth import authenticate, login, logout


class VisipediaMiddleware(object):

    @staticmethod
    def process_request(request):
        assert hasattr(request,
                       'session'), "The Visipedia authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        if request.path.endswith('.jpg'):
            return

        visipedia.persistent_storage = PersistentStorage(request.session)

        cookie = request.COOKIES.get('visipedia_session', None)
        if cookie is None:
            # user is not logged in to Visipedia, log her out
            # but only if she has the Visipedia account
            if request.user.is_authenticated():
                try:
                    request.user.visipedia_user
                    logout(request)
                except VisipediaUser.DoesNotExist:
                    pass
        else:
            # somebody is logged in to Visipedia, but not the same user is logged in here
            if request.user.is_authenticated() and cookie != request.session.get('visipedia_session', None):
                logout(request)

            # the visipedia_cookie exists - somebody should be authenticated
            if not request.user.is_authenticated():
                user = authenticate(visipedia_session=cookie)

                # ignoring unsucessful authentication (bad visipedia cookie, etc.)
                # TODO: is it really the best solution? (will send us to sign-in screen even when signed in)
                if user is not None:
                    login(request, user)
                request.session['visipedia_session'] = cookie
