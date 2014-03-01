from django.conf import settings
from django_visipedia.visipedia import Visipedia

from importlib import import_module
from django.core.exceptions import ImproperlyConfigured

try:
    from django.utils import six
except ImportError:
    import six

# utils
def load_class(path):

	try:
		mod_name, cls_name = path.rsplit('.', 1)
		mod = import_module(mod_name)
	except AttributeError as e:
		raise ImproperlyConfigured('Error importing {0}: "{1}"'.format(mod_name, e))

	try:
		cls = getattr(mod, cls_name)
	except AttributeError:
		raise ImproperlyConfigured('Module "{0}" does not define a "{1}" class'.format(mod_name, cls_name))

	return cls

# default session persistor
from django_visipedia.persistors import UserPersistor

class PersistentStorage():

	def __init__(self, session):
		self.session = session

	def get(self, key):
		return self.session.get('visipedia_%s' % key, None)

	def set(self, key, value):
		self.session['visipedia_%s' % key] = value

# settings
VISIPEDIA_APP_ID = getattr(settings, 'VISIPEDIA_APP_ID', None)
VISIPEDIA_APP_SECRET = getattr(settings, 'VISIPEDIA_APP_SECRET', None)
VISIPEDIA_API_SITE = getattr(settings, 'VISIPEDIA_API_SITE', 'https://visipedia.org')
VISIPEDIA_USER_PERSISTOR = getattr(settings, 'VISIPEDIA_USER_PERSISTOR', 'django_visipedia.persistors.UserPersistor')
VISIPEDIA_USER_PERSISTOR_SETTINGS = getattr(settings, 'VISIPEDIA_USER_PERSISTOR_SETTINGS', {})
VISIPEDIA_SCOPES = getattr(settings, 'VISIPEDIA_SCOPES', [])

visipedia = Visipedia(VISIPEDIA_APP_ID, VISIPEDIA_APP_SECRET, site=VISIPEDIA_API_SITE)

if isinstance(VISIPEDIA_USER_PERSISTOR, six.string_types):
	cls = load_class(VISIPEDIA_USER_PERSISTOR)
	persistor = cls(**VISIPEDIA_USER_PERSISTOR_SETTINGS)
else:
	persistor = VISIPEDIA_USER_PERSISTOR
