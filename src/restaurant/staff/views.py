from django.shortcuts import render, get_object_or_404,redirect
from orders.models import order, Help, Refill, orderItem, Table
from orders.forms import statusForm
from accounts.models import Customer
from django.contrib import messages
from accounts.decorators import allowed_users, unauthenticated_user
from .models import pay_by_cash 
from orders.views import generate_order_id
from .forms import ItemForm
from menu.models import Item
import datetime
""" Overview: A function to that manages the waiter's home page
    Returns: Json objects, html page
"""


@allowed_users(allowed_roles=['waiter'])
def waiter_home(request):
    orders = order.objects.filter(status="finished",delivered=False)
    helpx = Help.objects.filter(unresolved=True)
    drink_reqs = Refill.objects.filter(unresolved=True)
    pay_reqs = pay_by_cash.objects.filter(unresolved=True)
    context = {
        'orders':orders,
        'help_requests':helpx,
        'drink_requests':drink_reqs,
        'pay_requests':pay_reqs
    }

    return render(request, 'waiter_notif.html', context) #page for waiter notifications

""" Overview: A function to that manages the kitchen's home page
    Returns: Json objects, html page
"""


@allowed_users(allowed_roles=['kitchen'])
def kitchen_home(request):
    order_objs = order.objects.filter(status='in progress')
    order_items = []
    change_stat = statusForm(instance=order_objs.first()) #a form to change the status of an order that is in progress
    for s in order_objs:
        if len(s.items.all()) > 0:
            order_items.append(s.items.all())

    
    context = {
        'orders':order_objs,
        'items':order_items,
        'change_status': change_stat,

    }
    return render(request, 'kitchen_queue.html', context) #page for kitchen queue

@allowed_users(allowed_roles=['manager'])
def manager_home(request):
    return render(request, 'manager_home.html') #page for manager home

@allowed_users(allowed_roles=['manager'])
def manager_report(request):
    orderItems = orderItem.objects.all()#retrieves all the info from every item in orderItems
    orders= order.objects.all()#retrieves all the info from every item in orders
    today = datetime.datetime.now()

    order_items = []
    tax=0#calculate tax for the day
    tips=0#calculate tips for the day
    total=0#calculates total revenue for the day
    cost=0#calculated order costs for the day
    for i in orders: #for loop that calculates the cost of tax, tips, and meals if it was ordered today
        if today.month == i.time.month and today.day == i.time.day and today.year == i.time.year:
            order_items.append(i.items.all())
            tax+=i.get_tax()
            tips+=i.tip
            cost+=i.cost
    #for i in orderItems:
    #    q=i.quantity*i.cost
    #    cost+=q
    total = tax+tips+cost
    return render(request, 'manager_report.html', {'orderItems':orderItems, 'orders':orders, 'tax':tax, 'tips':tips, 'cost':cost, 'total':total, 'order_items':order_items})

@allowed_users(allowed_roles=['kitchen'])
def change_stat(request):
    if request.method == 'GET':
        idx= request.GET.get('pk')
        stat = request.GET.get('stat') #receive change rewquest from frontend with jQuery and process here
        order1 = order.objects.filter(pk=idx).first()
        order1.status = stat #change status of object to status ent from frontend
        print(order1.status)
        order1.save()
        print(order1.status)
    return redirect('kitchen_home')


""" Overview: A function to that handles help request made by a customer
    Returns:customer to the homepage
"""
def HelpFunc(request):
 
    cust = get_object_or_404(Customer, user=request.user)
    orderx = order.objects.get_or_create(owner=cust)[0]
    orderx.order_id = generate_order_id()
    orderx.save()
    h = Help.objects.get_or_create(orderx=orderx, unresolved=True)

    return redirect('customer-homepage')

def HelpFuncLocked(request):                                #if the games page is locked, it will redirect back to the games page locked instead
    cust = get_object_or_404(Customer, user=request.user)
    orderx = order.objects.get_or_create(owner=cust)[0]
    orderx.order_id = generate_order_id()
    orderx.save()
    h = Help.objects.get_or_create(orderx=orderx, unresolved=True)

    return redirect('games-home-locked')

""" Overview: A function to that handles help request aand allows waiters resolve them
    Returns:reloads the page
"""
@allowed_users(allowed_roles=['waiter'])

def delete_help_request(request):
    print(request)
    help_request_uniq = request.GET.get('pk')

    help_request,status = Help.objects.get_or_create(pk=help_request_uniq)
    help_request.unresolved = False
    help_request.resolved = True
    help_request.save()

    return redirect('waiter_home')


""" Overview: A function to that handles refill request aand allows waiters resolve them
    Returns:reloads the page
"""
@allowed_users(allowed_roles=['waiter'])

def delete_refill_request(request):
    print(request)
    ref_request_uniq = request.GET.get('pk')
    ref_request, status = Refill.objects.get_or_create(pk=ref_request_uniq)
    ref_request.unresolved = False
    ref_request.resolved = True
    ref_request.save()
    return redirect('waiter_home')



""" Overview: A function to that allows waiters resolve completed orders
    Returns:reloads the page
"""
@allowed_users(allowed_roles=['waiter'])

def delete_order_pickup(request):
    print(request)
    order_request_uniq = request.GET.get('pk')
    order_request, status = order.objects.get_or_create(pk=order_request_uniq)
    order_request.delivered = True
    order_request.save()
    return redirect('waiter_home')


""" Overview: A function to that allows waiters resolve cash payment requests
    Returns:reloads the page
"""
@allowed_users(allowed_roles=['waiter'])

def resolve_pay_by_cash(request):
    order_request_uniq = request.GET.get('pk')
    order_request, status = pay_by_cash.objects.get_or_create(pk=order_request_uniq)
    order_request.resolved = True
    order_request.unresolved = False
    order_request.order.is_ordered = True
    order_request.order.status = 'in progress'

    customer_profile = order_request.order.owner
    for item in orderItem.objects.filter(owner=customer_profile):
        item.is_ordered = True
        item.save()
    order_request.order.save()  
    order_request.save()  
    order.objects.create(owner=customer_profile, order_id=generate_order_id())
    
    return redirect('waiter_home')

@allowed_users(allowed_roles=['waiter'])
def show_table_map(request):
    if (Table.objects.filter(occupied=True).count()>0):
        table_objs = Table.objects.filter(occupied=True)
        for table_obj in table_objs:
            user_profile = Customer.objects.filter(user=table_obj.owner.user)[0]

            if order.objects.filter(owner=user_profile, delivered=False).count()>0:
                order1 = order.objects.filter(owner=user_profile, delivered=False)[0]
                if order1.is_ordered == False:
                    table_obj.order_status = "browsing"
                else:
                    table_obj.order_status = "In Kitchen"
                if order1.status=="finished":
                    table_obj.order_status = "Ready for delivery"

                table_obj.save()
        context = {
            'tables':table_objs
        }
        return render(request, 'waiter_table_map.html', context)
    
    
    else:
        return render(request, 'waiter_table_map.html')
    
def createItem(request):        #allows manager to create an item
    form = ItemForm()           #gets all attributes of the menu item from models
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/manager-menu')#change to whatever page we want after creating new item
    context={'form':form}
    return render(request, 'create_item.html', context)

def updateItem(request, pk):        #allows manager to update an item. uses create item but shows all of the fields with current info of the item
    item = Item.objects.get(id=pk)
    form = ItemForm(instance=item)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('/manager-menu')#change to whatever page we want after creating new item
    context={'form':form}
    return render(request, 'create_item.html', context)

def manager_menu(request):  #displays all menu items to manager with an update/delete button for each item and a create item button
    items = Item.objects.all() #put all food items in database in this single variable
    context = {'itms':items}
    return render(request, 'manager_menu.html',context) 

def deleteItem(request, pk):    #delete function for menu items
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('/manager-menu')
    context = {'item':item}
    return render(request, 'delete.html', context)
