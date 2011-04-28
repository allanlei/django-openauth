from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from openauth.openid.models import Association, OpenIDProfile, Nonce

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
    
    def validate(self, return_to, openid={}, ax_data=None):
        if return_to is None:
            raise ValidationError('No return_to specified')
        if 'openid.return_to' not in openid:
            raise ValidationError('openid.return_to not in response')
        if not openid['openid.return_to'].startswith(return_to):
            raise ValidationError('The specified return_to did not match the openid.return_to in the response.')
        if openid.get('openid.mode', None) != 'id_res':
            raise ValidationError('openid process cancelled or invalid')
        if 'openid.signed' not in openid or 'openid.sig' not in openid:
            raise ValidationError('No openid signature present')        
        if 'nonce' not in openid or not Nonce.objects.checkin(openid['openid.op_endpoint'].split('?')[0], openid['nonce']):
            raise ValidationError('Nonce did not validate! Possibility of replay attack')
        if ax_data:
            pass
            
        signing_pairs = []
        for field in openid['openid.signed'].split(','):
            if 'openid.%s' % field not in openid:
                raise ValidationError('Signature does not match.')
            else:
                signing_pairs.append((field, openid['openid.%s' % field]))

        association = Association.objects.get(handle=openid['openid.assoc_handle'])
        if base64.b64encode(association.sign(kvform.seqToKV(tuple(signing_pairs)))) != openid['openid.sig']:
            raise ValidationError('Signature does not match!')
        
    def authenticate(self, return_to=None, openid=None, ax_data=None):
        self.validate(return_to, openid, ax_data)
