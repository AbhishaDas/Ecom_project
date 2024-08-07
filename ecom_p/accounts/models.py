from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class UserInfo(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    last_login = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # This is a new instance
            self.password = make_password(self.password)
        else:
            old_password = UserInfo.objects.get(pk=self.pk).password
            if self.password != old_password:  # Password has been changed
                self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

    @property
    def backend(self):
        return 'accounts.backends.UserInfoBackend'
