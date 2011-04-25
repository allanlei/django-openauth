from auth.oauth.mixins import OAuthMixin

class GoogleOpenIDMixin(OAuthMixin):
    google_openid_oauth = False
    
    def get_openid_discovery_endpoint(self):
        return 'https://www.google.com/accounts/o8/site-xrds?hd=%(domain)s' % {'domain': self.get_openid_domain()}
        
    def get_openid_login_endpoint(self):
        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': self.get_openid_domain()}
        
    def get_openid_kwargs(self):
        kwargs = super(GoogleOpenIDMixin, self).get_openid_kwargs()
        if self.google_openid_oauth:
            kwargs.update({
                'openid.ns.ext2': 'http://specs.openid.net/extensions/oauth/1.0',
                'openid.ext2.consumer': self.get_oauth_consumer_key(),
                'openid.ext2.scope': ' '.join(self.get_oauth_scopes()),
            })
        return kwargs
