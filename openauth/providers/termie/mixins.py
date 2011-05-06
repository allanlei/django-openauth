class OAuthRequestTokenMixin(object):
    oauth_request_endpoint = 'http://term.ie/oauth/example/request_token.php'

class OAuthAuthorizeTokenMixin(object):
    pass

class OAuthAccessTokenMixin(object):
    oauth_access_endpoint = 'http://term.ie/oauth/example/access_token.php'
    
    def get_oauth_token(self):
        """
        term.ie doesn't require authorization of request token so just upgrade to access straight away
        """
        return self.get_oauth_request_token()
