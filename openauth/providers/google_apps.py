from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


class OpenIDMixin(object):
    google_apps_domain = None
    
    def get_openid_login_endpoint(self):
        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': self.get_google_apps_domain()}

    def get_openid_discovery_endpoint(self):
        return 'https://www.google.com/accounts/o8/site-xrds?hd=%(domain)s' % {'domain': self.get_google_apps_domain()}

    def get_google_apps_domain(self):
        if self.google_apps_domain:
            domain = self.google_apps_domain
        else:
            raise ImproperlyConfigured('Provide google_apps_domain')
        return domain

class HyrbridOpenIDMixin(OpenIDMixin):
    oauth_consumer_key = getattr(settings, 'OPENAUTH_OAUTH_CONSUMER_KEY', None)
    google_oauth_scopes = getattr(settings, 'OPENAUTH_GOOGLE_OAUTH_SCOPES', None)
    
    def get_oauth_consumer_key(self):
        if self.oauth_consumer_key:
            key = self.oauth_consumer_key
        else:
            raise ImproperlyConfigured('Provide oauth_consumer_key')
        return key

    def get_google_oauth_scopes(self):
        if self.google_oauth_scopes is None:
            scopes = list(self.google_oauth_scopes)
        else:
            raise ImproperlyConfigured('Provide google_oauth_scopes.')
        return scopes
        
    def get_openid_login_params(self):
        context = super(OAuthExtensionMixin, self).get_openid_login_params()
        scopes = self.get_google_oauth_scopes()
        
        if scopes:
            context.update({
                'openid.ns.ext2': 'http://specs.openid.net/extensions/oauth/1.0',
                'openid.ext2.consumer': self.get_oauth_consumer_key(),
                'openid.ext2.scope': ' '.join(scopes),
            })
        return context




#from django.core.exceptions import ImproperlyConfigured
##from openauth.oauth.mixins import OAuthMixin


#class OpenIDMixin(object):
#    def get_openid_discovery_endpoint(self):
#        return 'https://www.google.com/accounts/o8/site-xrds?hd=%(domain)s' % {'domain': self.get_openid_domain()}
#        
#    def get_openid_login_endpoint(self):
#        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': self.get_openid_domain()}

#class GoogleOpenIDOAuthMixin(object):
#    google_oauth_scopes = None

#    def get_google_oauth_scopes(self):
#        if self.google_oauth_scopes is not None:
#            scopes = self.google_oauth_scopes
#        else:
#            raise ImproperlyConfigured('Provide google_oauth_scopes or override get_google_oauth_scopes().')
#        return scopes
#        
#    def get_openid_kwargs(self):
#        kwargs = super(GoogleOpenIDOAuthMixin, self).get_openid_kwargs()
#        kwargs.update({
#            'openid.ns.ext2': 'http://specs.openid.net/extensions/oauth/1.0',
#            'openid.ext2.consumer': self.get_oauth_consumer_key(),
#            'openid.ext2.scope': ' '.join(self.get_oauth_scopes()),
#        })
#        return kwargs

#class OAuthRequestTokenMixin(object):
#    oauth_request_endpoint = 'https://www.google.com/accounts/OAuthGetRequestToken'
#    google_oauth_scopes = None
#    google_oauth_callback = None
#    
#    def get_google_oauth_callback(self):
#        if self.google_oauth_callback:
#            url = self.google_oauth_callback
#        else:
#            raise ImproperlyConfigured('Provide google_oauth_callback or override get_google_oauth_callback().')
#        return url
#    
#    def get_google_oauth_scopes(self):
#        if self.google_oauth_scopes:
#            scopes = self.google_oauth_scopes
#        else:
#            raise ImproperlyConfigured('Provide google_oauth_scopes or override get_google_oauth_scopes().')
#        return scopes
#        
#    def get_oauth_request_endpoint_params(self):
#        params = super(OAuthRequestTokenMixin, self).get_oauth_request_endpoint_params()
#        params.update({
#            'scope': ' '.join(self.get_google_oauth_scopes()),
#            'oauth_callback': self.get_google_oauth_callback(),
#        })
#        return params

#class OAuthAuthorizeTokenMixin(object):
#    oauth_authorization_endpoint = 'https://www.google.com/accounts/OAuthAuthorizeToken'

#class OAuthAccessTokenMixin(object):
#    oauth_access_endpoint = 'https://www.google.com/accounts/OAuthGetAccessToken'
















#from django.views import generic
#from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
#from django.contrib import messages
#from django.contrib.auth import authenticate, login
#from django.conf import settings

#from openauth.openid.mixins import OpenIDMixin
#from openauth.oauth.mixins import OAuthMixin, OAuthRequestTokenMixin, OAuthAuthorizeTokenMixin, OAuthAccessTokenMixin

#import mixins


#class GoogleOpenIDView(mixins.OpenIDMixin, OpenIDMixin, generic.base.View):
#    def post(self, *args, **kwargs):
#        return HttpResponseRedirect(self.get_openid_login_url())
#        

#class OpenIDOAuthHybridView(
#        mixins.GoogleOpenIDOAuthMixin,
#        mixins.OpenIDMixin, 
#        mixins.OAuthAccessTokenMixin,
#        OpenIDMixin, 
#        OAuthAccessTokenMixin, 
#        generic.base.View):

#    def get_oauth_token(self):
#        return {
#            'oauth_token': self.request.GET['openid.ext1.request_token'],
#            'oauth_token_secret': '',
#        }

#class OAuthView(
#        mixins.OAuthRequestTokenMixin, 
#        mixins.OAuthAuthorizeTokenMixin, 
#        mixins.OAuthAccessTokenMixin, 
#        OAuthRequestTokenMixin, 
#        OAuthAuthorizeTokenMixin, 
#        OAuthAccessTokenMixin, 
#        OAuthMixin, 
#        generic.base.View):
#        
#    def post(self, *args, **kwargs):
#        return HttpResponseRedirect(self.get_oauth_authorization_url())
