import urllib
import urllib2
import binascii
from openid import cryptutil
from openid import oidutil
from hashlib import sha1



    
    
def exchange_keys(url, params={}):
    data = urllib2.urlopen(urllib2.Request(url, data=urllib.urlencode(params)))
    response = data.read(1024 * 1024)
    return dict([tuple(arg.split(':', 1)) for arg in response.split()])


public_key = 'AMO8ntCnm/Q3tD02QoeFm4RysQxEZO6cofivMAjKb5qhQKXpqHLBMe4zVX7OC4wkDarGp+3kG5ypynZRu/L9CsqnZZi7fbyFKK+NhAmDhji2JaIFw5/GDXPKYFgCpgt31ohbSPnjJcuU1JRtiI2XZJKyto0m4Mr2fnj09vMkrMm3'

values = exchange_keys('https://www.google.com/a/helveticode.com/o8/ud?be=o8', params={
    'openid.mode': 'associate',
    'openid.ns': 'http://specs.openid.net/auth/2.0',
    'openid.assoc_type': 'HMAC-SHA1',
    'openid.session_type': 'DH-SHA1',
    'openid.dh_consumer_public': public_key,
})

dh_server_public = cryptutil.base64ToLong(values['dh_server_public'])
enc_mac_key = oidutil.fromBase64(values['enc_mac_key'])
modulus = 15454548
dh_shared = pow(dh_server_public, enc_mac_key, modulus)
hashed_dh_shared = sha1_module.new(cryptutil.longToBinary(dh_shared)).digest()

secret = strxor(enc_mac_key, hashed_dh_shared)

print secret
#print 'dh_server_public: ', dh_server_public
#print 'enc_mac_key: ', enc_mac_key





#dh_server_public, enc_mac_key, self.hash_func)
#print pow(dh_server_public, enc_mac_key, self.modulus)

def generate_secret():
    return ''
    
def association_associate(sender, association, **kwargs):
    if association.pk is None:
        if not association.secret_key:
            association.secret_key = generate_secret()
