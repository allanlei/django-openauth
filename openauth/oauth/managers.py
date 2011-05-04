from django.db import models

class OAuthUnauthorizedTokenManager(models.Manager):
    pass

class OAuthAuthorizedTokenManager(models.Manager):
    pass

class OAuthAccessTokenManager(models.Manager):
    pass
