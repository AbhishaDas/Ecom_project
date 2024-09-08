from django.urls import path
from .import views
from .views import create_paypal_payment, execute_paypal_payment


urlpatterns = [
    path('collections', views.collections, name='collections'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:id>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('cart/', views.view_cart, name='view_cart'),
    path('product/<int:id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('payment/paypal/', create_paypal_payment, name='create_paypal_payment'),
    path('payment/execute/', execute_paypal_payment, name='execute_paypal_payment'),
    path('payment/', views.create_paypal_payment, name='create_paypal_payment'),
    path('payment/execute/', views.execute_paypal_payment, name='execute_paypal_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
]