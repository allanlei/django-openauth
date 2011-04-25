from django.db import models
from django.db.models import F

from openid.store.nonce import SKEW
from openid.message import OPENID2_NS, OPENID1_NS
from openid import cryptutil

from utils import generate

import base64
import urllib
import urllib2
import time



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
    def clean(self, starting_time=None):
        if starting_time is None:
            starting_time = time.time()
        
        expired = self.filter(timestamp__lt=starting_time - SKEW)
        expired_count = expired.count()
        expired.delete()
        return expired_count
    
class NonceManager(QuerySetManager):
    def __init__(self, *args, **kwargs):
        super(NonceManager, self).__init__(queryset_class=NonceQuerySet, *args, **kwargs)

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
            defaults = generate(association.server_url, association.assoc_type, session_type, ns)
            association.handle = defaults['handle']
            association.secret_key = defaults['secret_key']
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
            return self.retrieve(endpoint, valid=valid), False
        except self.model.DoesNotExist:
            return self.generate(endpoint, **kwargs), True
            
    def retrieve(self, endpoint, valid=True):
        filters = {}
        if valid:
            filters['issued__gt'] = int(time.time()) - F('lifetime')
        return self.get(server_url=endpoint, **filters)

    def generate(self, endpoint, assoc_type='HMAC-SHA1', session_type='DH-SHA1', ns=OPENID2_NS):
        defaults = generate(endpoint, assoc_type, session_type, ns)
        return self.create(**defaults)
