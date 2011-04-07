from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login

from auth.openid import views


class OpenIDLoginView(views.OpenIDAXRequestMixin, views.OpenIDRequestMixin, generic.base.TemplateView):
    template_name = 'login.html'
    openid_required_ax = [
        'openid.ax.type.email', 
        'openid.ax.type.firstname', 
        'openid.ax.type.lastname', 
        'openid.ax.type.language', 
        'openid.ax.type.country',
    ]
    oauth_consumer_key = settings.OAUTH_CONSUMER_KEY
    oauth_secret_key = settings.OAUTH_CONSUMER_SECRET
    oauth_scopes = settings.OAUTH_SCOPES
    
    def get_openid_realm(self):
        return '%s://%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host())
        
    def get_openid_endpoint(self):
        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': self.request.POST['domain']}
        
    def get_openid_callback_url(self):
        return self.get_openid_realm() + reverse('openid_callback')

    def post(self, *args, **kwargs):
        return HttpResponseRedirect(self.get_openid_login_url())


class OpenIDLoginCallbackView(views.OpenIDResponseValidatorMixin, generic.base.TemplateView):
    template_name = 'login.html'
    
    def get(self, request, *args, **kwargs):
        if self.is_valid():
            user = authenticate(email=self.request.GET['openid.ext1.value.email'], openid_id=self.request.GET['openid.claimed_id'])
            if user:
                login(self.request, user)
                messages.success(self.request, 'Logged In as %s!' % user)
            else:
                messages.warning(self.request, 'OpenID log in successful, but Django login failed')
        else:
            messages.error(self.request, 'Log in failed') 
        return super(OpenIDLoginCallbackView, self).get(request, *args, **kwargs)
