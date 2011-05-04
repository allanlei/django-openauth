from django.conf.urls.defaults import patterns, include, url
from django.views import generic

from providers.google_apps import views as google_apps
from providers.termie import views as termie

openid_patterns = patterns('',
    url(r'^$', generic.base.RedirectView.as_view(url='/openid/google_apps/')),
    url(r'^google_apps/$', google_apps.OpenIDView.as_view(), name='google_apps'),
    url(r'^google_apps/hyrbid/$', google_apps.HybridOpenIDView.as_view(), name='google_apps_hybrid'),
)

oauth_patterns = patterns('',
    url(r'^$', generic.base.RedirectView.as_view(url='/oauth/googleapps/')),
#    url(r'^google/$', providers.google.views.OAuthView.as_view(), name='google'),
    url(r'^googleapps/$', google_apps.OAuthView.as_view(), name='google_apps'),
    url(r'^termie/$', termie.OAuthView.as_view(), name='termie'),
)



urlpatterns = patterns('',
    url(r'^$', generic.base.TemplateView.as_view(template_name='login.html')),
    
    url(r'^openid/', include(openid_patterns, namespace='openid')),
    url(r'^oauth/', include(oauth_patterns, namespace='oauth')),
)
