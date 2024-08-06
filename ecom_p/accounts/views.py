from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import UserInfo
from django.db import IntegrityError

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                auth_login(request, user)  # Log in the user immediately after sign up
                request.session['user_id'] = user.id  # Store user ID in session
                return redirect('home')  # Redirect to home page
            except IntegrityError as e:
                if 'UNIQUE constraint failed: accounts_userinfo.email' in str(e):
                    form.add_error('email', 'This email address is already in use.')
    else:
        form = UserForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            request.session['user_id'] = user.id  # Store user ID in session
            return redirect('home')  # Redirect to home page
        else:
            error = 'Invalid username or password'
            return render(request, 'accounts/login.html', {'error': error})
    
    return render(request, 'accounts/login.html')


def index(request):
    user = None
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            user = UserInfo.objects.get(pk=user_id)
        except UserInfo.DoesNotExist:
            user = None

    return render(request, 'index.html', {'user': user})


def logout(request):
    auth_logout(request)  # Logout the user
    return redirect('login')
