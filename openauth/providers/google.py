class GoogleMixin(object):
    def get_openid_login_endpoint(self):
        return 'https://www.google.com/accounts/o8/id'







#class OpenIDLoginEndpointMixin(object):
#    def get_openid_login_endpoint(self):
#        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': self.get_openid_domain()}
#        


#  
#class OpenIDHyrbridMixin(object):
#    def get_oauth_token(self):
#        return {
#            'oauth_token': self.request.GET['openid.ext2.request_token'],
#            'oauth_token_secret': '',
#        }
#                
#    def get_openid_kwargs(self):
#        kwargs = super(OpenIDHyrbridMixin, self).get_openid_kwargs()
#        kwargs.update({
#            'openid.ns.ext2': 'http://specs.openid.net/extensions/oauth/1.0',
#            'openid.ext2.consumer': self.get_oauth_consumer_key(),
#            'openid.ext2.scope': ' '.join(self.get_oauth_scopes()),
#        })
#        return kwargs



#class OAuthRequestTokenMixin(object):
#    oauth_request_endpoint = 'https://www.google.com/accounts/OAuthGetRequestToken'
#    oauth_callback = None
#    
#    def get_oauth_callback(self):
#        if self.oauth_callback:
#            url = self.oauth_callback
#        else:
#            raise ImproperlyConfigured('Provide oauth_callback or override get_oauth_callback().')
#        return url
#        
#    def get_oauth_request_endpoint_params(self):
#        params = super(OAuthRequestTokenMixin, self).get_oauth_request_endpoint_params()
#        params.update({
#            'scope': ' '.join(self.get_oauth_scopes()),
#            'oauth_callback': self.get_oauth_callback(),
#        })
#        return params

#class OAuthAuthorizeTokenMixin(object):
#    oauth_authorization_endpoint = 'https://www.google.com/accounts/OAuthAuthorizeToken'

#class OAuthAccessTokenMixin(object):
#    oauth_access_endpoint = 'https://www.google.com/accounts/OAuthGetAccessToken'
