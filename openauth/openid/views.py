from django.views import generic

from mixins import OpenIDLoginMixin, OpenIDAuthenticationMixin


class OpenIDLoginView(OpenIDLoginMixin, generic.base.View):
    def get_openid_realm(self):
        return '%s://%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host())

class OpenIDLoginAuthenticationView(OpenIDAuthenticationMixin, generic.base.View):
    pass
