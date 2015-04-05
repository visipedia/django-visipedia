from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.core.exceptions import AppRegistryNotReady


try:
    User = get_user_model()
except AppRegistryNotReady:
    User = settings.AUTH_USER_MODEL


class VisipediaUser(models.Model):
    vid = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, related_name='visipedia_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# TODO: unique_together?
