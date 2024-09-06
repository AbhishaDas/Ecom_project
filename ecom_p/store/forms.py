from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Category, Product, Wishlist, Cart, Order

class CategoryForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ['name', 'image']
        
class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'quantity','in_stock']
        
class EditProductForm(forms.ModelForm):
    class Meta:
        model   = Product
        fields  = ['name', 'description', 'price', 'quantity']
        
        
class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product']
        

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['product', 'size']
        widgets = {
            'size': forms.Select(choices=[('S'), ('M'), ('L'), ('XL')]),
        }
        
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =['address']