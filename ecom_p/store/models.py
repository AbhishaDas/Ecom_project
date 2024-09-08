from ctypes import addressof, sizeof
from email.mime import image
from itertools import product
from math import prod
from os import name
from django.db import models
from django.contrib.auth.models import User
import uuid

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
    quantity    = models.PositiveIntegerField(default=1)
    date_added  = models.DateTimeField(auto_now_add=True)
    size        = models.CharField(max_length=10)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    user             = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    order_id         = models.CharField(max_length=50, unique=True, default=uuid.uuid4, editable=False)
    address          = models.TextField()
    amount           = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status   = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date       = models.DateTimeField(auto_now_add=True)
    product        = models.ManyToManyField(Product, through='OrderProduct')
    
    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
    
class Payment(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.order_id} by {self.user.username}"
    
    
    

    