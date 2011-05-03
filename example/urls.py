from django.conf.urls.defaults import patterns, include, url
from django.views import generic

import views


openid_patterns = patterns('',
    url(r'^$', views.OpenIDView.as_view(), name='openid_login'),
)

oauth_patterns = patterns('',
    url(r'^$', views.OAuthView.as_view(), name='oauth_login'),
)



urlpatterns = patterns('',
    url(r'^$', generic.base.TemplateView.as_view(template_name='login.html')),
    
    url(r'^openid/$', include(openid_patterns)),
    url(r'^oauth/$', include(oauth_patterns)),
)
