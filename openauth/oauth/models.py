from django.db import models
from django.contrib.auth.models import User

import datetime

class OAuthProfile(models.Model):
    user = models.ForeignKey(User)
    
    access_key = models.TextField(max_length=2048, unique=True)
    access_secret= models.TextField(max_length=2048, blank=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    expires = models.DateTimeField(null=True)
    
    def __unicode__(self):
        return self.access_token
    
    @property
    def access_token(self):
        return u''





class OAuthToken(models.Model):
    UNAUTHORIZED_REQUEST_TOKEN = 'unauthorized_request_token'
    AUTHORIZED_REQUEST_TOKEN = 'authorized_request_token'
    ACCESS_TOKEN = 'access_token'
    TOKEN_TYPES = [UNAUTHORIZED_REQUEST_TOKEN, AUTHORIZED_REQUEST_TOKEN, ACCESS_TOKEN]
    
    token_type = models.CharField(max_length=64, choices=[(token, token) for token in TOKEN_TYPES], default=UNAUTHORIZED_REQUEST_TOKEN)
    key = models.TextField()
    secret = models.TextField(blank=True)
    
    
    def token(self):
        return ''
    
    def upgrade(self):
        return
