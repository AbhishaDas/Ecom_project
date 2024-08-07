from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import UserInfo

class UserInfoBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(username=username)
            if check_password(password, user.password):
                return user
        except UserInfo.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserInfo.objects.get(pk=user_id)
        except UserInfo.DoesNotExist:
            return None