from django.db import models
from django.utils.crypto import salted_hmac

from managers import NonceManager, AssociationManager

from openid import cryptutil

import base64
import time


class Nonce(models.Model):
    identifier = models.URLField(db_index=True, blank=False, null=False)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=50)
    
    objects = NonceManager()
    
    def __unicode__(self):
        return base64.b64encode(salted_hmac(self.salt, ''.join([str(self.pk), self.identifier, str(self.timestamp)])).digest())


class Association(models.Model):
    TYPES = {
        'HMAC-SHA1': cryptutil.hmacSha1,
        'HMAC-SHA256': cryptutil.hmacSha256,
    }
    
    server_url = models.URLField(max_length=2048, db_index=True)
    handle = models.CharField(max_length=255, db_index=True)
    secret = models.TextField(max_length=255, blank=False)
    issued = models.IntegerField()
    lifetime = models.IntegerField(default=0)
    assoc_type = models.CharField(max_length=64, choices=[(t, t) for t in TYPES.keys()], default='HMAC-SHA1')

    objects = AssociationManager()
        
    def __unicode__(self):
        return u'%s %s min' % (self.server_url, self.timeleft/60)
    
    @property
    def timeleft(self):
        return int(self.issued) + int(self.lifetime) - int(time.time())
    
    @property
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


from django.db.models.signals import pre_save
from signals import generate_hash, make_association

pre_save.connect(generate_hash, sender=Nonce)
pre_save.connect(make_association, sender=Association)
