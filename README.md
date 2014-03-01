# Django Visipedia

The Django Visipedia application provides the Visipedia OAuth2 authentication, user account management and Visipedia API access for both internal and third-party applications.

Currently the repository covers especially the use for internal applications which differs from the third-party OAuth2 flow in a few ways:

1. The OAuth2 uses two-legged authentication since we don't have to (and don't want to) ask the user for permissions on the internal apps. The two-legged authentication uses shared cookie for all the applications on the `*.visipedia.co` subdomains (and works only on those).
2. Thanks to the first point the user session on all the `*.visipedia.co` is very well synchronized. That means the user is atomatically logged in/out in all the Visipedia internall applications.
3. The application provides a possibility to define a confidental API accessible only by the Visipedia server.

## Installation
You can install Django Visipedia with [PIP](http://www.pip-installer.org/):
```bash
pip install git+git://github.com/visipedia/django-visipedia
```

If you haven't done so, register your application at https://visipedia.co/settings/developer/ at first.

Add your application ID and secret to your settings:
```python
VISIPEDIA_APP_ID     = '...'
VISIPEDIA_APP_SECRET = '...'
```

Add the Visipedia OAuth2 authentication backend:
```python
AUTHENTICATION_BACKENDS = (
	'django_visipedia.backends.OAuth2Backend',
)
```

Add the Visipedia middleware class:
```python
MIDDLEWARE_CLASSES = (
	'django_visipedia.middleware.VisipediaMiddleware',
)
```

The Visipedia middleware class requires sessions and the Django Auth application and must be included **after** the `SessionMiddleware` and `AuthenticationMiddleware`.

Now, when we are using the temporary visipedia.co domain, you must add also:
```python
VISIPEDIA_API_SITE = 'https://visipedia.co'
```

## Usage

### Visipedia login
The Django Visipedia application allows you to seamlessly authenticate the users of your application over Visipedia.

To log a user in with Visipedia set any route to the  `django_visipedia.views.login` view:
```python
url(r'^login/$', 'django_visipedia.views.login'),
```

You can also redirect the user to Visipedia sign in page manually from a view. To get the Visipedia sign in URL use:
```python
from django_visipedia import visipedia

redirect_uri = '...' # URL where you want to be redirected after login (must be absolute)
visipedia.get_visipedia_signin_url(redirect_uri)
```

### Accounts
The default managing of user accounts works as follows:
* If the user has never been logged in to your app, the first login with Visipedia will create his account in your User model in Django.
* If the user already exists in your application, he will be simply logged in.

This flow lets you manage your users in any way you want. You can use any other method of authentication together with Visipedia login.

The Visipedia login's default behavior is to set the user information obtained from the Visipedia server to your User model and update the information on further authentications to keep the information synchronized with Visipedia. If you want to change the default behavior, you can write a custom **persistor** class and register it in your settings:
```python
VISIPEDIA_USER_PERSISTOR = 'my_app.persistors.UserPersistor'
```

The persistor class requires you to implement `create_user` and `update_user` methods. The default implementation looks as follows:
```python
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
```
For example if you use another authentication system, the Visipedia usernames might conflict with your app's usernames. To solve this problem you can write your own persistor class that can for instance prefix the Visipedia username with a special string (like `v:MyUsername`).

**NOTE:** The user has immutable Visipedia ID (called **vid**), but all the other properties are **editable**! The **email** field is always set but can change! The **username** field is not strictly required on Visipedia (since the users can sign in via Facebook, Google, etc.), but if the username the API will still return a value 

### API
To use the Visipedia API you can simply do:
```python
from django_visipedia import visipedia

data = visipedia.get('/me/')
```

Similarly you can use `visipedia.post('...')`, `visipedia.put('...')` and `visipedia.delete('...')`. All the request will be automatically authenticated with OAuth2 access token for the current user.

### Providing API back to Visipedia server (internal apps only)
The Django Visipedia application offers you a possibility to secure any view to let only the Visipedia server have access to it. You can do so very easily:

```python
from django_visipedia.decorators import visipedia_server_only

@visipedia_server_only
def my_api_for_visipedia_server(request):
	...
```

This functionality is implemented using the HTTP Basic Authentication ([RFC2617](http://tools.ietf.org/html/rfc2617)). Server authenticates to the client with clients ID and secret. The connection must be secured with HTTPS!
