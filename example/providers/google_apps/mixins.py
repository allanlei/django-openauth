from django.core.exceptions import ImproperlyConfigured

from openauth.oauth.mixins import OAuthMixin


class OpenIDMixin(OAuthMixin):
    def get_openid_discovery_endpoint(self):
        return 'https://www.google.com/accounts/o8/site-xrds?hd=%(domain)s' % {'domain': self.get_openid_domain()}
        
    def get_openid_login_endpoint(self):
        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': self.get_openid_domain()}

class GoogleOpenIDOAuthMixin(object):
    google_oauth_scopes = None

    def get_google_oauth_scopes(self):
        if self.google_oauth_scopes:
            scopes = self.google_oauth_scopes
        else:
            raise ImproperlyConfigured('Provide google_oauth_scopes or override get_google_oauth_scopes().')
        return scopes
        
    def get_openid_kwargs(self):
        kwargs = super(GoogleOpenIDOAuthMixin, self).get_openid_kwargs()
        kwargs.update({
            'openid.ns.ext2': 'http://specs.openid.net/extensions/oauth/1.0',
            'openid.ext2.consumer': self.get_oauth_consumer_key(),
            'openid.ext2.scope': ' '.join(self.get_google_oauth_scopes()),
        })
        return kwargs





    


class OAuthRequestTokenMixin(object):
    oauth_request_endpoint = 'https://www.google.com/accounts/OAuthGetRequestToken'
    google_oauth_scopes = None
    google_oauth_callback = None
    
    def get_google_oauth_callback(self):
        if self.google_oauth_callback:
            url = self.google_oauth_callback
        else:
            raise ImproperlyConfigured('Provide google_oauth_callback or override get_google_oauth_callback().')
        return url
    
    def get_google_oauth_scopes(self):
        if self.google_oauth_scopes:
            scopes = self.google_oauth_scopes
        else:
            raise ImproperlyConfigured('Provide google_oauth_scopes or override get_google_oauth_scopes().')
        return scopes
        
    def get_oauth_request_endpoint_params(self):
        params = super(OAuthRequestTokenMixin, self).get_oauth_request_endpoint_params()
        params.update({
            'scope': ' '.join(self.get_google_oauth_scopes()),
            'oauth_callback': self.get_google_oauth_callback(),
        })
        return params

class OAuthAuthorizeTokenMixin(object):
    oauth_authorization_endpoint = 'https://www.google.com/accounts/OAuthAuthorizeToken'

class OAuthAccessTokenMixin(object):
    oauth_access_endpoint = 'https://www.google.com/accounts/OAuthGetAccessToken'
