from django.db import models
from django.contrib.auth.models import User

from auth.openid import managers

from openid import oidutil, cryptutil, kvform

import base64
import time


class Nonce(models.Model):
    server_url = models.TextField(max_length=2048)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    objects = managers.NonceManager()
    
    class Meta:
        ordering = ['-timestamp']
        
    def __unicode__(self):
        return u'Nonce: %s, %s' % (self.server_url, self.salt)

class Association(models.Model):
    TYPES = {
        'HMAC-SHA1': None,
        'HMAC-SHA256': None,
    }    
    
    server_url = models.TextField(max_length=2048)
    handle = models.CharField(max_length=255)
    secret_key = models.TextField(max_length=255)
    issued = models.IntegerField(default=time.time)
    lifetime = models.IntegerField(default=0)
    assoc_type = models.TextField(max_length=64, choices=tuple([(t, t) for t in TYPES.keys()]))

    objects = managers.AssociationManager()
    
    class Meta:
        ordering = ['-issued']
        
    def __unicode__(self):
        return u'%s issued: %s exp:%smin' % (self.server_url, self.issued, self.timeleft()/60)
    
    def timeleft(self):
        return int(self.issued) + int(self.lifetime) - int(time.time())
        
    def is_expired(self):
        return self.timeleft < 0
    
    @property
    def secret(self):
        return self.secret_key
#        return base64.b64decode(self.secret_key)
    
    @secret.setter
    def secret(self, secret):
        self.secret_key = secret
#        self.secret_key = base64.b64encode(secret)
    
    def sign(self, message):
        hash_func = None
        if self.assoc_type == 'HMAC-SHA1':
            hash_func = cryptutil.hmacSha1
        elif self.assoc_type == 'HMAC-SHA256':
            hash_func = cryptutil.hmacSha256
        secret = base64.b64decode(self.secret_key)
        return hash_func(secret, message)
        
class OpenIDProfile(models.Model):
    user = models.ForeignKey(User)
    claimed_id = models.TextField(max_length=2048, unique=True)
    display_id = models.TextField(max_length=2048, blank=True)


#from signals import association_associate
#models.signals.pre_save.connect(association_associate, sender=Association)
