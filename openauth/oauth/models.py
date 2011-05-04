from django.db import models
from django.contrib.auth.models import User

import managers

import datetime
import time


class OAuthToken(models.Model):
    token = models.CharField(max_length=1024, blank=True)
    secret = models.CharField(max_length=1024, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
    def is_valid(self):
        return False
        

class OAuthUnauthorizedToken(OAuthToken):
    objects = managers.OAuthUnauthorizedTokenManager()

class OAuthAuthorizedToken(OAuthToken):
    objects = managers.OAuthAuthorizedTokenManager()

class OAuthAccessToken(OAuthToken):
    objects = managers.OAuthAccessTokenManager()
