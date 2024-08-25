from django.shortcuts import render, get_object_or_404, redirect
import random
from accounts.models import UserInfo
from .models import Product, Wishlist, Cart, User
from django.http import Http404

def collections(request):
    all_products = list(Product.objects.all())
    random.shuffle(all_products)  # Shuffle the list to randomize the order

    context = {
        'products': all_products,  # Add the products to the context
        'user_id': request.session.get('user_id')  # Add user_id to the context
    }

    return render(request, 'collections.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    
    user_id = request.session.get('user_id')  # Retrieve user_id from session
    print(f"User ID in product_detail view: {user_id}")  # Debugging line
    
    context = {
        'product': product,
        'user_id': user_id
    }

    return render(request, 'product_detail.html', context)

def contact(request):
    context = {
        'user_id': request.session.get('user_id')
    }
    return render(request, 'contact.html', context)



def add_to_wishlist(request, id):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    print(f"Wishlisted_user:{user_id}")
    user = get_object_or_404(UserInfo, id=user_id)
    
    product = get_object_or_404(Product, id=id)
    
    if not Wishlist.objects.filter(user=user, product=product).exists():
        Wishlist.objects.create(user=user, product=product)
    
    return redirect('product_detail', id=id)


def wishlist_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session['user_id']
    user = get_object_or_404(UserInfo, id=user_id)
    
    wishlist_items = Wishlist.objects.filter(user=user)
    
    if request.method == 'POST' and 'delete' in request.POST:
        product_id = request.POST.get('product_id')
        print(f"Product ID received: {product_id}")
        
        try:
            product = Product.objects.get(id=product_id)
            Wishlist.objects.filter(user=user, product=product).delete()
            return redirect('wishlist')
        except Product.DoesNotExist:
            print(f"No Product matches the ID: {product_id}")
            raise Http404("Product not found")
        
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items, 'user':user})


def view_cart(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session['user_id']
    user = get_object_or_404(UserInfo, id=user_id)
    
    cart_items = Cart.objects.filter(user=user)
    return render(request, 'cart.html', {'cart_items':cart_items, 'user':user})

 
def add_to_cart(request, id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session['user_id']
    user = get_object_or_404(UserInfo, id=user_id)
    product = get_object_or_404(Product, id=id)
    if not Cart.objects.filter(user=user, product=product).exists():
        Cart.objects.create(user=user, product=product)
    return redirect('product_detail', id=id)
 
def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')



