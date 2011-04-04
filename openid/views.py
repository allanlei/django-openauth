from django.views import generic
from django.core.exceptions import ImproperlyConfigured
from auth.mixins import ResponseValidatorMixin, HostInfoMixin
import urllib

from oauth.views import OAuthMixin

class OpenIDMixin(object):
    openid_realm = None
    openid_endpoint = None
    openid_callback_url = None
        
    def get_openid_callback_url(self):
        if self.openid_callback_url:
            url = self.openid_callback_url
        else:
            raise ImproperlyConfigured("Provide openid_callback_url or override get_openid_callback_url().")
        return url
        
    def get_openid_endpoint(self):
        if self.openid_endpoint:
            url = self.openid_endpoint
        else:
            raise ImproperlyConfigured("No Openid endpoint URL. Provide openid_endpoint or override get_openid_endpoint().")
        return url

    def get_openid_realm(self):
        if self.openid_realm:
            realm = self.openid_realm
        else:
            raise ImproperlyConfigured("Provide openid_realm or override get_openid_realm.")
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
        
class OpenIDAttributeExchangeMixin(object):
    openid_ax = None
    openid_ax_mapping = None
        
    def get_openid_ax(self):
        if self.openid_ax is not None:
            ax = list(self.openid_ax)
        else:
            raise ImproperlyConfigured("Provide openid_ax or override get_openid_ax().")
        return ax
    
    def get_openid_ax_mapping(self):
        if self.openid_ax_mapping:
            mapping = dict(self.openid_ax_mapping)
        else:
            mapping = {
                'openid.ax.type.email': {
                    'ns': 'http://axschema.org/contact/email',
                    'response': 'openid.ext1.value.email',
                },
                'openid.ax.type.firstname':{
                    'ns': 'http://axschema.org/namePerson/first',
                    'response': 'openid.ext1.value.firstname',
                },
                'openid.ax.type.lastname': {
                    'ns': 'http://axschema.org/namePerson/last',
                    'response': 'openid.ext1.value.lastname',
                },
                'openid.ax.type.language': {
                    'ns': 'http://axschema.org/pref/language',
                    'response': 'openid.ext1.value.language',
                },
                'openid.ax.type.country': {
                    'ns': 'http://axschema.org/contact/country/home',
                    'response': 'openid.ext1.value.country',
                }
            }
        return mapping
    
    def get_openid_kwargs(self):
        kwargs = super(OpenIDAttributeExchangeMixin, self).get_openid_kwargs()
        axs = self.get_openid_ax()
        if len(axs) > 0:
            ax_kwargs = {
                'openid.ax.required': ','.join([ax.split('.')[-1] for ax in axs]),
            }
            ax_mapping = self.get_openid_ax_mapping()
            ax_kwargs.update(dict([(ax, ax_mapping[ax]['ns']) for ax in axs]))
            kwargs.update(ax_kwargs)
        return kwargs
    
    def is_valid_openid_response(self):
        valid = super(OpenIDAttributeExchangeMixin, self).is_valid_openid_response()
#        mapping = self.get_openid_ax_mapping()
#        for ax in self.get_openid_ax():
#            valid = valid and mapping[ax]['response'] in self.request.GET
        return valid

class OpenIDLoginMixin(OpenIDMixin):
    def get_openid_login_url(self):
        return '%s?%s' % (self.get_openid_endpoint(), urllib.urlencode(self.get_openid_kwargs()))

        
        
        

class OpenIDLoginCallbackMixin(HostInfoMixin, OpenIDMixin):
    def is_valid_openid_signature(self):
        return True
    
    def is_valid_openid_discovered_info(self):
        return True
        
    def is_valid_openid_return_to(self):
        return_to = self.request.GET['openid.return_to']
        current_request_path = '%s%s' % (self.get_realm(), self.request.get_full_path())
        return current_request_path.startswith(return_to)
        
    def is_valid_openid_response(self):
        return self.is_valid_openid_return_to() and self.is_valid_openid_discovered_info() and self.is_valid_openid_signature()
    
