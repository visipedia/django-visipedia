import base64
import os
import requests
from requests.compat import json
from urllib import quote, urlencode

# TODO:
#  - redirect URI (better handling)
#  - check base64 encoding variant with OAuth2 RFC
#  - maybe split to Base, Visipedia and InnerApi classes
#  - any point using requests.Session() ?

class Visipedia(object):

	site = 'https://visipedia.org'
	authorization_url = '/auth/oauth2/authorize/'
	access_token_url = '/auth/oauth2/token/'
	visipedia_signin_url = '/signin/'
	certificate = os.path.dirname(os.path.abspath(__file__)) + '/visipedia.crt'

	client_id = None
	client_secret = None

	def __init__(self, client_id, client_secret, site=None, persistent_storage=None):

		self.client_id = client_id
		self.client_secret = client_secret
		if site is not None:
			self.site = site
		self.persistent_storage = persistent_storage

	def get_authorization_url(self, redirect_uri=None, scope=None, state=None):

		params = {
			'response_type': 'code',
			'client_id': self.client_id,
		}

		if redirect_uri:
			params['redirect_uri'] = redirect_uri
		if scope:
			params['scope'] = scope
		if state:
			params['state'] = state

		return "%s%s?%s" % (self.site, quote(self.authorization_url), urlencode(params))

	def get_access_token_from_code(self, code, redirect_uri=None):

		data = {
			'grant_type': 'authorization_code',
			'client_id': self.client_id,
			'client_secret': self.client_secret,
			'code': code,
		}

		if redirect_uri:
			data['redirect_uri'] = redirect_uri

		data = self._request('POST', '%s' % quote(self.access_token_url), data=data)

		self._add_persistent_data(result)
		return data

	def get_access_token_from_visipedia_session(self, visipedia_session):

		data = {
			'grant_type': 'password',
			'username' : 'visipedia',
			'password' : visipedia_session
		}

		auth_token = '%s:%s' % (self.client_id, self.client_secret)
		headers = {'Authorization': 'Basic %s' % base64.b64encode(auth_token)}

		result = self._request('POST', '%s' % self.access_token_url, headers=headers, data=data)
		self._add_persistent_data(result)
		return result

	def get_visipedia_signin_url(self, redirect_uri=None):

		params = {}
		if redirect_uri:
			params['next'] = redirect_uri

		return "%s%s?%s" % (self.site, quote(self.visipedia_signin_url), urlencode(params))

	def api(self, method, path, params={}):

		headers = {'Authorization': 'Bearer %s' % self._get_persistent_data('access_token')}

		path = '/api%s' % path
		if method == 'GET':
			return self._request('GET', path, headers, params)
		else:
			try:
				data = json.dumps(data)
			except Exception:
				raise VisipediaException('Invalid request format')
			return self._request(method, path, headers, data=data)

	def get(self, path, params={}):
		return self.api('GET', path, params)

	def post(self, path, params={}):
		return self.api('POST', path, params)

	def put(self, path, params={}):
		return self.api('PUT', path, params)

	def delete(self, path, params={}):
		return self.api('DELETE', path, params)

	def _request(self, method, path, headers={}, params={}, data={}):

		try:
			response = requests.request(
				method, "%s%s" % (self.site, quote(path)),
				headers=headers,
				params=params,
				data=data,
				verify=self.certificate
			)
		except requests.exceptions.RequestException, e:
			raise VisipediaException(e)

		# handle HTTP error codes
		if response.status_code != requests.codes.ok:
			try:
				info = response.json()
			except Exception:
				info = 'Unknown error, server returned code %s' % response.status_code
			raise VisipediaException(info)

		try:
			return response.json()
		except Exception:
			raise VisipediaException('Invalid response from the server')

	def _set_persistent_data(self, key, value):
		if self.persistent_storage is not None:
			self.persistent_storage.set(key, value)

	def _get_persistent_data(self, key):
		if self.persistent_storage is not None:
			return self.persistent_storage.get(key)
		else:
			return None

	def _add_persistent_data(self, data):
		for k, v in data.items():
			self._set_persistent_data(k, v)

class VisipediaException(Exception):

	def __init__(self, raw):

		self.raw = raw

		try:
			self.error = raw['error']
		except Exception:
			self.error = ''

		# a temporary solution until the server provides better error messages
		fix = {
			'invalid_client' : 'Invalid client',
			'unsupported_grant_type' : 'Unsupported grant type'
		}
		if isinstance(raw, dict) and 'error' in raw and not 'error_description' in raw \
			and raw['error'] in fix:
			raw['error_description'] = fix[raw['error']]

		# OAuth 2.0 RFC6749 style
		try:
			self.error_description = raw["error_description"]
		except Exception:
			self.error_description = raw

		Exception.__init__(self, self.error_description)
