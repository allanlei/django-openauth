from django.db import models
from django.db.models import F
from django.conf import settings

import time
import logging
logger = logging.getLogger(__name__)


OPENAUTH_OPENID_NONCE_EXPIRE = getattr(settings, 'OPENAUTH_OPENID_NONCE_EXPIRE', 60 * 10)

class NonceManager(models.Manager):
    def validate(self, identifier, nonce_string):
        split = nonce_string.split('$', 1)
        hashed, salt = split[0], ''.join(split[1:])
        if hashed and salt:            
            try:
                nonce = self.nonexpired().filter(identifier=identifier).get(salt=salt)
                is_valid = str(nonce) == hashed
                nonce.delete()
                return is_valid
            except self.model.DoesNotExist:
                logger.warn('There was an attempt to use an invalid Nonce')
        return False

    def nonexpired(self):
        return self.filter(timestamp__gt=int(time.time()) - OPENAUTH_OPENID_NONCE_EXPIRE)

    def expired(self):
        return self.filter(timestamp__lte=int(time.time()) - OPENAUTH_OPENID_NONCE_EXPIRE)

class AssociationManager(models.Manager):
    def valid(self):
        return self.nonexpired()

    def nonexpired(self):
        return self.filter(issued__gt=int(time.time()) - F('lifetime'))

    def expired(self):
        return self.filter(issued__lte=int(time.time()) - F('lifetime'))
