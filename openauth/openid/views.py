from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate, login
from django.contrib.auth import REDIRECT_FIELD_NAME

from mixins import LoginMixin


import logging
logger = logging.getLogger(__name__)


class LoginView(LoginMixin, generic.edit.FormView):
    template_name = 'registration/login.html'
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_form_class(self):
        if self.authentication_form:
            form = self.authentication_form
        else:
            raise ImproperlyConfigured('Provide authentication_form')
        return form

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context.update({
            self.redirect_field_name: self.get_next_url(),
        })
        return context

    def get_next_url(self):
        return self.request.REQUEST.get(self.redirect_field_name, '')

    def get_openid_return_to_params(self):
        params = super(LoginView, self).get_openid_return_to_params()
        params.update({
            self.redirect_field_name: self.get_next_url(),
        })
        return params

    def get_success_url(self):
        return self.get_openid_login_url()

class AuthenticationView(generic.base.RedirectView):
    unsuccessful_login_url = None
    success_url = None
    
    def get_unsucessful_login_url(self):
        if self.unsuccessful_login_url:
            url = self.unsuccessful_login_url
        else:
            raise ImproperlyConfigured('Provide unsuccessful_login_url')
        return url

    def get_success_url(self):
        if self.successful_login_url:
            url = self.successful_login_url
        else:
            raise ImproperlyConfigured('Provide successful_login_url')
        return url

    def is_valid_openid_response(self):
        return True

    def get_openid_response_data(self):
        return dict([(key.replace('openid.', ''), val) for key, val in self.request.GET.items() if key.startswith('openid.')])

    def get_redirect_url(self):
        if self.is_valid_openid_response():
            return self.get_success_url()
        return self.get_unsucessful_login_url()
