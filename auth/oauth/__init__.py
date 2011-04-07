#import gdata.auth

#class OAuthMixin(object):
#    oauth_consumer_key = None
#    oauth_secret_key = None
#    oauth_scopes = []
#    oauth_client = None
#    oauth_http_client = None
#    oauth_signature_method = gdata.auth.OAuthSignatureMethod.HMAC_SHA1
#    oauth_input_params = None
#    oauth_callback_url = None
#    oauth_version = '1.0'
#    
#    def get_oauth_version(self):
#        if self.oauth_version:
#            version = self.oauth_version
#        else:
#            raise ImproperlyConfigured('Provide oauth_version or override get_oauth_version()')
#        return version
#        
#    def get_oauth_client(self):
#        if self.oauth_client is None:
#            self.oauth_client = GDClient()
#        return self.oauth_client
#        
#    def get_oauth_http_client(self):
#        if self.oauth_http_client is None:
#            self.oauth_http_client = HttpClient()
#        return self.oauth_http_client
#    
#    def get_oauth_input_params(self):
#        if self.oauth_input_params is None:
#            self.oauth_input_params = gdata.auth.OAuthInputParams(
#                self.get_oauth_signature_method(), 
#                self.get_oauth_consumer_key(), 
#                consumer_secret=self.get_oauth_secret_key(),
#            )
#        return self.oauth_input_params
#        
#    def get_oauth_consumer_key(self):
#        if self.oauth_consumer_key:
#            key = self.oauth_consumer_key
#        else:
#            raise ImproperlyConfigured("No OAuth Consumer key. Provide oauth_consumer_key.")
#        return key
#            
#    def get_oauth_secret_key(self):
#        if self.oauth_secret_key:
#            key = self.oauth_secret_key
#        else:
#            raise ImproperlyConfigured("No OAuth Secret key. Provide oauth_secret_key.")
#        return key
#    
#    def get_oauth_scopes(self):
#        if self.oauth_scopes is not None:
#            scopes = list(self.oauth_scopes)
#        else:
#            scopes = []
#        if len(scopes) == 0:
#             raise ImproperlyConfigured('oauth_scopes cannot be empty!')
#        return scopes
#    
#    def get_oauth_callback_url(self):
#        if self.oauth_callback_url:
#            url = self.oauth_callback_url
#        else:
#            raise ImproperlyConfigured('Provide oauth_callback_url or override get_callback_url()')
#        return url

#    def get_oauth_signature_method(self):
#        if self.oauth_signature_method:
#            method = self.oauth_signature_method
#        else:
#            raise ImproperlyConfigured('Provide oauth_signature_method or override get_oauth_signature_method()')
#        return method
