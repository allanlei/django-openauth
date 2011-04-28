from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from auth.openid import managers

from openid import cryptutil

import hashlib
import base64
import time


class Nonce(models.Model):
    EXPIRES = 60 * 10
    identifier = models.TextField(max_length=2048, db_index=True)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    objects = managers.NonceManager()
    
    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return self.get_hash()
    
    def is_expired(self):
        return self.timestamp + self.EXPIRES < time.time()

    def get_hash(self):
        h = hashlib.sha1()
        h.update(str(self.pk))
        h.update(self.identifier)
        h.update(str(self.timestamp))
        h.update(self.salt)
        h.update(settings.SECRET_KEY)
        return '%s$%s' % (base64.b64encode(h.digest()), self.salt)

class Association(models.Model):
    TYPES = {
        'HMAC-SHA1': cryptutil.hmacSha1,
        'HMAC-SHA256': cryptutil.hmacSha256,
    }    
    
    server_url = models.TextField(max_length=2048, db_index=True)
    handle = models.CharField(max_length=255, db_index=True)
    secret = models.TextField(max_length=255, blank=False)
    issued = models.IntegerField(default=time.time)
    lifetime = models.IntegerField(default=0)
    assoc_type = models.TextField(max_length=64, choices=tuple([(t, t) for t in TYPES.keys()]))

    objects = managers.AssociationManager()
    
    class Meta:
        ordering = ['-issued']
        
    def __unicode__(self):
        return u'%s exp:%smin' % (self.server_url, self.timeleft()/60)
    
    def timeleft(self):
        return int(self.issued) + int(self.lifetime) - int(time.time())
        
    def is_expired(self):
        return self.timeleft < 0
    
    @property
    def secret_key(self):
        return base64.b64decode(self.secret)
    
    @secret_key.setter
    def secret_key(self, secret):
        self.secret = base64.b64encode(secret)
    
    def sign(self, message):
        hash_func = self.TYPES[self.assoc_type]
        return hash_func(self.secret_key, message)
         
class OpenIDProfile(models.Model):
    user = models.ForeignKey(User)
    claimed_id = models.TextField(max_length=2048, unique=True)
    display_id = models.TextField(max_length=2048, blank=True)  #rename to identity
