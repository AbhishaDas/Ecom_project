from email.mime import image
from os import name
from django.db import models

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
    