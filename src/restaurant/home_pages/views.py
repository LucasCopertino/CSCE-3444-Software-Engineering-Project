from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Table, order
from accounts.models import Customer
from accounts.decorators import allowed_users
import datetime
import random
import string
"""
Overview: Generate hashed order id by using the date and time order was created
Returns: A string containing the order id



 """
def generate_order_id():
    date_str = datetime.date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second) #GET THE DATE AND TIME FOR ID GENERATION
    rand_str = "".join([random.choice(string.digits) for count in range(3)]) #ADD RANDOMIZATION 
    return date_str + rand_str

# Create your views here.
def index(request):
    return render(request, 'index.html')

"""Overview:Home page view for authenticated customer
    Return:  html page 
"""
#@login_required

def customer_home_page(request):
    #create a cart for the customer after login 
    carts_customer = get_object_or_404(Customer, user=request.user)
    if order.objects.filter(owner=carts_customer, is_ordered=False).count()>0: #CHECK IF USER;S ORDER EXISTS AND AT A TABLE
        if Table.objects.filter(owner=carts_customer).count()<=0:
            order.objects.filter(owner=carts_customer, is_ordered=False).first().table_num=Table.objects.filter(owner=carts_customer).first().TableNum
        pass
    else:
        if Table.objects.filter(owner=carts_customer).count()>0: #IF USER NOT ASSIGNED TO A TABLE, CREATE A NEW ORDER ASSIGN TABLE USER SELECTED WHEN USER FOR LOGGED IN

            order.objects.create(owner=carts_customer, table_num=Table.objects.filter(owner=carts_customer).first().TableNum, order_id=generate_order_id())
        

    return render(request, 'login_customer_home.html')
"""Overview:Home page view for unauthenticated customer
    Return: html page 
"""
def home_page(request):
    

    return render(request, 'guest_home.html')

#@login_required
"""Overview:Page to select table number after login
    Return: json object, html page 
"""
def select_table(request):
    person = request.user
    if Customer.objects.filter(user=person).count()>0: 
        cust = Customer.objects.filter(user=person).first()
        if Table.objects.filter(owner=cust).count()>0: #IF USER ALREADY ASSIGNED TO TABLE GO TO HOMEPAGE
            print("table num is",Table.objects.filter(owner=cust).first().TableNum)
            return redirect('customer-homepage')
        else:#IF USER NOT ASSIGNED TO RENDER HTML VIEW WITH OPTIONS TO SELECT ONE
            table_objs = Table.objects.filter(occupied=False)#DISPLAY ONLY UNOCCUPIED TABLES
            context = {
                'tables':table_objs
            }
            return render(request,'select_table.html',context) #VIEW TO SELECT TABLE
    else:
        redirect('login')

#@login_required
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
        return render(request, 'login_customer_home.html')       

"""Overview:Function to free user's tables and log out user
    Return: to the guest homepage
"""  

def logOut(request):
    person = request.user
    if Customer.objects.filter(user=person).count()>0:
        if Table.objects.filter(owner=Customer.objects.filter(user=person)[0], occupied=True).count()>0: #CHECK FOR USERS TABLE
            tables = Table.objects.filter(owner=Customer.objects.filter(user=person)[0], occupied=True) #UNASSIGN USER FROM TABLE
            for table in tables:
                table.occupied = False
                table.owner = None
                table.save()
    return redirect('logout')