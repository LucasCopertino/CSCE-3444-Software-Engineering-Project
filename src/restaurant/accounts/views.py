from django.shortcuts import render

# Create your views here.
def customer_login(request):
    return render( request,'login.html')