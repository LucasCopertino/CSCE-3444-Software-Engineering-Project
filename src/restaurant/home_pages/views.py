from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Table
from accounts.models import Customer
from accounts.decorators import allowed_users

# Create your views here.
def index(request):
    return render(request, 'index.html')

"""Overview:Home page view for authenticated customer
    Return:  html page 
"""
@login_required(login_url='/login/')

def customer_home_page(request):
    return render(request, 'login_customer_home.html')
"""Overview:Home page view for unauthenticated customer
    Return: html page 
"""
def home_page(request):
    

    return render(request, 'guest_home.html')


"""Overview:Page to select table number after login
    Return: json object, html page 
"""
def select_table(request):
    table_objs = Table.objects.filter(occupied=False)
    context = {
        'tables':table_objs
    }
    return render(request,'select_table.html',context)


"""Overview:Function to handle table selection 
    Return:reload page
"""  
def table_selection(request):
    user_profile = get_object_or_404(Customer, user=request.user)

    if request.method=='GET' and request.GET.get('table_id')!=None : #check type of request coming from jquery
        table_objs = Table.objects.filter(occupied=False)

        table_id = request.GET.get('table_id')
        table = table_objs.filter(TableNum = table_id)[0]
        table.occupied = True #make table occupied and remove from selection 
        table.owner = user_profile #asiign table to customer
        print(table.TableNum)
        table.save()
        return redirect('select_table')

"""Overview:Function to free user's tables and log out user
    Return: to the guest homepage
"""  

def logOut(request):
    person = request.user
    if Customer.objects.filter(user=person).exists:
        if Table.objects.filter(owner=Customer.objects.filter(user=person)[0], occupied=True).exists():
            tables = Table.objects.filter(owner=Customer.objects.filter(user=person)[0], occupied=True)
            for table in tables:
                table.occupied = False
                table.owner = None
                table.save()
    return redirect('logout')