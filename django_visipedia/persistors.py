from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import AppRegistryNotReady

try:
    User = get_user_model()
except AppRegistryNotReady:
    User = settings.AUTH_USER_MODEL


class UserPersistor(object):

    @staticmethod
    def create_user(vid, email, username, first_name=None, last_name=None):
        user = User()
        user.email = email
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        return user

    @staticmethod
    def update_user(user, vid, email, username, first_name=None, last_name=None):
        user.email = email
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        return user
