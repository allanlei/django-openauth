from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate

from openid.consumer.consumer import Consumer, SUCCESS, FAILURE, CANCEL
from django_openid_auth.store import DjangoOpenIDStore
import urllib
        
class OpenIDMixin(object):
    openid_domain = None
    openid_realm = None
    openid_discovery_endpoint = None
    openid_login_endpoint = None
    openid_callback_url = None
    
    def get_openid_domain(self):
        if self.openid_domain:
            domain = self.openid_domain
        else:
            raise ImproperlyConfigured('Provide openid_domain or override get_openid_domain().')
        return domain
        
    def get_openid_callback_url(self):
        if self.openid_callback_url:
            url = self.openid_callback_url
        else:
            raise ImproperlyConfigured('Provide openid_callback_url or override get_openid_callback_url().')
        return url
    
    def get_openid_discovery_endpoint(self):
        if self.openid_discovery_endpoint:
            url = self.openid_discovery_endpoint
        else:
            raise ImproperlyConfigured('Provide openid_callback_url or override get_openid_callback_url().')
        return url
        
    def get_openid_login_endpoint(self):
        if self.openid_login_endpoint:
            url = self.openid_login_endpoint
        else:
            raise ImproperlyConfigured('No Openid endpoint URL. Provide openid_endpoint or override get_openid_endpoint().')
        return url

    def get_openid_realm(self):
        if self.openid_realm:
            realm = self.openid_realm
        else:
            raise ImproperlyConfigured('Provide openid_realm or override get_openid_realm.')
        return realm

    def get_openid_kwargs(self):
        kwargs = {
            'be': 'o8',
            'openid.mode': 'checkid_setup',
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.return_to': self.get_openid_callback_url(),
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.realm': self.get_openid_realm(),
            'openid.ns.ax': 'http://openid.net/srv/ax/1.0',
            'openid.ns.ui': 'http://specs.openid.net/extensions/ui/1.0',
            'openid.ax.mode': 'fetch_request',
        }
        return kwargs
    
    def get_openid_login_url(self):
        session = self.request.session.setdefault('OPENID', {})
        consumer = Consumer(session, DjangoOpenIDStore())
            
        openid_request = consumer.begin(self.get_openid_discovery_endpoint())
        return '%s?%s' % (self.get_openid_login_endpoint(), urllib.urlencode(self.get_openid_kwargs()))
    
    def get_openid_response(self):
        session = self.request.session.setdefault('OPENID', {})
        consumer = Consumer(session, DjangoOpenIDStore())
        openid_response = consumer.complete(dict(self.request.REQUEST.items()), self.request.build_absolute_uri())
        
        return openid_response



class GoogleOpenIDMixin(object):
    def get_openid_discovery_endpoint(self):
        return 'https://www.google.com/accounts/o8/site-xrds?hd=%(domain)s' % {'domain': self.get_openid_domain()}
        
    def get_openid_login_endpoint(self):
        return 'https://www.google.com/a/%(domain)s/o8/ud' % {'domain': self.get_openid_domain()}
