from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users

# Create your views here.
def index(request):
    return render(request, 'index.html')
@login_required(login_url='/login/')
def customer_home_page(request):
    return render(request, 'login_customer_home.html')
def home_page(request):
    return render(request, 'guest_home.html')
