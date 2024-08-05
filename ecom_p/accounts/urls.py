from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.loginn, name='login'),
    path('signup/', views.signup, name='signup'),
]