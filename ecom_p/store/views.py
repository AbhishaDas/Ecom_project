from django.shortcuts import render, get_object_or_404, redirect
import random
from accounts.models import UserInfo
from .models import Product, Wishlist, Cart, User

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
    print(f"Wishlisted_product id: {id}")
    print(f"Wishlisted_product name:{product.name}")
    
    if not Wishlist.objects.filter(user=user, product=product).exists():
        Wishlist.objects.create(user=user, product=product)
        print("item added to wishlist")
    else:
        print("item already in wishlist")
    
    return redirect('product_detail', id=id)


def wishlist_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session['user_id']
    user = get_object_or_404(UserInfo, id=user_id)
    
    wishlist_items = Wishlist.objects.filter(user=user)
    
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



