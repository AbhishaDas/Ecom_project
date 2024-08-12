from django.urls import path
from .import views

urlpatterns = [
    path('collections', views.collections, name='collections'),
    path('product/', views.product_detail, name='product_detail'),
    path('product_detail', views.product_detail, name='product_detail'),
]