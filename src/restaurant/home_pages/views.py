from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')
@login_required(login_url='/customer-login/')
def customer_home_page(request):
    return render(request, 'customer_home.html')
