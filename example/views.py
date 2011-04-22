from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login

from auth.openid import views


class OpenIDView(views.OpenIDRequestMixin, generic.base.TemplateView):
    template_name = 'login.html'
    openid_required_ax = [
        'openid.ax.type.email', 
        'openid.ax.type.firstname', 
        'openid.ax.type.lastname', 
        'openid.ax.type.language', 
        'openid.ax.type.country',
    ]
    
    def get_openid_realm(self):
        return '%s://%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host())
        
    def get_openid_endpoint(self):
        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': self.request.POST['domain']}
        
    def get_openid_callback_url(self):
        return self.get_openid_realm() + reverse('openid_login')

    def get(self, *args, **kwargs):
        if 'openid.mode' in self.request.GET:
            user = authenticate(callback=self.get_openid_callback_url(), openid=dict(self.request.GET.items()))
            if user:
#                login(self.request, user)
                messages.success(self.request, 'Logged In as %s!' % user)
            else:
                messages.warning(self.request, 'OpenID log in successful, but Django login failed')
        return super(OpenIDView, self).get(self.request, *args, **kwargs)
        
    def post(self, *args, **kwargs):
        return HttpResponseRedirect(self.get_openid_login_url())
