from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings

from openauth.openid.mixins import *
from openauth.oauth.mixins import *

import mixins
from mixins import OpenIDMixin as GoogleOpenIDMixin
from mixins import OAuthRequestTokenMixin as GoogleOAuthRequestTokenMixin
from mixins import OAuthAuthorizeTokenMixin as GoogleOAuthAuthorizeTokenMixin
from mixins import OAuthAccessTokenMixin as GoogleOAuthAccessTokenMixin


OAUTH_CONSUMER_KEY = ''
OAUTH_CONSUMER_SECRET =''

consumer = oauth.Consumer(OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET)

class OpenIDView(GoogleOpenIDMixin, OpenIDMixin, generic.base.View):
    def get_openid_domain(self):
        return self.request.POST['domain']
        
    def get_openid_realm(self):
        return '%s://%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host())
        
    def get_openid_return_to(self):
        return self.get_openid_realm() + reverse('openid:google_apps')

    def get(self, *args, **kwargs):
        if 'openid.mode' in self.request.GET:
            user = authenticate(return_to=self.get_openid_return_to(), openid=dict(self.request.GET.items()))
            if user:
                login(self.request, user)
                messages.success(self.request, 'Logged In as %s!' % user)
            else:
                messages.warning(self.request, 'OpenID log in successful, but Django login failed')
            return HttpResponseRedirect('/')
        
    def post(self, *args, **kwargs):
        return HttpResponseRedirect(self.get_openid_login_url())
        

class HybridOpenIDView(
        mixins.GoogleOpenIDOAuthMixin, 
        GoogleOpenIDMixin, 
        GoogleOAuthAccessTokenMixin,
        OpenIDMixin, 
        OAuthAccessTokenMixin, 
        generic.base.View):
        
    oauth_consumer_key = OAUTH_CONSUMER_KEY
    oauth_consumer_secret = OAUTH_CONSUMER_SECRET
    oauth_consumer = consumer
    
    google_oauth_scopes = ['http://docs.google.com/feeds/', 'http://www.google.com/calendar/feeds/', 'http://www.google.com/m8/feeds']
    
    def get_openid_domain(self):
        return self.request.POST['domain']
        
    def get_openid_realm(self):
        return '%s://%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host())
        
    def get_openid_return_to(self):
        return self.get_openid_realm() + reverse('openid:google_apps')

    def get(self, *args, **kwargs):
        if 'openid.mode' in self.request.GET:
            user = authenticate(return_to=self.get_openid_return_to(), openid=dict(self.request.GET.items()))
            if user:
                login(self.request, user)
                print self.get_oauth_access_token()
                messages.success(self.request, 'Logged In as %s!' % user)
            else:
                messages.warning(self.request, 'OpenID log in successful, but Django login failed')
            return HttpResponseRedirect('/')
        
    def post(self, *args, **kwargs):
        return HttpResponseRedirect(self.get_openid_login_url())

    def get_oauth_token(self):
        return {
            'oauth_token': self.request.GET['openid.ext1.request_token'],
            'oauth_token_secret': '',
        }




class OAuthView(
        GoogleOAuthRequestTokenMixin, 
        GoogleOAuthAuthorizeTokenMixin, 
        GoogleOAuthAccessTokenMixin, 
        OAuthRequestTokenMixin, 
        OAuthAuthorizeTokenMixin, 
        OAuthAccessTokenMixin, 
        OAuthMixin, 
        generic.base.View):
        
    oauth_consumer_key = OAUTH_CONSUMER_KEY
    oauth_consumer_secret = OAUTH_CONSUMER_SECRET
    oauth_consumer = consumer
    
    google_oauth_scopes = ['http://docs.google.com/feeds/', 'http://www.google.com/calendar/feeds/', 'http://www.google.com/m8/feeds']
    google_oauth_callback = 'http://dev.app.rhinoaccounting.com/oauth/googleapps/'
    
    def post(self, *args, **kwargs):
        return HttpResponseRedirect(self.get_oauth_authorization_url())
    
    def get(self, *args, **kwargs):
        if 'oauth_verifier' in self.request.GET and 'oauth_token' in self.request.GET:
            messages.success(self.request, self.get_oauth_access_token())
        return HttpResponseRedirect('/')
