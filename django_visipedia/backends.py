from django.contrib.auth import get_user_model
from django_visipedia import visipedia, persistor
from django_visipedia.models import VisipediaUser
from django_visipedia import VISIPEDIA_SCOPES

# compatibility for Django < 1.6
try:
	from django.db.transaction import atomic
except ImportError:
	from django.db.transaction import commit_on_success as atomic

User = get_user_model()

class OAuth2Backend(object):

	def authenticate(self, visipedia_session):

		scope = ','.join(VISIPEDIA_SCOPES)
		visipedia.get_access_token_from_visipedia_session(visipedia_session, scope=scope)

		# if the user is not found, throws VisipediaException
		# (no need to catch it since we are in the backend class)
		me = visipedia.get('/me/')
		vid = me['vid']

		# try to find the Visipedia user account
		try:
			user = User.objects.get(visipedia_user=vid)
			user = persistor.update_user(user, **me)
			user.save()

		# if the account does not exist, create it
		except User.DoesNotExist:
			user = persistor.create_user(**me)

			with atomic():
				user.save()

				visipedia_user = VisipediaUser()
				visipedia_user.vid = vid
				visipedia_user.user = user
				visipedia_user.save()

		return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
