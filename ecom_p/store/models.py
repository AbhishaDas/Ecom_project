from email.mime import image
from os import name
from django.db import models
from django.contrib.auth.models import User

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
    
    def __str__(self):
        return self.name
    
    
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'

    