from django.shortcuts import render, get_object_or_404
import random
from .models import Product

def collections(request):
    all_products = list(Product.objects.all())
    random.shuffle(all_products)  # Shuffle the list to randomize the order

    # Debugging: Print the image paths to the console
    for product in all_products:
        print(f"Product: {product.name}, Image Path: {product.image.url}")

    return render(request, 'collections.html', {'products': all_products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def contact(request):
    return render(request, 'contact.html')



