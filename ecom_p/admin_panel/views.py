from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from accounts.models import UserInfo
from accounts.forms import EditUserForm
from store.models import Category, Product
from store.forms import CategoryForm, ProductForm


admin_username = 'admin'
admin_password = 'admin123'

def admin_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == admin_username and password == admin_password:
            return redirect('dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid usename or password'})
    return render(request, 'admin/admin_login.html')

def dashboard(request):
    return render(request, 'admin/dashboard.html')

def user_dashboard(request):
    query = request.GET.get('q')
    if query:
        user_details = UserInfo.objects.filter(
            first_name__icontains=query) | UserInfo.objects.filter(
            last_name__icontains=query) | UserInfo.objects.filter(
            email__icontains=query) | UserInfo.objects.filter(
            username__icontains=query) | UserInfo.objects.filter(
            phone=query)
    else:
        user_details = UserInfo.objects.all()
        
    return render(request, 'admin/user_dashboard.html', {'users': user_details})

def manage_user(request, user_id):
    user = get_object_or_404(UserInfo, pk=user_id)
    if request.POST:
        if 'save' in request.POST:
            frm = EditUserForm(request.POST, instance=user)
            if frm.is_valid():
                frm.save()
                return redirect('user_dashboard')
        elif 'delete' in request.POST:
            user.delete()
            return redirect('user_dashboard')
    else:
        
        frm = EditUserForm(instance=user)
    
    return render(request, 'admin/manage_user.html', {'frm': frm, 'user': user})

def product_dashboard(request):
    return render(request, 'admin/product_dashboard.html')

def add_category(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_category')
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category.html', {'categories':categories, 'form':form})

def add_product(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_product')
    else:
        form = ProductForm()
    return render(request, 'admin/add_product.html', {'products': products, 'form':form})