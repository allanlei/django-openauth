from django.db import models
from django.db.models import F

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
    def clean(self):
        now = int(time.time())
        expired = self.filter(issued__lt=now-F('lifetime'))
        expired_count = expired.count()
        expired.delete()
        return expired_count
