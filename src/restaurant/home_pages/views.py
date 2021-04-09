from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')
@login_required
def customer_home_page(request):
    return render(request, 'login_customer_home.html')
def home_page(request):
    return render(request, 'guest_home.html')
