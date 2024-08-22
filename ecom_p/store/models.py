from ctypes import sizeof
from email.mime import image
from math import prod
from os import name
from django.db import models
from django.contrib.auth.models import User

from accounts.models import UserInfo

# Create your models here.
class Category(models.Model):
    name        = models.CharField(max_length=100)
    image       = models.ImageField(upload_to='category/')
    
    def __str__(self):
        return self.name
 
    
class Product(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    category    = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image       = models.ImageField(upload_to='products/')
    quantity    = models.IntegerField(default=1)
    in_stock    = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.in_stock = True
        else:
            self.in_stock = False
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
        

class Wishlist(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
    
class Cart(models.Model):
    user        = models.ForeignKey(UserInfo, on_delete=models.CASCADE)        
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.PositiveIntegerField(default=0)
    date_added  = models.DateTimeField(auto_now_add=True)
    size        = models.CharField(max_length=10)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    

    