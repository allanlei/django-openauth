from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views import generic

import views
from forms import LoginForm

urlpatterns = patterns('',
    url(r'^accounts/login/$', views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    url(r'^accounts/login/authenticate/$', views.AuthenticationView.as_view(), name='authenticate'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    
    url(r'^accounts/profile/$', login_required(generic.base.TemplateView.as_view(template_name='home.html')), name='home'),
)
