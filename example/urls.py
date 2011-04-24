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
)
