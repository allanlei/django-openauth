from openauth.oauth.mixins import OAuthMixin

class GoogleOpenIDMixin(OAuthMixin):
    def get_openid_discovery_endpoint(self):
        return 'https://www.google.com/accounts/o8/site-xrds?hd=%(domain)s' % {'domain': self.get_openid_domain()}
        
    def get_openid_login_endpoint(self):
        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': self.get_openid_domain()}

class GoogleOpenIDOAuthMixin(object):
    def get_openid_kwargs(self):
        kwargs = super(GoogleOpenIDOAuthMixin, self).get_openid_kwargs()
        kwargs.update({
            'openid.ns.ext2': 'http://specs.openid.net/extensions/oauth/1.0',
            'openid.ext2.consumer': self.get_oauth_consumer_key(),
            'openid.ext2.scope': ' '.join(self.get_oauth_scopes()),
        })
        return kwargs



class GoogleOAuthMixin(object):
    oauth_request_endpoint = 'https://www.google.com/accounts/OAuthGetRequestToken'
    oauth_authorization_endpoint = 'https://www.google.com/accounts/OAuthAuthorizeToken'
    oauth_access_endpoint = 'https://www.google.com/accounts/OAuthGetAccessToken'
