from django.shortcuts import render, get_object_or_404, redirect
import random
from accounts.models import UserInfo
from .models import Product, Wishlist, Cart, Order
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from uuid import uuid4
import uuid
from decimal import Decimal
from django.db.models import Q
import stripe
from django.http import JsonResponse




def collections(request):
    products = Product.objects.all()

    category_filter = request.GET.get('category')
    search_query = request.GET.get('search', '')
    
    if category_filter:
        products = products.filter(category__name__iexact=category_filter)  

    sort_by = request.GET.get('sort_by')
    if sort_by == 'low_to_high':
        products = products.order_by('price') 
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')
        
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(category__name__icontains=search_query)
        )

    context = {
        'products': products,
        'user_id': request.session.get('user_id')
    }

    return render(request, 'collections.html', context)

def product_detail(request, id):
    if 'user_id' not in request.session:
        return redirect('login')

    product = get_object_or_404(Product, id=id)
    user_id = request.session.get('user_id')

    cart_item = Cart.objects.filter(user_id=user_id, product=product).first()
    wishlist_item = Wishlist.objects.filter(user_id=user_id, product=product).exists()

    size_in_cart = cart_item.size if cart_item else None
    is_in_cart = cart_item is not None
    is_in_wishlist = wishlist_item

    if request.method == "POST":
        selected_size = request.POST.get('size', None)
        
        if selected_size is None:
            context = {
                'product': product,
                'size_in_cart': size_in_cart,
                'is_in_cart': is_in_cart,
                'is_in_wishlist': is_in_wishlist,
                'error_message': "Please select a size before adding to cart."
            }
            return render(request, 'product_detail.html', context)
        
        if not is_in_cart or selected_size != size_in_cart:
            Cart.objects.create(user_id=user_id, product=product, size=selected_size)
            return redirect('view_cart')

    context = {
        'product': product,
        'size_in_cart': size_in_cart,
        'is_in_cart': is_in_cart,
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'product_detail.html', context)



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
    
    messages.success(request, 'Product added to Wishlist')
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
    sub_total = sum(item.product.price*item.quantity for item in cart_items)
    shipping_cost = 0
    total = sub_total + shipping_cost
    return render(request, 'cart.html', {'cart_items':cart_items, 'user':user, 'sub_total':sub_total, 'shipping_cost':shipping_cost,'total':total})

def update_cart_quantity(request, id, action):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session['user_id']
    user = get_object_or_404(UserInfo, id=user_id)
    cart_item = get_object_or_404(Cart, id=id, user=user)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        # Handle cases where quantity cannot be decreased (e.g., minimum quantity of 1)
        pass
    
    cart_item.save()
    return redirect('view_cart')
 
def add_to_cart(request, id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session['user_id']
    user = get_object_or_404(UserInfo, id=user_id)
    product = get_object_or_404(Product, id=id)
    selectedSize = request.POST.get('size')
    
    cart_item = Cart.objects.filter(user=user, product=product, size=selectedSize).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = Cart.objects.create(user=user, product=product, size=selectedSize)
        
    messages.success(request, 'Product added to Cart')    
    return redirect('product_detail', id=id)


 
def remove_from_cart(request, id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session['user_id']
    user = get_object_or_404(UserInfo, id=user_id)
    product = get_object_or_404(Product, id=id)

    if request.method =='POST' and 'delete' in request.POST:
        Cart.objects.filter(user=user, product=product).delete()
        return redirect('view_cart')


def checkout_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id)

    if request.method == "POST":
        # Just gather the order details, don't create the order yet.
        full_name = request.POST.get('firstname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        full_address = f"{address}, {city}, {state}, {zip_code}"

        cart_items = Cart.objects.filter(user=user)

        sub_total = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
        shipping_cost = Decimal(0)
        total = sub_total + shipping_cost

        # Store the necessary data temporarily in session until payment is confirmed.
        request.session['order_data'] = {
            'full_address': full_address,
            'amount': float(total),
            'user_id': user_id,
            'cart_items': [item.id for item in cart_items],  # Storing cart item IDs temporarily
        }

        return redirect(reverse('payment') + "?amount={}".format(total))

    else:
        cart_items = Cart.objects.filter(user=user)

        sub_total = sum(item.product.price * item.quantity for item in cart_items)
        shipping_cost = 0
        total = sub_total + shipping_cost

        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'sub_total': sub_total,
            'shipping_cost': shipping_cost,
            'total': total
        })


stripe.api_key = settings.STRIPE_SECRET_KEY

def payment(request):
    if request.method == 'POST':
        try:
            amount = int(request.POST.get('amount', 0)) * 100  # Convert ₹ to paise
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='inr',
                payment_method_types=['card'],
            )
            return JsonResponse({'client_secret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return render(request, 'payment.html', {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

    
    
def order_confirm(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id)

    if request.method == 'GET':

        order_data = request.session.get('order_data')
        if not order_data:
            return redirect('payment')


        order = Order.objects.create(
            user=user,
            order_id=uuid.uuid4(),
            address=order_data['full_address'],
            amount=Decimal(order_data['amount']),
            payment_status='Pending' 
        )

        cart_items = Cart.objects.filter(id__in=order_data['cart_items'])
        for item in cart_items:
            item.delete() 
        request.session.pop('order_data', None)

        return render(request, 'order_confirm.html', {
            'user': user,
            'order': order,
            'amount': order_data['amount']
        })

    return render(request, 'order_confirm.html')    

def order_summary(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'order_summary.html', {
        'order': order
    })