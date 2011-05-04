from openid.message import OPENID2_NS, OPENID1_NS
from openid.consumer.consumer import DiffieHellmanSHA1ConsumerSession, DiffieHellmanSHA256ConsumerSession

from openid import cryptutil

import base64
import urllib
import urllib2


REQUEST_TYPE = {
    'HMAC-SHA1': {
        'DH-SHA1': DiffieHellmanSHA1ConsumerSession,
        'DH-SHA256': DiffieHellmanSHA256ConsumerSession,
    },
    'HMAC-SHA256': {
        'DH-SHA1': DiffieHellmanSHA1ConsumerSession,
        'DH-SHA256': DiffieHellmanSHA256ConsumerSession,
    },
}

def generate(endpoint, assoc_type='HMAC-SHA1', session_type='DH-SHA1', ns=OPENID2_NS):
    if assoc_type not in REQUEST_TYPE:
        raise Exception('Unknown assoc_type')
    if session_type not in REQUEST_TYPE[assoc_type]:
        raise Exception('Unknown session_type')
        
    session_class = REQUEST_TYPE[assoc_type][session_type]
    assoc_session = session_class()
    params = {
        'mode': 'associate',
        'ns': ns,
        'assoc_type': assoc_type,
        'session_type': session_type,
    }
        
    params.update(assoc_session.getRequest())
    params = dict([('openid.%s' % key, value) for key, value in params.items()])

    try:
        data = urllib2.urlopen(urllib2.Request(endpoint, data=urllib.urlencode(params)))
    except HTTPError, err:
        raise Exception('OpenID: Http404 %s %s' % (endpoint, str(params)))
        
    response = data.read(1024 * 1024)
    response_data = dict([tuple(arg.split(':', 1)) for arg in response.split()])
        
    if 'dh_server_public' not in response_data or 'enc_mac_key' not in response_data:
        raise Exception('Bad OpenID association response from %s' % endpoint)
        
    dh_server_public = cryptutil.base64ToLong(response_data['dh_server_public'])
    enc_mac_key = base64.b64decode(response_data['enc_mac_key'])

    secret = assoc_session.dh.xorSecret(dh_server_public, enc_mac_key, assoc_session.hash_func)
        
    defaults = {
        'server_url': endpoint,
        'handle': response_data['assoc_handle'],
        'secret': base64.b64encode(secret),
        'lifetime': int(response_data['expires_in']),
        'assoc_type': response_data['assoc_type'],
    }
    return defaults
