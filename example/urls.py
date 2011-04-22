from django.conf.urls.defaults import patterns, include, url
from django.views import generic

import views


openid_patterns = patterns('',
    url(r'^$', views.OpenIDView.as_view(), name='openid_login'),
)



urlpatterns = patterns('',
    url(r'^$', generic.base.RedirectView.as_view(url='/openid/')),
    url(r'^openid/$', include(openid_patterns)),
#    url(r'^oauth/$', include(oauth_patterns)),
    
    
    
    
    
    
    
    
#    url(r'^openid/callback/$', views.OpenIDLoginCallbackView.as_view(), name='openid_callback'),
#    url(r'^hybrid/$', views.OpenIDOAuthHybridLoginView.as_view(), name='hybrid_login'),
#    url(r'^oauth/$', views.OAuthLoginView.as_view(), name='oauth_login'),
#    
#    url(r'^hybrid/callback$', views.OpenIDOAuthHyrbidLoginCallbackView.as_view(), name='hybrid_callback'),
#    url(r'^oauth/callback/$', views.OAuthLoginCallbackView.as_view(), name='oauth_callback'),
)
