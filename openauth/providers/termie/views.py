from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from openauth.oauth.mixins import *

import mixins


OAUTH_CONSUMER_KEY = 'key'
OAUTH_CONSUMER_SECRET = 'secret'
consumer = oauth.Consumer(OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET)

class OAuthView(
        mixins.OAuthRequestTokenMixin,
        mixins.OAuthAuthorizeTokenMixin,
        mixins.OAuthAccessTokenMixin,
        OAuthRequestTokenMixin, 
        OAuthAuthorizeTokenMixin, 
        OAuthAccessTokenMixin, 
        OAuthMixin, 
        generic.base.View):
        
    oauth_consumer_key = OAUTH_CONSUMER_KEY
    oauth_consumer_secret = OAUTH_CONSUMER_SECRET
    oauth_consumer = consumer
        
    def post(self, *args, **kwargs):
        messages.success(self.request, self.get_oauth_access_token())
        return HttpResponseRedirect('/')
