from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from openauth.openid.backends import OpenIDBackend as OIDBackend
from openauth.openid.models import OpenIDProfile

class OpenIDBackend(OIDBackend):
    def authenticate(self, return_to=None, openid=None):
        try:
            self.validate(return_to, openid)
        except ValidationError, ex:
            print ex
            return None
        
        user = None
        try:
            user = OpenIDProfile.objects.get(claimed_id=openid['openid.claimed_id']).user
        except OpenIDProfile.DoesNotExist:
            user = User.objects.create(username=openid['openid.identity'])
            OpenIDProfile.objects.create(user=user, claimed_id=openid['openid.claimed_id'], display_id=openid['openid.identity'])
        return user


class EmailBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def authenticate(self, email=None):
        if email:
            user = None
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            return user
