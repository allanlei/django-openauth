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
