from django.shortcuts import render, get_object_or_404, redirect
import random
from accounts.models import UserInfo
from .models import Product, Wishlist, Cart, Order
from django.http import Http404, HttpResponse
from django.contrib import messages
from .forms import CheckoutForm
import paypalrestsdk
from django.conf import settings

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
    if request.method == 'POST':
        # Fetch the required product_id from the cart or session
        product_id = request.POST.get('product_id')  # Ensure product_id is available in the POST request
        product = Product.objects.get(id=product_id)
        
        if product:
            # Get the billing and shipping details from the form
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = request.POST.get('zip')

            # Example: You can calculate total amount, assuming you have product.price
            total_amount = product.price
            
            # Create the order object
            order = Order.objects.create(
                product=product,
                user=request.user,  # assuming the user is logged in
                address=address,
                amount=total_amount,
                status="pending"
            )

            return redirect('order_confirmation')

        else:
            return HttpResponse("Product not found", status=404)

    return render(request, 'checkout.html')


paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def create_paypal_payment(request):
    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute/",
                "cancel_url": "http://localhost:8000/payment/cancel/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Item Name",
                        "sku": "item",
                        "price": "10.00",
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": "10.00",
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]})

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            print(payment.error)
    return render(request, 'checkout.html')

def execute_paypal_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return redirect('payment_success')
    else:
        return redirect('payment_failed')