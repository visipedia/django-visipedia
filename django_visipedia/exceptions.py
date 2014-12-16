class VisipediaException(Exception):
    def __init__(self, raw):

        self.raw = raw

        try:
            self.error = raw['error']
        except Exception:
            self.error = ''

        # a temporary solution until the server provides better error messages
        fix = {
            'invalid_client': 'Invalid client',
            'unsupported_grant_type': 'Unsupported grant type'
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
