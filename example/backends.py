from django.contrib.auth.models import User
from django.db.models import Q


class ExampleBackend(object):
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
        
    def authenticate(self, username=None):
        if username is None:
            return None
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        return None
