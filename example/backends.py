from django.conf import settings
from django.contrib.auth.models import User
from models import UserProfile

import urllib

class OpenIDBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    _signing_key = None
    
    def __init__(self):
        if self.__class__._signing_key is None:
            self.__class__._signing_key = self.get_signing_key()
    
    def get_signing_key(self):
	
        url = 'https://www.google.com/a/helveticode.com/o8/ud?be=o8'

        params = urllib.urlencode({
            'ns': 'http://specs.openid.net/auth/2.0',
            'dh_consumer_public': 'AMO8ntCnm/Q3tD02QoeFm4RysQxEZO6cofivMAjKb5qhQKXpqHLBMe4zVX7OC4wkDarGp+3kG5ypynZRu/L9CsqnZZi7fbyFKK+NhAmDhji2JaIFw5/GDXPKYFgCpgt31ohbSPnjJcuU1JRtiI2XZJKyto0m4Mr2fnj09vMkrMm3'
            'mode': 'associate',
            'assoc_type': 'HMAC-SHA1',
            'session_type': 'DH-SHA1',
        })

        data = urllib.urlopen(url, params).read()
	
	
	
#        return '445609452350.apps.googleusercontent.com'
    
    def get_signature(self, secret, data):
        return ''
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, callback=None, requested_ax=[], openid=None):
        user = None
        if openid.get('openid.mode', None) == 'id_res':
            if 'openid.signed' in openid and 'openid.sig' in openid:
                for ax in requested_ax:
                    if ax not in openid:
                        return None
                if callback != openid['openid.return_to']:
                    return None
                
                signing_pairs = {}
                for field in openid['openid.signed'].split(','):
                    if 'openid.%s' % field not in openid:
                        return None
                    else:
                        signing_pairs[field] = openid['openid.%s' % field]
                
                computed_signature = self.get_signature(self.get_signing_key())
                if computed_signature == openid['openid.sig']:
                    print 'CREATE USER'
        return user
