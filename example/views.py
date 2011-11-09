from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from openauth.openid import views as openid
from openauth.providers.google_apps import OpenIDMixin as GoogleAppsOpenIDMixin
from openauth.openid.extensions import UIExtension, AXExtension, AssociationExtension, NonceExtension



class Extensions(GoogleAppsOpenIDMixin, NonceExtension, AssociationExtension, UIExtension, AXExtension):
    def get_login_url(self):
        return reverse('login')

    def get_login_authenticate_url(self):
        return reverse('authenticate')
    
class LoginView(Extensions, openid.LoginView):
    def form_valid(self, form, **kwargs):
        self.google_apps_domain = form.cleaned_data['domain']
        return super(LoginView, self).form_valid(form, **kwargs)

    def get_openid_return_to_url(self):
        return self.request.build_absolute_uri(self.get_login_authenticate_url())


class AuthenticationView(Extensions, openid.AuthenticationView):
    def get_success_url(self):
        User.objects.get_or_create(username=self.request.GET.get('openid.claimed_id'))      #Fake user creation
        
        user = authenticate(username=self.request.GET.get('openid.claimed_id'))
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return reverse('home')
        return self.get_login_url()
