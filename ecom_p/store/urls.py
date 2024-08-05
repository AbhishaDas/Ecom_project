from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='home'),
    path('collections', views.collections, name='collections'),
]