from django.shortcuts import redirect, render, get_object_or_404
from accounts.models import UserInfo
from accounts.forms import EditUserForm
from store.models import Category, Order, Product
from store.forms import CategoryForm, ProductForm, EditProductForm
import hashlib
from django.core.files.base import ContentFile
from .models import Banner
from .forms import BannerForm


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

def admin_logout(request):
    if 'user_id' in request.session:
        request.session.flush()
    return redirect('admin_login')

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
    query = request.GET.get('q')
    if query:
        product_details = Product.objects.filter(
            name__icontains = query)|Product.objects.filter(
            category__name__contains = query)
    else:
        product_details = Product.objects.all()
    return render(request, 'admin/product_dashboard.html',{'products':product_details})

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


def manage_product(request):
    products = Product.objects.all()
    if request.method == 'POST':
        if 'delete' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return redirect('manage_product')
        else:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid(): 
            #hashing the image
                image = form.cleaned_data['image']
                if image:
                    image_content = image.read() 
                    image_hash = hashlib.sha256(image_content).hexdigest() 
                    image_name = f"{image_hash}.{image.name.split('.')[-1]}"
                    image_file = ContentFile(image_content)
                    form.instance.image.save(image_name, image_file)
            
                form.save()
                return redirect('manage_product')
    else:
        form = ProductForm()
        
    return render(request, 'admin/manage_product.html', {'products': products, 'form':form})

def edit_product(request,id):
    product = get_object_or_404(Product, id=id)
    if request.POST:
        if 'save' in request.POST:
            form = EditProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect('product_dashboard')
        elif 'delete' in request.POST:
            product.delete()
            return redirect('product_dashboard')
    else:
        form = EditProductForm(instance=product)
    
    return render(request, 'admin/edit_product.html', {'form':form, 'product':product})
        
        
def order_info(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(order_id=order_id)

        new_order_status = request.POST.get('order_status')
        if new_order_status:
            order.order_status = new_order_status

        new_payment_status = request.POST.get('payment_status')
        if new_payment_status:
            order.payment_status = new_payment_status

        order.save()

        return redirect('order_info')

    order_details = Order.objects.all()
    return render(request, 'admin/order_info.html', {'orders': order_details})



def banner_admin(request):
    banner = Banner.objects.first()  # Assuming you manage one banner
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect("banner_admin")  # Reload the page
    else:
        form = BannerForm(instance=banner)
    return render(request, "admin/banner_admin.html", {"form": form})
