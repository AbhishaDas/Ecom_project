from django.shortcuts import render, get_object_or_404
from .models import Product
from random import sample

# Create your views here.
def collections(request):
    all_products = list(Product.objects.all())
    random_products = sample(all_products, len(all_products)) if all_products else []
    return render(request, 'collections.html', {'products': random_products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def contact(request):
    return render(request, 'contact.html')



