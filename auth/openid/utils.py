from openid.message import OPENID2_NS, OPENID1_NS
     

def getAssociationRequestParams(endpoint, assoc_type, session_type):
    session_class = DiffieHellmanSHA1ConsumerSession()
    assoc_session = session_class()
    
    params = {
        'ns': ''
        'mode': 'associate',
        'assoc_type': assoc_type,
    }
    params.update(assoc_session.getRequest())
    return params
