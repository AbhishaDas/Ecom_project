from django.urls import path
from .import views


urlpatterns = [
    path('collections', views.collections, name='collections'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:id>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]