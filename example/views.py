from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings

from openauth.openid.mixins import OpenIDMixin
from openauth.google.mixins import GoogleOpenIDMixin, GoogleOpenIDOAuthMixin, GoogleOAuthMixin

from openauth.oauth.mixins import *

class OpenIDView(GoogleOpenIDOAuthMixin, GoogleOpenIDMixin, OpenIDMixin, generic.base.View):
    def get_openid_domain(self):
        return self.request.POST['domain']
        
    def get_openid_realm(self):
        return '%s://%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host())
        
    def get_openid_return_to(self):
        return self.get_openid_realm() + reverse('openid_login')

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


class OAuthView(GoogleOAuthMixin, OAuthUnauthorizedTokenMixin, OAuthAuthorizedTokenMixin, OAuthAccessTokenMixin, OAuthMixin, generic.base.View):
    oauth_consumer_key = settings.OAUTH_CONSUMER_KEY
    oauth_consumer_secret = settings.OAUTH_CONSUMER_SECRET
    oauth_scopes = settings.OAUTH_SCOPES
    
    def get_oauth_callback_url(self):
        return '%s://%s%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host(), reverse('oauth_login'))
        
    def post(self, *args, **kwargs):
        return HttpResponseRedirect(self.get_authorization_url())
    
    def get(self, *args, **kwargs):
        if 'oauth_verifier' in self.request.GET:
            print self.request.GET['oauth_verifier']
        return HttpResponseRedirect('/')
