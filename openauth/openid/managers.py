from django.db import models
from django.db.models import F
from django.contrib.auth.models import get_hexdigest

from openid.store.nonce import SKEW
from openid.message import OPENID2_NS, OPENID1_NS
from openid import cryptutil

import utils

import base64
import urllib
import urllib2
import time
import random

class AssociationCreationError(Exception):
    pass

class QuerySetManager(models.Manager):
    def __init__(self, queryset_class=None, *args, **kwargs):
        super(QuerySetManager, self).__init__(*args, **kwargs)
        self.queryset_class = queryset_class
        
    def get_query_set(self):
        if self.queryset_class:
            return self.queryset_class(self.model)
        return super(QuerySetManager, self).get_query_set()
            
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

class NonceQuerySet(models.query.QuerySet):
    def clean(self):
        self.filter(timestamp__lt=int(time.time()) - self.model.EXPIRES).delete()
        
class NonceManager(QuerySetManager):
    def __init__(self, *args, **kwargs):
        super(NonceManager, self).__init__(queryset_class=NonceQuerySet, *args, **kwargs)

    def checkout(self, identifier):
        timestamp = int(time.time())
        salt = get_hexdigest('sha1', str(random.random()), str(random.random()))[:10]
        return self.create(identifier=identifier, timestamp=timestamp, salt=salt)
    
    def checkin(self, identifier, nonce_string):
        split = nonce_string.split('$', 1)
        hashed, salt = split[0], ''.join(split[1:])
        if hashed and salt:
            try:
                nonce = self.get(salt=salt, identifier=identifier)
                valid = not nonce.is_expired() and nonce.get_hash() == nonce_string
                nonce.delete()
                return valid
            except self.model.DoesNotExist:
                pass
        return False






class AssociationQuerySet(models.query.QuerySet):        
    def clean(self):
        now = int(time.time())
        expired = self.filter(issued__lt=now-F('lifetime'))
        expired_count = expired.count()
        expired.delete()
        return expired_count
    
    def renew(self, session_type='DH-SHA1', ns=OPENID2_NS):
        count = 0
        for association in self.all():
            defaults = utils.generate(association.server_url, association.assoc_type, session_type, ns)
            association.handle = defaults['handle']
            association.secret_key = defaults['secret']
            association.lifetime = defaults['lifetime']
            association.assoc_type = defaults['assoc_type']
            association.save()
            count = count + 1
        return count
        
class AssociationManager(QuerySetManager):
    def __init__(self, *args, **kwargs):
        super(AssociationManager, self).__init__(queryset_class=AssociationQuerySet, *args, **kwargs)
        
    def retrieve_or_generate(self, endpoint, valid=True, **kwargs):
        try:
            self.clean()
        except:
            pass
        try:
            return self.retrieve(endpoint, valid=valid), False
        except self.model.DoesNotExist:
            return self.generate(endpoint, **kwargs), True
            
    def retrieve(self, endpoint, valid=True):
        filters = {
            'server_url': endpoint,
        }
        if valid:
            filters['issued__gt'] = int(time.time()) - F('lifetime')
        try:
            return self.get(**filters)
        except self.model.MultipleObjectsReturned:
            return self.filter(**filters)[0]

    def generate(self, endpoint, assoc_type='HMAC-SHA1', session_type='DH-SHA1', ns=OPENID2_NS):
        defaults = utils.generate(endpoint, assoc_type, session_type, ns)
        return self.create(**defaults)
