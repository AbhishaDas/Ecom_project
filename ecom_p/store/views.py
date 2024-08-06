from django.shortcuts import render

# Create your views here.
def collections(request):
    return render(request, 'collections.html')
