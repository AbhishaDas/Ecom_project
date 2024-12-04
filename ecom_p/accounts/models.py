from django.db import models
from django.contrib.auth.hashers import make_password

class UserInfo(models.Model):
    first_name      = models.CharField(max_length=200)
    last_name       = models.CharField(max_length=200)
    email           = models.EmailField(unique=True, null= False, blank=False)
    phone           = models.CharField(max_length=50, default='',null= False, blank=False)
    username        = models.CharField(max_length=200, null= False, blank=False)
    password        = models.CharField(max_length=200, null= False, blank=False)
    last_login      = models.DateTimeField(auto_now_add= True)
    
    class Meta:
        db_table = 'userinfo'

    def save(self, *args, **kwargs):
        if not self.pk:  # This is a new instance
            self.password = make_password(self.password)
        else:
            old_password = UserInfo.objects.get(pk=self.pk).password
            if self.password != old_password:  # Password has been changed
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

    
    @staticmethod
    def get_email_field_name():
        return 'email'
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def __str__(self):
        return self.username


