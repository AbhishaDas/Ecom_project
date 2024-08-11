from pyexpat import model
from django import forms
from django.forms import ModelForm
from .models import UserInfo

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autocorrect': 'off', 'autocapitalize': 'none'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        }
        
class EditProfileForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'email', 'phone']
        
        widgets = {
            'email': forms.EmailInput(attrs={
                'autocorrect': 'off', 
                'autocapitalize': 'none'
            }),
        }
    

class EditUserForm(ModelForm):
    class Meta:
        model = UserInfo
        exclude = ['username', 'password']
