from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class UserInfo(models.Model):
    first_name      = models.CharField(max_length=200)
    last_name       = models.CharField(max_length=200)
    email           = models.EmailField(unique=True)
    phone           = models.CharField(max_length=50, default='')
    username        = models.CharField(max_length=200)
    password        = models.CharField(max_length=200)
    
    
    
    def save(self, *args, **kwargs):
        if not self.pk or 'password' in self.get_dirty_fields():
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

     


