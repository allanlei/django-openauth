class OAuthRequestTokenMixin(object):
    oauth_request_endpoint = 'https://www.google.com/accounts/OAuthGetRequestToken'
    oauth_callback = None
    
    def get_oauth_callback(self):
        if self.oauth_callback:
            url = self.oauth_callback
        else:
            raise ImproperlyConfigured('Provide oauth_callback or override get_oauth_callback().')
        return url
        
    def get_oauth_request_endpoint_params(self):
        params = super(OAuthRequestTokenMixin, self).get_oauth_request_endpoint_params()
        params.update({
            'scope': ' '.join(self.get_oauth_scopes()),
            'oauth_callback': self.get_oauth_callback(),
        })
        return params

class OAuthAuthorizeTokenMixin(object):
    oauth_authorization_endpoint = 'https://www.google.com/accounts/OAuthAuthorizeToken'

class OAuthAccessTokenMixin(object):
    oauth_access_endpoint = 'https://www.google.com/accounts/OAuthGetAccessToken'
