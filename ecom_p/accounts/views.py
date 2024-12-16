from django.shortcuts import render, redirect, get_object_or_404
from .forms import EditProfileForm, UserForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import UserInfo
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from store.models import Product
import random
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from .tokens import user_info_token_generator
from django.utils.http import urlsafe_base64_encode


def signup(request):
    if 'user_id' in request.session:
        return redirect('home')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save() 
                return redirect('login')  
            except IntegrityError as e:
                if 'UNIQUE constraint failed: accounts_userinfo.email' in str(e):
                    form.add_error('email', 'This email address is already in use.')
    else:
        form = UserForm()
    
    return render(request, 'accounts/signup.html', {'form': form})



def loginn(request):
    if 'user_id' in request.session:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = UserInfo.objects.get(username=username)
            if check_password(password, user.password):  # Use check_password to verify password
                request.session['user_id'] = user.id  # Store user ID in session
                return redirect('home')
            else:
                error = 'Invalid username or password'
        except UserInfo.DoesNotExist:
            error = 'Invalid username or password'
    
        return render(request, 'accounts/login.html', {'error': error})
    
    return render(request, 'accounts/login.html')



def index(request):
    user = None
    user_id = '*' 
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        if user_id is None:
            user_id = '*'
        try:
            user = UserInfo.objects.get(pk=user_id)
        except UserInfo.DoesNotExist:
            user = None
            
    all_products = list(Product.objects.all())
    random.shuffle(all_products)  # Shuffle the list to randomize the order
    selected_products = all_products[:12]  # Select only the first 12 products
    
    if user:
        print(f"Username: {user.username}")
    else:
        print("No user is logged in or user not found.")

    return render(request, 'index.html', {'user': user, 'user_id':user_id, 'products': selected_products})


def logout(request):
    if 'user_id' in request.session:
        request.session.flush()
    return redirect('login')


def profile(request, user_id):
    user = get_object_or_404(UserInfo, pk=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user_id)
    else:
            form = EditProfileForm(instance=user)   
    return render(request, 'accounts/profile.html', {'form':form, 'user_id':user_id})

def orders(request):
    return render(request, 'orders.html')




def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Get the user by email
            user = UserInfo.objects.get(email=email)
            
            # Encode the user ID in base64
            uidb64 = urlsafe_base64_encode(str(user.pk).encode())  # Ensure base64 encoding
            
            # Generate the token
            token = default_token_generator.make_token(user)

            # Create the reset link
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            )

            # Send the email with the reset link
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_url}',
                'your-email@example.com',
                [user.email]
            )
            return redirect('password_reset_done')
        except UserInfo.DoesNotExist:
            return redirect('password_reset_done')
    return render(request, 'accounts/password_reset_request.html')




def password_reset_confirm(request, uidb64, token):
    try:
        # Decode the base64-encoded user ID
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode and convert to string
        user = UserInfo.objects.get(pk=uid)

        # Validate the token
        if not default_token_generator.check_token(user, token):
            return redirect('password_reset_done')

    except (TypeError, ValueError, OverflowError, UserInfo.DoesNotExist):
        return redirect('password_reset_done')

    if request.method == 'POST':
        # Update the password
        new_password = request.POST.get('new_password')
        user.password = make_password(new_password)  # Use make_password for hashing
        user.save()
        return redirect('password_reset_complete')

    return render(request, 'accounts/password_reset_confirm.html', {'user': user, 'token': token})



def password_reset_confirm(request, uidb64, token):
    try:
        # Decode the base64-encoded user ID
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode and convert to string
        user = UserInfo.objects.get(pk=uid)

        # Validate the token
        if not default_token_generator.check_token(user, token):
            return redirect('password_reset_done')

    except (TypeError, ValueError, OverflowError, UserInfo.DoesNotExist):
        return redirect('password_reset_done')

    if request.method == 'POST':
        # Update the password
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        return redirect('password_reset_complete')

    return render(request, 'accounts/password_reset_confirm.html', {'user': user, 'token': token})



def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')



def password_reset_complete(request):
    return render(request, 'accounts/password_reset_complete.html')


    