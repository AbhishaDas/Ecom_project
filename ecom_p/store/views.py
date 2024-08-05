from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def collections(request):
    return render(request, 'collections.html')
