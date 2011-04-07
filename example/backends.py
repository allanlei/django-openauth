from django.conf import settings
from django.contrib.auth.models import User
from models import UserProfile

class OpenIDBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
            
    def authenticate(self, email=None, openid_id=None):
        if email and openid_id:
            try:
                user = UserProfile.objects.get(openid=openid_id).user
            except UserProfile.DoesNotExist:
                user = User.objects.create(username=email, email=email)
                profile = UserProfile.objects.create(user=user, openid=openid_id)
            return user
        return None
