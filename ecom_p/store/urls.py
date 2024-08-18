from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('collections', views.collections, name='collections'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)