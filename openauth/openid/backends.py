from django.contrib.auth.models import User
from django.db.models import Q

from openauth.openid.models import OpenIDProfile


class OpenIDBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def create_user(self, email=None, identity=None, **kwargs):
        return User.objects.create(username=identity, email=email)

    def create_openid_profile(self, user, claimed_id=None, identity=None):
        return OpenIDProfile.objects.create(user=user, claimed_id=claimed_id, display_id=identity)
        
    def authenticate(self, email=None, claimed_id=None, identity=None):
        if email is None or claimed_id is None or identity is None:
            return None
            
        user = None
        try:
            user = User.objects.filter(Q(openidprofile__claimed_id=claimed_id) | Q(email=email)).distinct().get()
        except User.DoesNotExist:
            user = self.create_user(email=email, claimed_id=claimed_id, identity=identity)
        
        if user and not OpenIDProfile.objects.filter(user=user, claimed_id=claimed_id).exists():
            self.create_openid_profile(user, claimed_id=claimed_id, identity=identity)
        return user
