class OpenIDLoginEndpointMixin(object):
    def get_openid_login_endpoint(self):
        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': self.get_openid_domain()}
        
#    def get_openid_discovery_endpoint(self):
#        return 'https://www.google.com/accounts/o8/site-xrds?hd=%(domain)s' % {'domain': self.get_openid_domain()}
        
class OpenIDHyrbridMixin(object):
    def get_oauth_token(self):
        return {
            'oauth_token': self.request.GET['openid.ext2.request_token'],
            'oauth_token_secret': '',
        }
                
    def get_openid_kwargs(self):
        kwargs = super(OpenIDHyrbridMixin, self).get_openid_kwargs()
        kwargs.update({
            'openid.ns.ext2': 'http://specs.openid.net/extensions/oauth/1.0',
            'openid.ext2.consumer': self.get_oauth_consumer_key(),
            'openid.ext2.scope': ' '.join(self.get_oauth_scopes()),
        })
        return kwargs
