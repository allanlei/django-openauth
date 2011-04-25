from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate

#from openid.consumer.consumer import Consumer, SUCCESS, FAILURE, CANCEL
#from django_openid_auth.store import DjangoOpenIDStore

from auth.openid.models import Association

import urllib


class OpenIDDiscoveryMixin(object):
    pass

class OpenIDAssociationMixin(object):
    pass



class OpenIDMixin(object):
    openid_domain = None
    openid_realm = None
    openid_discovery_endpoint = None
    openid_login_endpoint = None
    openid_return_to = None
    
    def get_openid_domain(self):
        if self.openid_domain:
            domain = self.openid_domain
        else:
            raise ImproperlyConfigured('Provide openid_domain or override get_openid_domain().')
        return domain
        
    def get_openid_return_to(self):
        if self.openid_return_to:
            url = self.openid_return_to
        else:
            raise ImproperlyConfigured('Provide openid_return_to or override get_openid_return_to().')
        return url
    
    def get_openid_discovery_endpoint(self):
        if self.openid_discovery_endpoint:
            url = self.openid_discovery_endpoint
        else:
            raise ImproperlyConfigured('Provide openid_return_to or override get_openid_return_to().')
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
        association = Association.tokens.get(server_url=self.get_openid_login_endpoint())

        kwargs = {
            'be': 'o8',
            'openid.mode': 'checkid_setup',
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.return_to': self.get_openid_return_to(),
            'openid.assoc_handle': association.handle,            
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.realm': self.get_openid_realm(),
            'openid.ns.ax': 'http://openid.net/srv/ax/1.0',
            'openid.ns.ui': 'http://specs.openid.net/extensions/ui/1.0',
            'openid.ax.mode': 'fetch_request',
        }
        return kwargs
    
    def get_openid_login_url(self):
        return '%s?%s' % (self.get_openid_login_endpoint(), urllib.urlencode(self.get_openid_kwargs()))


class OpenIDAXMixin(object):
    openid_required_ax = None
    openid_ax_mapping = None
        
    def get_openid_required_ax(self):
        if self.openid_required_ax is not None:
            ax = list(self.openid_required_ax)
        else:
            raise ImproperlyConfigured("Provide openid_ax or override get_openid_required_ax().")
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
        kwargs = super(OpenIDAXMixin, self).get_openid_kwargs()
        axs = self.get_openid_required_ax()
        if len(axs) > 0:
            ax_kwargs = {
                'openid.ax.required': ','.join([ax.split('.')[-1] for ax in axs]),
            }
            ax_mapping = self.get_openid_ax_mapping()
            ax_kwargs.update(dict([(ax, ax_mapping[ax]['ns']) for ax in axs]))
            kwargs.update(ax_kwargs)
        return kwargs
