from django.db import models
from django.contrib.auth.models import User

from auth.openid import managers

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
    server_url = models.TextField(max_length=2048)
    handle = models.CharField(max_length=255)
    secret_key = models.TextField(max_length=255) # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField(max_length=64)

    objects = managers.AssociationManager()
    
    class Meta:
        ordering = ['-issued']
        
    def __unicode__(self):
        return u'Association: %s, %s' % (self.server_url, self.handle)
    
    def is_expired(self):
        return self.issued < int(time.time()) - self.lifetime
    
    @property
    def secret(self):
        return base64.b64decode(self.secret_key)
    
    @secret.setter
    def secret(self, secret):
        self.secret_key = base64.b64encode(secret)

class OpenIDProfile(models.Model):
    user = models.ForeignKey(User, related_name='')
    claimed_id = models.TextField(max_length=2048, unique=True)
    display_id = models.TextField(max_length=2048, blank=True)


from signals import association_associate
models.signals.pre_save.connect(association_associate, sender=Association)
