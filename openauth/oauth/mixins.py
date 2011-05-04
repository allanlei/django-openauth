from django.core.exceptions import ImproperlyConfigured

import oauth2 as oauth
import cgi
import time
import urllib


class OAuthMixin(object):
    oauth_consumer_class = oauth.Consumer
    oauth_client_class = oauth.Client
    oauth_consumer_key = None
    oauth_consumer_secret = None
    oauth_signature_method = oauth.SignatureMethod_HMAC_SHA1
    oauth_version = '1.0'
    
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
    
    def get_oauth_consumer(self):
        return self.get_oauth_consumer_class()(**self.get_oauth_consumer_kwargs())
    
    def get_oauth_consumer_class(self):
        if self.oauth_consumer_class:
            consumer = self.oauth_consumer_class
        else:
            raise ImproperlyConfigured('Provide oauth_consumer_class or override get_oauth_consumer_class().')
        return consumer
    
    def get_oauth_consumer_kwargs(self):
        return {
            'key': self.get_oauth_consumer_key(),
            'secret': self.get_oauth_consumer_secret(),
        }
    
    def get_oauth_client(self):
        return self.get_oauth_client_class()(**self.get_oauth_client_kwargs())
    
    def get_oauth_client_class(self):
        if self.oauth_client_class:
            client = self.oauth_client_class
        else:
            raise ImproperlyConfigured('Provide oauth_client_class or override get_oauth_client_class().')
        return client
    
    def get_oauth_client_kwargs(self):
        return {
            'consumer': self.get_oauth_consumer(),
        }
    
    def get_oauth_signature_method(self):
        if self.oauth_signature_method:
            method = self.oauth_signature_method
        else:
            raise ImproperlyConfigured('Provide oauth_signature_method or override get_oauth_signature_method().')
        return method
    
    def get_oauth_version(self):
        return self.oauth_version or '1.0'





class OAuthRequestTokenMixin(object):
    oauth_request_endpoint = None
    oauth_request_endpoint_method = 'GET'
    
    def get_oauth_request_endpoint(self):
        if self.oauth_request_endpoint:
            endpoint = self.oauth_request_endpoint
        else:
            raise ImproperlyConfigured('Provide oauth_request_endpoint or override get_oauth_request_endpoint().')
        return endpoint
    
    def get_oauth_request_endpoint_params(self):
        return {}
    
    def store_oauth_token(self, token):
        self.request.session['oauth_request_token'] = token
    
    def get_oauth_request_token(self):
        token = None
        client = self.get_oauth_client()
        url = '%s?%s' % (
            self.get_oauth_request_endpoint(), 
            urllib.urlencode(self.get_oauth_request_endpoint_params())
        )
        resp, content = client.request(url, self.oauth_request_endpoint_method)
        if resp['status'] != '200':
            raise Exception('Could not get request token from %s: HTTP %s' % (url, resp['status']))
        token = dict(cgi.parse_qsl(content))
        if 'oauth_token' not in token:
            raise Exception('Token not found: %s' % token)
        self.store_oauth_token(token)
        return token





class OAuthAuthorizeTokenMixin(object):
    oauth_authorization_endpoint = None

    def get_oauth_authorization_endpoint(self):
        if self.oauth_authorization_endpoint:
            endpoint = self.oauth_authorization_endpoint
        else:
            raise ImproperlyConfigured('Provide oauth_authorization_endpoint or override get_oauth_authorization_endpoint().')
        return endpoint
        
    def get_oauth_authorization_url(self):
        
        return '%s?%s' % (self.get_oauth_authorization_endpoint(), urllib.urlencode(self.get_oauth_authorization_url_params()))

    def get_oauth_authorization_url_params(self, oauth_token=None):
        token = self.get_oauth_request_token()
        return {
            'oauth_token': oauth_token or token['oauth_token'],
        }
        
    def get_oauth_authorized_token(self):
        return None


class OAuthAccessTokenMixin(object):
    oauth_access_endpoint = None

    def get_oauth_access_endpoint(self):
        if self.oauth_access_endpoint:
            endpoint = self.oauth_access_endpoint
        else:
            raise ImproperlyConfigured('Provide oauth_access_endpoint or override get_oauth_access_endpoint().')
        return endpoint
    
    def get_oauth_access_endpoint_params(self):
        return {}
    
    def get_oauth_verifier(self):
        return self.request.GET.get('oauth_verifier', None)
    
    def get_oauth_token(self):
        return self.request.session['oauth_request_token']
        
    def get_oauth_access_token(self):
        request_token = self.get_oauth_token()
        
        token = oauth.Token(
            request_token['oauth_token'], 
            request_token['oauth_token_secret'],
        )
        token.set_verifier(self.get_oauth_verifier())
        
        client = oauth.Client(self.get_oauth_consumer(), token)
        url = '%s?%s' % (
            self.get_oauth_access_endpoint(), 
            urllib.urlencode(self.get_oauth_access_endpoint_params())
        )
        resp, content = client.request(url, 'GET')
        if resp['status'] != '200':
            raise Exception('Could not get access token from %s: HTTP %s' % (url, resp['status']))
        token = dict(cgi.parse_qsl(content))
#        if '' in token:
#            raise Exception('Token not found: %s' % token)
        return token
