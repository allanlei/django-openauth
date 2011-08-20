from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from openauth.openid.models import Association, Nonce
from openid import kvform

import base64
import urllib


class OpenIDNonceMixin(object):
    def get_openid_nonce(self, identifier=None):
        nonce = Nonce.objects.checkout(identifier or self.get_openid_login_endpoint())
        return str(nonce)

class OpenIDAssociationMixin(object):
    def get_openid_association(self):
        association, created = Association.objects.retrieve_or_generate(self.get_openid_login_endpoint())
        return association

class OpenIDLoginMixin(OpenIDAssociationMixin, OpenIDNonceMixin):
    openid_return_to = None
    openid_domain = None
    openid_realm = None
    
    def get_openid_return_to(self):
        if self.openid_return_to:
            url = self.openid_return_to
        else:
            raise ImproperlyConfigured('Provide openid_return_to or override get_openid_return_to().')
        return url

    def get_openid_domain(self):
        if self.openid_domain:
            domain = self.openid_domain
        else:
            raise ImproperlyConfigured('Provide openid_domain or override get_openid_domain().')
        return domain

    def get_openid_realm(self):
        return '%s://%s' % (self.request.is_secure() and 'https' or 'http', self.request.get_host())
        
    def get_openid_kwargs(self):
        return {
            'openid.mode': 'checkid_setup',
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.return_to': '%s?%s' % (self.get_openid_return_to(), urllib.urlencode({'nonce': self.get_openid_nonce()})),
            'openid.assoc_handle': self.get_openid_association().handle,      
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.realm': self.get_openid_realm(),
            'openid.ns.ax': 'http://openid.net/srv/ax/1.0',
            'openid.ns.ui': 'http://specs.openid.net/extensions/ui/1.0',
            'openid.ax.mode': 'fetch_request',
        }
        
    def get_openid_login_url(self):
        return '%s?%s' % (self.get_openid_login_endpoint(), urllib.urlencode(self.get_openid_kwargs()))

class OpenIDAuthenticationMixin(object):
    def is_openid_return_to_valid(self):
        return 'openid.return_to' in self.request.GET and self.request.GET['openid.return_to'].startswith(self.get_openid_return_to())

    def is_openid_mode_valid(self):
        return self.request.GET.get('openid.mode', None) == 'id_res'

    def is_openid_signature_valid(self):
        if 'openid.signed' not in self.request.GET or 'openid.sig' not in self.request.GET:
            return False
            
        signing_pairs = []
        for field in self.request.GET['openid.signed'].split(','):
            if 'openid.%s' % field not in self.request.GET:
                return False
            else:
                signing_pairs.append((field, self.request.GET['openid.%s' % field]))
                
        association = Association.objects.get(handle=self.request.GET['openid.assoc_handle'])
        return base64.b64encode(association.sign(kvform.seqToKV(tuple(signing_pairs)))) == self.request.GET['openid.sig']
    
    def is_openid_nonce_valid(self):
        return 'nonce' in self.request.GET and Nonce.objects.checkin(self.request.GET['openid.op_endpoint'].split('?')[0], self.request.GET['nonce'])

    def is_openid_response_valid(self):
        return self.is_openid_return_to_valid() and self.is_openid_mode_valid() and self.is_openid_signature_valid() and self.is_openid_nonce_valid()


class OpenIDAXMixin(object):
    openid_required_ax = None
    openid_ax_mapping = None
        
    def get_openid_required_ax(self):
        if self.openid_required_ax is not None:
            ax = list(self.openid_required_ax)
        else:
            raise ImproperlyConfigured("Provide openid_required_ax or override get_openid_required_ax().")
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

    def is_openid_ax_valid(self):
        for key, value in self.request.GET.items():
            print key, value
        return True
        
    def is_openid_response_valid(self):
        return self.is_openid_ax_valid() and super(OpenIDAXMixin, self).is_openid_response_valid()
