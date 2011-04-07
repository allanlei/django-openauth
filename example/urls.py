from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',    
    url(r'^$', views.OpenIDLoginView.as_view(), name='openid_login'),
    url(r'^hybrid/$', views.OpenIDOAuthHybridLoginView.as_view(), name='hybrid_login'),
    url(r'^oauth/$', views.OAuthLoginView.as_view(), name='oauth_login'),
    
    url(r'^openid/callback/$', views.OpenIDLoginCallbackView.as_view(), name='openid_callback'),
    url(r'^hybrid/callback$', views.OpenIDOAuthHyrbidLoginCallbackView.as_view(), name='hybrid_callback'),
    url(r'^oauth/callback/$', views.OAuthLoginCallbackView.as_view(), name='oauth_callback'),
)
