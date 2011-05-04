from django.core.exceptions import ImproperlyConfigured

import gdata.auth
from gdata.client import GDClient
from atom.http import HttpClient

class OAuthMixin(object):
    oauth_token_class = gdata.auth.OAuthToken
    oauth_consumer_key = None
    oauth_consumer_secret = None
    oauth_scopes = []
    oauth_client_class = GDClient
    oauth_http_client = HttpClient
    oauth_signature_method = gdata.auth.OAuthSignatureMethod.HMAC_SHA1
    oauth_input_params = None
    oauth_callback_url = None
    oauth_version = '1.0'

    def get_oauth_token(self, **kwargs):
        if self.oauth_token_class:
            token = self.oauth_token_class(**kwargs)
        else:
            raise ImproperlyConfigured('Provide oauth_token_class or override get_oauth_token().')
        return token
        
    def get_oauth_consumer_key(self):
        if self.oauth_consumer_key:
            key = self.oauth_consumer_key
        else:
            raise ImproperlyConfigured('Provide oauth_consumer_key or override get_oauth_consumer_key().')
        return key
            
    def get_oauth_consumer_secret(self):
        if self.oauth_consumer_secret:
            key = self.oauth_consumer_secret
        else:
            raise ImproperlyConfigured('Provide oauth_consumer_secret or override get_oauth_consumer_secret().')
        return key

    def get_oauth_scopes(self):
        if self.oauth_scopes is not None:
            scopes = list(self.oauth_scopes)
        else:
            scopes = []
        if len(scopes) == 0:
             raise ImproperlyConfigured('oauth_scopes cannot be empty!')
        return scopes
    
    def get_oauth_client(self):
        return self.oauth_client_class()
        
    def get_oauth_http_client(self):
        return self.oauth_http_client()
        
    def get_oauth_signature_method(self):
        if self.oauth_signature_method:
            method = self.oauth_signature_method
        else:
            raise ImproperlyConfigured('Provide oauth_signature_method or override get_oauth_signature_method()')
        return method
    
    def get_oauth_callback_url(self):
        if self.oauth_callback_url:
            url = self.oauth_callback_url
        else:
            raise ImproperlyConfigured('Provide oauth_callback_url or override get_oauth_callback_url().')
        return url
    
    def get_oauth_input_params(self):
        if self.oauth_input_params:
            params = self.oauth_input_params
        else:
            params = gdata.auth.OAuthInputParams(
                self.get_oauth_signature_method(), 
                self.get_oauth_consumer_key(), 
                consumer_secret=self.get_oauth_consumer_secret(),
            )
        return params
        
    def get_oauth_callback(self):
        callback = self.get_oauth_callback_url()
        if not callback.startswith('http'):
            raise ImproperlyConfigured('oauth_callback_url needs to be an absolute URL.')
        return callback
        
    def get_oauth_version(self):
        return self.oauth_version




















class OAuthUnauthorizedTokenMixin(object):
    oauth_request_endpoint = None
    
    def get_oauth_request_endpoint(self):
        if self.oauth_request_endpoint:
            url = self.oauth_request_endpoint
        else:
            raise ImproperlyConfigured('Provide oauth_request_endpoint or override get_oauth_request_endpoint().')
        return url
        
    def get_oauth_request_token_url(self):
        return gdata.auth.GenerateOAuthRequestTokenUrl(
            self.get_oauth_input_params(), 
            self.get_oauth_scopes(),
            extra_parameters={
                'oauth_callback': self.get_oauth_callback(),
            }
        )
        
    def get_oauth_unauthorized_token(self):
        response = self.get_oauth_http_client().request('GET', str(self.get_oauth_request_token_url()))
        if response.status == 200:
            token = self.get_oauth_token(
                scopes=self.get_oauth_scopes(), 
                oauth_input_params=self.get_oauth_input_params()
            )
            token.set_token_string(response.read())
            return token
        
        
        
        
        
        

class OAuthAuthorizedTokenMixin(object):
    oauth_authorization_endpoint = None
    
    def get_oauth_authorization_endpoint(self):
        if self.oauth_authorization_endpoint:
            url = self.oauth_authorization_endpoint
        else:
            raise ImproperlyConfigured('Provide oauth_authorization_endpoint or override get_oauth_authorization_endpoint().')
        return url
    
    def get_oauth_authorized_token(self):
        return None
    
            return str(gdata.auth.GenerateOAuthAuthorizationUrl(
                self.get_oauth_unauthorized_token(),
                authorization_url=self.get_oauth_authorization_endpoint(),
#                scopes_param_prefix='oauth_token_scope'
            )
        )
        
class OAuthAccessTokenMixin(object):
    oauth_access_endpoint = None
    
    def get_oauth_access_endpoint(self):
        if self.oauth_access_endpoint:
            url = self.oauth_access_endpoint
        else:
            raise ImproperlyConfigured('Provide oauth_access_endpoint or override get_oauth_access_endpoint().')
        return url
    
    def get_oauth_access_token(self):
        return None

















class OAuthTokenRequestMixin(object):
    def get_oauth_request_token_url(self):
        return gdata.auth.GenerateOAuthRequestTokenUrl(
            self.get_oauth_input_params(), 
            self.get_oauth_scopes(),
            extra_parameters={
                'oauth_callback': self.get_oauth_callback(),
            }
        )
        
    def get_token(self):
        response = self.get_oauth_http_client().request('GET', str(self.get_oauth_request_token_url()))
        if response.status == 200:
            token = self.get_oauth_token(
                scopes=self.get_oauth_scopes(), 
                oauth_input_params=self.get_oauth_input_params()
            )
            token.set_token_string(response.read())
            return token
    
    def get_authorization_url(self):


class OAuthTokenResponseMixin(object):
    
    def get_oauth_verifier(self):
        return self.request.GET['oauth_verifier']

    def get_token(self):
        authorized_request_token = gdata.auth.OAuthToken(
            key=self.request.GET['oauth_token'],
            secret=self.get_token_secret(),
            scopes=self.get_oauth_scopes(),
            oauth_input_params=self.get_oauth_input_params()
        )
        
        access_token_url = gdata.auth.GenerateOAuthAccessTokenUrl(
            authorized_request_token,
            self.get_oauth_input_params(),
            access_token_url=self.get_oauth_access_endpoint(),
            oauth_version=self.get_oauth_version(),
            oauth_verifier=self.get_oauth_verifier(),
        )
        response = self.http_client.request('GET', str(access_token_url))
        if response.status == 200:
            token = gdata.auth.OAuthTokenFromHttpBody(response.read())
            token.scopes = authorized_request_token.scopes
            token.oauth_input_params = authorized_request_token.oauth_input_params
            return token







            
            
           


class OAuthAccessTokenMixin2(object):
    oauth_access_endpoint = None
    
    def get_oauth_access_endpoint(self):
        if self.oauth_access_endpoint:
            url = self.oauth_access_endpoint
        else:
            raise ImproperlyConfigured('Provide oauth_access_endpoint or override get_oauth_access_endpoint().')
        return url

    def get_oauth_verifier(self):
        return self.request.GET.get('oauth_verifier', None)
   
    def get_oauth_access_token(self, token):
        access_token_url = gdata.auth.GenerateOAuthAccessTokenUrl(
            token,
            self.get_oauth_input_params(),
            access_token_url=self.get_oauth_access_endpoint(),
            oauth_version=self.get_oauth_version(),
            oauth_verifier=self.get_oauth_verifier(),
        )
        response = self.get_oauth_http_client().request('GET', str(access_token_url))
        if response.status == 200:
            token = gdata.auth.OAuthTokenFromHttpBody(response.read())
            token.scopes = token.scopes
            token.oauth_input_params = token.oauth_input_params
            return token
