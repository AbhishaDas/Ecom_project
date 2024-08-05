from django.shortcuts import redirect, render


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
    return render(request, 'admin/user_dashboard.html')

def product_dashboard(request):
    return render(request, 'admin/product_dashboard.html')