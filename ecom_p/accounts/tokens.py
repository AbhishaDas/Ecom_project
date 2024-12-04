# tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserInfoTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + user.email  # Customizing to work with UserInfo model

# Create a global instance of this generator
user_info_token_generator = UserInfoTokenGenerator()
