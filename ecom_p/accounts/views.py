from django.shortcuts import render

# Create your views here.
def loginn(request):
    return render(request, 'accounts/login.html')

def signup(request):
    return render(request, 'accounts/signup.html')