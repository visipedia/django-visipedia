from django.contrib.auth import get_user_model

User = get_user_model()

class UserPersistor(object):

	def create_user(self, vid, email, username, first_name=None, last_name=None):
		user = User()
		user.email = email
		user.username = username
		user.first_name = first_name
		user.last_name = last_name
		return user

	def update_user(self, user, vid, email, username, first_name=None, last_name=None):
		user.email = email
		user.username = username
		user.first_name = first_name
		user.last_name = last_name
		return user
