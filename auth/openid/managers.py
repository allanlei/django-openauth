from django.db import models
from django.db.models import F

from auth.openid.utils import getAssociationRequestParams
from openid.store.nonce import SKEW

import time

class NonceManager(models.Manager):
    def use(self, server_url, timestamp, salt):
        created = False
        
        if abs(timestamp - time.time()) > SKEW:
            return False
        
        nonce, created = self.get_or_create(
            server_url__exact=server_url,
            timestamp__exact=timestamp,
            salt__exact=salt,
        )
        return created
    
    def clean(self, starting_time=None):
        if starting_time is None:
            starting_time = time.time()
        
        expired = self.filter(timestamp__lt=starting_time - SKEW)
        expired_count = expired.count()
        expired.delete()
        return expired_count


class AssociationManager(models.Manager):
    def request(self, endpoint, assoc_type=getattr(settings, 'OPENID_ASSOC_TYPE', None), session_type=getattr(settings, 'OPENID_SESSION_TYPE', None)):
        params = getAssociationRequestParams(endpoint, assoc_type, session_type)
        data = urllib2.urlopen(urllib2.Request(url, data=urllib.urlencode(params)))
        response = data.read(1024 * 1024)
        response_data = dict([tuple(arg.split(':', 1)) for arg in response.split()])
        print response_data
        
        dh_server_public = cryptutil.base64ToLong(values['dh_server_public'])
        enc_mac_key = oidutil.fromBase64(values['enc_mac_key'])
        modulus = 15454548
        dh_shared = pow(dh_server_public, enc_mac_key, modulus)
        hashed_dh_shared = sha1_module.new(cryptutil.longToBinary(dh_shared)).digest()

        secret = strxor(enc_mac_key, hashed_dh_shared)

        print secret
        
        
        
        
        
        
        
        
        
    def clean(self):
        now = int(time.time())
        expired = self.filter(issued__lt=now-F('lifetime'))
        expired_count = expired.count()
        expired.delete()
        return expired_count
