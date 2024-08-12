from django.shortcuts import render
from .models import Product
from random import sample

# Create your views here.
def collections(request):
    # Fetch all products
    all_products = list(Product.objects.all())
    
    # Shuffle the list to get a random order
    random_products = sample(all_products, len(all_products)) if all_products else []
    return render(request, 'collections.html', {'products': random_products})

def product_detail(request):
    return render(request, 'product_detail.html')



