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
        if self.oauth_secret_key:
            key = self.oauth_secret_key
        else:
            raise ImproperlyConfigured('Provide oauth_secret_key or override get_oauth_consumer_secret().')
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
                consumer_secret=self.get_oauth_secret_key(),
            )
        return params
        
    def get_oauth_callback(self):
        callback = self.get_oauth_callback_url()
        if not callback.startswith('http'):
            raise ImproperlyConfigured('oauth_callback_url needs to be an absolute URL.')
        return callback
        
    def get_oauth_version(self):
        return self.oauth_version






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
        print self.get_token()
        return 'http://www.google.com'



class OAuthTokenResponseMixin(object):
    def get_token(self):
        pass


















            
class OAuthAuthorizedTokenMixin2(object):
    oauth_authorization_endpoint = None
    oauth_token_scope_prefix = 'oauth_token_scope'
    
    def get_oauth_authorization_endpoint(self):
        if self.oauth_authorization_endpoint:
            url = self.oauth_authorization_endpoint
        else:
            raise ImproperlyConfigured('Provide oauth_authorization_endpoint or override get_oauth_authorization_endpoint()')
        return url
    
    def get_oauth_token_scope_prefix(self):
        if self.oauth_token_scope_prefix:
            prefix = self.oauth_token_scope_prefix
        else:
            raise ImproperlyConfigured('Provide oauth_token_scope_prefix or override get_oauth_token_scope_prefix()')
        return prefix
        
    def get_authorization_url(self, token):
        return str(gdata.auth.GenerateOAuthAuthorizationUrl(
            token,
            authorization_url=self.get_oauth_authorization_endpoint(),
            scopes_param_prefix=self.get_oauth_token_scope_prefix(),
        ))

    def get_token_key(self):
        return self.request.GET.get('oauth_token', None)
    
    def get_token_secret(self):
        raise ImproperlyConfigured('Implement token secret storage, Must correspond with get_token_secret()')
        
    def get_authorized_request_token(self):
        key = self.get_token_key()
        if key:
            token = gdata.auth.OAuthToken(
                key=key,
                secret=self.get_token_secret(),
                scopes=self.get_oauth_scopes(),
                oauth_input_params=self.get_oauth_input_params()
            )
            return token
            
    def get_openid_kwargs(self):
        kwargs = super(OAuthAuthorizedTokenMixin, self).get_openid_kwargs()
        if self.get_oauth_consumer_key() not in self.get_openid_realm():
            raise ImproperlyConfigured('oauth_consumer_key(%s) is different than openid_realm(%s). This key will not work.' % (self.get_oauth_consumer_key(), self.get_openid_realm()))
        kwargs.update({
            'openid.ns.ext2': 'http://specs.openid.net/extensions/oauth/1.0',
            'openid.ext2.consumer': self.get_oauth_consumer_key(),
            'openid.ext2.scope': ' '.join(self.get_oauth_scopes()),
        })
        return kwargs


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
