
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group

"""Overview: Function to sign new customers up"""
#sign up view
def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None) #form instance to recevive data from potential customer
    if request.method == "POST": #validate that request is posting to the backend
        if form.is_valid():
            user = form.save()
            login(request,user)
            group=Group.objects.get(name='customer') #add account to the customer role for least permissions
            user.groups.add(group)
            return render(request,'login_customer_home.html')
    context['form']=form
    return render(request,'sign_up.html',context)


# Create your login view here.
def customer_login(request):
    return render( request,'login.html')
