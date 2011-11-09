from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from models import Association, Nonce

from openid import kvform

import base64
import logging
logger = logging.getLogger(__name__)


class NonceExtension(object):
    nonce_field = 'nonce'
    
    def get_openid_return_to_params(self):
        params = super(NonceExtension, self).get_openid_return_to_params()
        
        nonce = Nonce.objects.create(identifier=self.get_openid_login_endpoint())
        params.update({
            self.nonce_field: '%s$%s' % (nonce, nonce.salt),
        })
        return params

    def is_valid_openid_response(self):
        identifier = self.request.GET.get('openid.op_endpoint')
        nonce = self.request.GET.get(self.nonce_field)
        if identifier is None or nonce is None:
            return False
        valid = Nonce.objects.validate(identifier.split('?')[0], nonce)
        if not valid:
            logger.warn('Attempt to validate invalid Nonce')
        return valid and super(NonceExtension, self).is_valid_openid_response()
        
class AssociationExtension(object):
    def get_openid_association(self):
        assoc, created = Association.objects.valid().get_or_create(server_url=self.get_openid_login_endpoint())
        return assoc

    def get_openid_login_params(self):
        context = super(AssociationExtension, self).get_openid_login_params()
        context.update({
            'openid.assoc_handle': self.get_openid_association().handle,
        })
        return context

    def is_valid_openid_response(self):
        data = self.get_openid_response_data()
        if 'signed' not in data:
            return False
        if 'sig' not in data:
            return False
        if 'assoc_handle' not in data:
            return False
        
        associations = Association.objects.filter(handle=data['assoc_handle'])
        if not associations.exists():
            return False
            
        signing_pairs = []
        for field in data['signed'].split(','):
            if field not in data:
                return False
            else:
                signing_pairs.append((field, data[field]))
        association = associations.get()
        valid = base64.b64encode(association.sign(kvform.seqToKV(tuple(signing_pairs)))) == data['sig']
        return valid and super(AssociationExtension, self).is_valid_openid_response()


class PAPEExtension(object):
    def get_openid_login_params(self):
        context = super(PAPEExtension, self).get_openid_login_params()
        context.update({
            'openid.ns.pape': 'http://specs.openid.net/extensions/pape/1.0',
        })
        return context

    def is_valid_openid_response(self):
        valid = True
        return valid and super(PAPEExtension, self).is_valid_openid_response()
        
class UIExtension(object):
    def get_openid_login_params(self):
        context = super(UIExtension, self).get_openid_login_params()
        context.update({
            'openid.ns.ui': 'http://specs.openid.net/extensions/ui/1.0',
        })
        return context

class AXExtension(object):
    openid_ax_extensions = getattr(settings, 'OPENAUTH_OPENID_AX', {
        ('openid.ax.type.country', 'http://axschema.org/contact/country/home'): '',
        ('openid.ax.type.email', 'http://axschema.org/contact/email'): '',
        ('openid.ax.type.firstname', 'http://axschema.org/namePerson/first'): '',
        ('openid.ax.type.language', 'http://axschema.org/pref/language'): '',
        ('openid.ax.type.lastname', 'http://axschema.org/namePerson/last'): '',
    })
    
    def get_openid_ax_extensions(self):
        if self.openid_ax_extensions is not None:
            exts = self.openid_ax_extensions
        else:
            raise ImproperlyConfigured('Provide openid_ax_extensions or set as [].')
        return exts
        
    def get_openid_login_params(self):
        context = super(AXExtension, self).get_openid_login_params()
        
        extensions = self.get_openid_ax_extensions().keys()
        if extensions:
            mapping = dict(extensions)
            context.update({
                'openid.ns.ax': 'http://openid.net/srv/ax/1.0',
                'openid.ax.mode': 'fetch_request',
                'openid.ax.required': ','.join([ax.split('.')[-1]for ax in mapping.keys()]),
            })
            context.update(mapping)
        return context

    def is_valid_openid_response(self):
        valid = True
        #Should validate ax data, ensure there is no extra fields
        return valid and super(AXExtension, self).is_valid_openid_response()
