from email import message
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EditProfileForm, UserForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import UserInfo
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password

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
            user = UserInfo.objects.get (username = username)
            if check_password(password, user.password):
                auth_login(request, user)
                request.session['user_id'] = user.id 
                return redirect('home')
            else:
                error = 'Invalid username or password'
 
        except UserInfo.DoesNotExist:
            error = 'Invalid username or password'
    
        return render(request, 'accounts/login.html', {'error':error})
    
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

    return render(request, 'index.html', {'user': user, 'user_id':user_id})


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
    