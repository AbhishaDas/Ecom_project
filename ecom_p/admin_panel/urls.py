from django.urls import path
from .import views

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('product_dashboard/', views.product_dashboard, name='product_dashboard')
]