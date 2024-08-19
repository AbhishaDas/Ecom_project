from django.shortcuts import render, get_object_or_404, redirect
import random
from .models import Product, Wishlist
from django.contrib.auth.decorators import login_required

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

@login_required
def add_to_wishlist(request, id):
    # if 'user_id' not in request.session:
    #     return redirect('login')
    print(f"User: {request.user}") 
    product = get_object_or_404(Product, id=id)
    user = request.user

    if not Wishlist.objects.filter(user=user, product=product).exists():
        Wishlist.objects.create(user=user, product=product)
    
    return redirect('product_detail', id=id)

@login_required
def wishlist_view(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})



