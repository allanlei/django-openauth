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
