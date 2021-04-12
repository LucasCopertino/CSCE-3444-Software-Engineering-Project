from django.shortcuts import render, get_object_or_404,redirect
from orders.models import order, Help, Refill, orderItem, Table
from orders.forms import statusForm
from accounts.models import Customer
from django.contrib import messages
from accounts.decorators import allowed_users, unauthenticated_user
from .models import pay_by_cash 
from orders.views import generate_order_id

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
    return render(request, 'manager_report.html')    #page for manager report
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

    return redirect('homepage')


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
   
    return redirect('waiter_home')

@allowed_users(allowed_roles=['waiter'])

def show_table_map(request):
    if (Table.objects.filter(occupied=True).exists()):
        table_objs = Table.objects.filter(occupied=True)
        for table_obj in table_objs:
            user_profile = Customer.objects.filter(user=table_obj.owner.user)[0]

            if order.objects.filter(owner=user_profile, delivered=False).exists():
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
    