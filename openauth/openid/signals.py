from django.contrib.auth.models import get_hexdigest

import time
import random
import utils


def generate_hash(sender, instance, **kwargs):       
    if instance.pk is None and instance.identifier:
        instance.timestamp = int(time.time())
        instance.salt = get_hexdigest('sha1', str(random.random()), str(random.random()))[:10]

def make_association(sender, instance, **kwargs):
    if not instance.server_url or not instance.assoc_type:
        raise Exception('association.server_url or association.assoc_type is None')

    response = utils.generate(instance.server_url, assoc_type=instance.assoc_type)
    instance.handle = response['handle']
    instance.secret = response['secret']
    instance.lifetime = response['lifetime']
    instance.issued = int(time.time())
