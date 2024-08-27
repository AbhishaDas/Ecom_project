from django.urls import path
from .import views


urlpatterns = [
    path('collections', views.collections, name='collections'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:id>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('cart/', views.view_cart, name='view_cart'),
    path('product/<int:id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
]