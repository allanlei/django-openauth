from auth.openid.backends import OpenIDBackend as OIDBackend

class OpenIDBackend(OIDBackend):
    def authenticate(self, return_to=None, openid=None):
        try:
            self.validate(return_to, openid)
        except OpenIDValidationError, err:
            return None
        print 'OKAY'
        return None
