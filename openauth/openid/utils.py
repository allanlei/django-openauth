from django.core.validators import URLValidator

from openid import cryptutil
from openid.message import OPENID2_NS, OPENID1_NS
from openid.consumer.consumer import DiffieHellmanSHA1ConsumerSession, DiffieHellmanSHA256ConsumerSession

import time
import base64
import urllib
import urllib2
from sets import Set


import logging
logger = logging.getLogger(__name__)

SESSION_TYPES = {
    'DH-SHA1': DiffieHellmanSHA1ConsumerSession,
    'DH-SHA256': DiffieHellmanSHA256ConsumerSession,
}

ASSOCIATION_TYPES = {
    'HMAC-SHA1': {
        'DH-SHA1': SESSION_TYPES.get('DH-SHA1'),
        'DH-SHA256': SESSION_TYPES.get('DH-SHA256'),
    },
    'HMAC-SHA256': {
        'DH-SHA1': SESSION_TYPES.get('DH-SHA1'),
        'DH-SHA256': SESSION_TYPES.get('DH-SHA256'),
    },
}

OPENID_VERSIONS = {
    1: OPENID1_NS,
    2: OPENID2_NS,
}

def generate(endpoint, assoc_type='HMAC-SHA1', session_type='DH-SHA1', openid_ns=2):
    URLValidator()(endpoint)

    session_class = ASSOCIATION_TYPES.get(assoc_type).get(session_type)
    assoc_session = session_class()
    ns = OPENID_VERSIONS.get(openid_ns)

    params = {
        'mode': 'associate',
        'ns': ns,
        'assoc_type': assoc_type,
        'session_type': session_type,
    }
    params.update(assoc_session.getRequest())
    params = dict([('openid.%s' % key, value) for key, value in params.items()])
    
    response = {}
    try:
        data = urllib2.urlopen(urllib2.Request(endpoint, data=urllib.urlencode(params)))
        response_data = data.read(1024 * 1024)
        response = dict([tuple(arg.split(':', 1)) for arg in response_data.split()])
    except urllib2.HTTPError, err:
        logger.error('OpenID Association process failed. %s' % err)
        raise err


    required = ['dh_server_public', 'enc_mac_key', 'assoc_handle', 'assoc_type', 'session_type', 'expires_in', 'ns']
    if not response or Set(required).difference(Set(response.keys())):
        logger.error('There is a difference in expected OpenID keys')
        raise Exception('OpenID response is not valid.')
    
    dh_server_public = cryptutil.base64ToLong(response.get('dh_server_public'))
    enc_mac_key = base64.b64decode(response.get('enc_mac_key'))
    secret = assoc_session.dh.xorSecret(dh_server_public, enc_mac_key, assoc_session.hash_func)
    
    return {
        'server_url': endpoint,
        'handle': response['assoc_handle'],
        'secret': base64.b64encode(secret),
        'lifetime': int(response['expires_in']),
        'assoc_type': response['assoc_type'],
    }
