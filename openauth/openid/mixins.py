from django.core.exceptions import ImproperlyConfigured
from django.utils.http import urlencode

import logging
logger = logging.getLogger(__name__)


class LoginMixin(object):
    openid_login_endpoint = None

    def get_openid_login_endpoint(self):
        if self.openid_login_endpoint:
            endpoint = self.openid_login_endpoint
        else:
            raise ImproperlyConfigured('Provide the openid login endpoint.')
        return endpoint

    def get_openid_return_to_url(self):
        return self.request.build_absolute_uri(self.request.path)
        
    def get_openid_return_to_params(self):
        return {}
        
    def get_openid_return_to(self):
        return '%(url)s?%(params)s' % {
            'url': self.get_openid_return_to_url(),
            'params': urlencode(self.get_openid_return_to_params()),
        }

    def get_openid_login_params(self):
        return {
            'openid.mode': 'checkid_setup',
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.return_to': self.get_openid_return_to(), 
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        }
        
    def get_openid_login_url(self):
        return '%s?%s' % (self.get_openid_login_endpoint(), urlencode(self.get_openid_login_params()))
