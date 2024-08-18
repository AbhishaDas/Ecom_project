from django.shortcuts import render, get_object_or_404, redirect
import random
from .models import Product, Wishlist

def collections(request):
    all_products = list(Product.objects.all())
    random.shuffle(all_products)  # Shuffle the list to randomize the order
        
    for product in all_products:
        print(f"Product: {product.name}, Image Path: {product.image.path}")

    return render(request, 'collections.html', {'products': all_products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def contact(request):
    return render(request, 'contact.html')

from django.contrib.auth.decorators import login_required

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        # Optionally, handle the case where the item is already in the wishlist
        pass
    return redirect('wishlist_view')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


