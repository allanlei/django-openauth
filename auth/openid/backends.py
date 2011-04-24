from django.contrib.auth.models import User

from auth.openid.exceptions import OpenIDValidationError
from auth.openid.models import Association, OpenIDProfile
from openid import kvform
import base64


class OpenIDBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def validate(self, return_to, openid={}):
        if return_to is None:
            raise OpenIDValidationError('No return_to specified')
        if 'openid.return_to' not in openid:
            raise OpenIDValidationError('openid.return_to not in response')
        if return_to != openid['openid.return_to']:
            raise OpenIDValidationError('The specified return_to did not match the openid.return_to in the response.')
        if openid.get('openid.mode', None) != 'id_res':
            raise OpenIDValidationError('openid process cancelled or invalid')
        if 'openid.signed' not in openid or 'openid.sig' not in openid:
            raise OpenIDValidationError('No openid signature present')
        
        signing_pairs = []
        for field in openid['openid.signed'].split(','):
            if 'openid.%s' % field not in openid:
                raise OpenIDValidationError('Signature does not match.')
            else:
                signing_pairs.append((field, openid['openid.%s' % field]))

        association = Association.objects.get(handle=openid['openid.assoc_handle'])
        if base64.b64encode(association.sign(kvform.seqToKV(tuple(signing_pairs)))) != openid['openid.sig']:
            raise OpenIDValidationError('Signature does not match!')
        
    def authenticate(self, return_to=None, openid=None):
        try:
            self.validate(return_to, openid)
        except OpenIDValidationError, err:
            return None
        return user
