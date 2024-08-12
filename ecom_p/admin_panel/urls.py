from django.urls import path
from .import views

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('manage_user/<int:user_id>/', views.manage_user, name='manage_user'),
    path('product_dashboard/', views.product_dashboard, name='product_dashboard'),
    path('add_category/', views.add_category, name='add_category'),
    path('manage_product/', views.manage_product, name='manage_product'),
]