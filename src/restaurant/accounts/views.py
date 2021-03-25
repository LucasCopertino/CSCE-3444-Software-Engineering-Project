
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


#sign up view
def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return render(request,'accounts/home_pages/index.html')
    context['form']=form
    return render(request,'sign_up.html',context)


# Create your login view here.
def customer_login(request):
    return render( request,'login.html')
