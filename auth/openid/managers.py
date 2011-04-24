from django.db import models
from django.db.models import F

from openid.store.nonce import SKEW
from openid.message import OPENID2_NS, OPENID1_NS
from openid import cryptutil, oidutil

from utils import REQUEST_TYPE

import urllib
import urllib2
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
    def clean(self):
        now = int(time.time())
        expired = self.filter(issued__lt=now-F('lifetime'))
        expired_count = expired.count()
        expired.delete()
        return expired_count
    
    def request(self, endpoint, assoc_type='HMAC-SHA1', session_type='DH-SHA1', update=True):
        if assoc_type not in REQUEST_TYPE:
            raise Exception('Unknown assoc_type')
        if session_type not in REQUEST_TYPE[assoc_type]:
            raise Exception('Unknown session_type')
            
        session_class = REQUEST_TYPE[assoc_type][session_type]
        assoc_session = session_class()
        
        params = {
            'mode': 'associate',
            'ns': OPENID2_NS,
            'assoc_type': assoc_type,
            'session_type': session_type,
        }
        params.update(assoc_session.getRequest())
        params = dict([('openid.%s' % key, value) for key, value in params.items()])
        
        data = urllib2.urlopen(urllib2.Request(endpoint, data=urllib.urlencode(params)))
        
        response = data.read(1024 * 1024)
        response_data = dict([tuple(arg.split(':', 1)) for arg in response.split()])

        dh_server_public = cryptutil.base64ToLong(response_data['dh_server_public'])
        enc_mac_key = oidutil.fromBase64(response_data['enc_mac_key'])        
        
        secret = assoc_session.dh.xorSecret(dh_server_public, enc_mac_key, assoc_session.hash_func)
        
        defaults = {
            'handle': response_data['assoc_handle'],
            'secret_key': oidutil.toBase64(secret),
            'lifetime': int(response_data['expires_in']),
            'assoc_type': response_data['assoc_type'],
        }
        
        if update:
            association, created = self.get_or_create(server_url=endpoint, defaults=defaults)
            if not created:
                self.filter(pk=association.pk).update(**defaults)
        else:
            association = self.create(server_url=endpoint, **defaults)
        return association
