from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('manage_user/<int:user_id>/', views.manage_user, name='manage_user'),
    path('product_dashboard/', views.product_dashboard, name='product_dashboard'),
    path('add_category/', views.add_category, name='add_category'),
    path('manage_product/<int:product_id>', views.manage_product, name='manage_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('manage_product/', views.manage_product, name= 'manage_product'),
    path('order_info/', views.order_info, name='order_info'),
    path('banner_admin/', views.banner_admin, name="banner_admin"),
    path('dashboard/', views.progress_graph, name='signup_progress'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)