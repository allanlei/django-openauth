from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings

from openauth.openid.mixins import OpenIDMixin
from openauth.oauth.mixins import OAuthMixin, OAuthRequestTokenMixin, OAuthAuthorizeTokenMixin, OAuthAccessTokenMixin

import mixins


class GoogleOpenIDView(mixins.OpenIDMixin, OpenIDMixin, generic.base.View):
    def post(self, *args, **kwargs):
        return HttpResponseRedirect(self.get_openid_login_url())
        

class OpenIDOAuthHybridView(
        mixins.GoogleOpenIDOAuthMixin,
        mixins.OpenIDMixin, 
        mixins.OAuthAccessTokenMixin,
        OpenIDMixin, 
        OAuthAccessTokenMixin, 
        generic.base.View):

    def get_oauth_token(self):
        return {
            'oauth_token': self.request.GET['openid.ext1.request_token'],
            'oauth_token_secret': '',
        }

class OAuthView(
        mixins.OAuthRequestTokenMixin, 
        mixins.OAuthAuthorizeTokenMixin, 
        mixins.OAuthAccessTokenMixin, 
        OAuthRequestTokenMixin, 
        OAuthAuthorizeTokenMixin, 
        OAuthAccessTokenMixin, 
        OAuthMixin, 
        generic.base.View):
        
    def post(self, *args, **kwargs):
        return HttpResponseRedirect(self.get_oauth_authorization_url())
