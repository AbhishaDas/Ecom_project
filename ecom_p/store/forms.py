from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ['name', 'image']
        
class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name', 'description', 'price', 'category', 'image']
