from openid.message import OPENID2_NS, OPENID1_NS
from openid.consumer.consumer import DiffieHellmanSHA1ConsumerSession, DiffieHellmanSHA256ConsumerSession


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

def getAssociationRequestParams(endpoint, assoc_type, session_type):
    if assoc_type not in REQUEST_TYPE:
        raise Exception('Unknown assoc_type')
    if session_type not in REQUEST_TYPE[assoc_type]:
        raise Exception('Unknown session_type')
        
    session_class = REQUEST_TYPE[assoc_type][session_type]
    assoc_session = session_class()
    print '\tMOD: ', assoc_session.dh.modulus
    print '\tGEN: ', assoc_session.dh.generator
    
    params = {
        'mode': 'associate',
        'ns': OPENID2_NS,
        'assoc_type': assoc_type,
        'session_type': session_type,
    }
    params.update(assoc_session.getRequest())
    return dict([('openid.%s' % key, value) for key, value in params.items()]), assoc_session.dh.modulus, assoc_session.dh.generator
