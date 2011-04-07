from django.views import generic
#from django.core.urlresolvers import reverse
#from django.conf import settings
from django.http import HttpResponseRedirect

#from forms import DomainForm

#from openid.mixins import *
#from oauth.mixins import *

from django.core.urlresolvers import reverse

from mixins import HostInfoMixin
from openid.views import *
from oauth.views import *

from django.conf import settings
import urllib

import hmac
import hashlib
import base64

class CustomSignatureMixin(object):
    def get_custom_signature(self):
        secret = settings.SECRET_KEY
        message = self.request.META['REMOTE_ADDR']
        
        dig = hmac.new(bytes(secret), msg=message, digestmod=hashlib.sha256).digest()
        return base64.b64encode(dig).decode()


class GoogleEndpointsMixin(object):
    oauth_access_endpoint = 'https://www.google.com/accounts/OAuthGetAccessToken'
    oauth_authorization_endpoint = 'https://www.google.com/accounts/OAuthAuthorizeToken'

class OpenIDLoginView(
        OpenIDAttributeExchangeMixin, 
        OpenIDLoginMixin,
        generic.base.TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_openid_login_url())
        
    openid_ax = [
        'openid.ax.type.email', 
        'openid.ax.type.firstname', 
        'openid.ax.type.lastname', 
        'openid.ax.type.language', 
        'openid.ax.type.country',
    ]
    
    def get_openid_realm(self):
        return '%s://%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host())
        
    def get_openid_endpoint(self):
        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': 'helveticode.com'}
        
    def get_openid_callback_url(self):
        return self.get_openid_realm() + reverse('openid_callback')


class OpenIDLoginCallbackView(OpenIDLoginCallbackMixin, generic.base.View):        
    def get(self, request, *args, **kwargs):
        if self.is_valid_openid_response():
            print 'VALID'
            return
        print 'INVALID'
        return


















class OpenIDOAuthHybridLoginView(
        OpenIDAttributeExchangeMixin, 
        OAuthAuthorizedTokenMixin,
        OAuthMixin,
        OpenIDLoginMixin,
        generic.base.TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_openid_login_url())
        
    openid_ax = [
        'openid.ax.type.email', 
        'openid.ax.type.firstname', 
        'openid.ax.type.lastname', 
        'openid.ax.type.language', 
        'openid.ax.type.country',
    ]
    
    oauth_consumer_key = settings.CONSUMER_KEY
    oauth_scopes = ['http://docs.google.com/feeds/']
    
    def get_openid_realm(self):
        return '%s://%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host())
        
    def get_openid_endpoint(self):
        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': 'helveticode.com'}
        
    def get_openid_callback_url(self):
        return self.get_openid_realm() + reverse('hybrid_callback')



class OpenIDOAuthHyrbidLoginCallbackView(
        GoogleEndpointsMixin,
        OpenIDAttributeExchangeMixin,  
        OpenIDLoginCallbackMixin, 
        OAuthAuthorizedTokenMixin,
        OAuthAccessTokenMixin,
        OAuthMixin,
        generic.base.View):
    
    oauth_consumer_key = settings.CONSUMER_KEY
    oauth_secret_key = settings.CONSUMER_SECRET
    oauth_scopes = ['http://docs.google.com/feeds/']
    

    def get_token_key(self):
        return self.request.GET['openid.ext2.request_token']
    
    def get_token_secret(self):
        return ''

    def get(self, request, *args, **kwargs):
        if self.is_valid_openid_response():
            request_token = self.get_authorized_request_token()
            if request_token:
                access_token = self.get_oauth_access_token(request_token)
                if access_token:
                    print access_token
                    return
        print 'INVALID'
        return






















class OAuthLoginView(
        GoogleEndpointsMixin,
        OAuthUnauthorizedTokenMixin,
        OAuthAuthorizedTokenMixin, 
        OAuthMixin, 
        generic.base.TemplateView,
        generic.base.View):
        
    template_name = 'login.html'
    oauth_consumer_key = settings.CONSUMER_KEY
    oauth_secret_key = settings.CONSUMER_SECRET
    oauth_scopes = ['http://docs.google.com/feeds/']
    
    def get_oauth_callback_url(self):
        return '%s://%s%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host(), reverse('oauth_callback'))
    
    def set_token_secret(self, token):
        self.request.session['oauth_token_secret'] = token
        
    def post(self, request, *args, **kwargs):
        request_token = self.get_unauthorized_request_token()
        if request_token:
            return HttpResponseRedirect(self.get_authorization_url(request_token))
        print 'SOMETHING WRONG'


class OAuthLoginCallbackView(OAuthAuthorizedTokenMixin, OAuthAccessTokenMixin, OAuthMixin, generic.base.View):
    oauth_consumer_key = settings.CONSUMER_KEY
    oauth_secret_key = settings.CONSUMER_SECRET
    oauth_scopes = ['http://docs.google.com/feeds/']
    oauth_access_endpoint = 'https://www.google.com/accounts/OAuthGetAccessToken'
    
    def get_token_secret(self):
        return self.request.session['oauth_token_secret']
        
    def get(self, request, *args, **kwargs):
        request_token = self.get_authorized_request_token()
        if request_token:
            access_token = self.get_oauth_access_token(request_token)
            if access_token:
                print access_token
                print 'VALID'
                return
        print 'INVALID'
        return
