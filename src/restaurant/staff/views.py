from django.shortcuts import render, get_object_or_404,redirect
from orders.models import order, Help, Refill, orderItem
from orders.forms import statusForm
from accounts.models import Customer
from django.contrib import messages
from .models import pay_by_cash 
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

def kitchen_home(request):
    order_objs = order.objects.filter(status='in progress')
    order_items = []
    change_stat = statusForm(instance=order_objs.first())
    for s in order_objs:
       order_items.append(s.items.all())

    
    context = {
        'orders':order_objs,
        'items':order_items,
        'change_status': change_stat,

    }
    return render(request, 'kitchen_queue.html', context) #page for kitchen queue

def manager_home(request):
    return render(request, 'manager_home.html') #page for manager home

def manager_report(request):
    return render(request, 'manager_report.html')    #page for manager report
def change_stat(request):
    if request.method == 'GET':
        idx= request.GET.get('pk')
        stat = request.GET.get('stat')
        order1 = order.objects.filter(pk=idx).first()
        order1.status = stat
        print(order1.status)
        order1.save()
        print(order1.status)
    return redirect('kitchen_home')

def HelpFunc(request):
 
    cust = get_object_or_404(Customer, user=request.user)
    orderx = order.objects.filter(owner=cust)[0]
    h = Help.objects.get_or_create(orderx=orderx, unresolved=True)

    return redirect('homepage')

def delete_help_request(request):
    print(request)
    help_request_uniq = request.GET.get('pk')

    help_request,status = Help.objects.get_or_create(pk=help_request_uniq)
    help_request.unresolved = False
    help_request.resolved = True
    help_request.save()

    return redirect('waiter_home')
def delete_refill_request(request):
    print(request)
    ref_request_uniq = request.GET.get('pk')
    ref_request, status = Refill.objects.get_or_create(pk=ref_request_uniq)
    ref_request.unresolved = False
    ref_request.resolved = True
    ref_request.save()
    return redirect('waiter_home')

def delete_order_pickup(request):
    print(request)
    order_request_uniq = request.GET.get('pk')
    order_request, status = order.objects.get_or_create(pk=order_request_uniq)
    order_request.delivered = True
    order_request.save()
    return redirect('waiter_home')
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
