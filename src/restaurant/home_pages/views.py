from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')
def customer_home_page(request):
    return render(request, 'customer_home.html')
