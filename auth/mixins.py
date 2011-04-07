from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

class HostInfoMixin(object):
    def get_realm(self):
        return '%s://%s' % (self.get_protocol(), self.get_host())
        
    def get_host(self):
        return self.request.get_host()
    
    def get_protocol(self):
        return self.request.is_secure() and 'https' or 'http'

class CallbackMixin(object):
    def get_callback_url(self, url_attr, reverse_url_attr=None, error=None):
        if getattr(self, url_attr):
            url = getattr(self, url_attr)
        elif reverse_url_attr is not None and getattr(self, reverse_url_attr):
            url = '%s%s' % (self.get_realm(), reverse(getattr(self, reverse_url_attr)))
        else:
            properties = [prop for prop in [url_attr, reverse_url_attr] if prop is not None]
            raise ImproperlyConfigured(error or 'Provide %s.' % ' or '.join(properties))
        return url

class ResponseValidatorMixin(object):
    def is_valid(self):
        return True

class SignatureValidatorMixin(object):
    def is_signature_valid(self, signature_method):
        return True

class ContextDataMixin(object):
    def get_context_data(self, **kwargs):
        if hasattr(super(ContextDataMixin, self), 'get_context_data'):
            return super(ContextDataMixin, self).get_context_data(**kwargs)
        else:
            return {}
            
class TokenStorageMixin(object):
    storage_engine = None
    storage_key = None
    
    def get_storage_engine(self):
        if self.storage:
            storage = self.storage
        else:
            raise ImproperlyConfigured('Provide storage or override get_storage(). Must be dict like object')
        return storage
    
    def get_storage_key(self):
        if self.key:
            key = self.storage_key
        else:
            raise ImproperlyConfigured('Provide storage_key or override get_storage_key().')
        return key
        
    def get_token(self):
        return self.get_storage_engine()[self.get_storage_key()]
    
    def set_token(self, token):
        self.get_storage_engine()[self.get_storage_key()] = token
    
class SessionTokenStorageMixin(TokenStorageMixin):
    def get_storage_engine(self):
        return self.request.session
