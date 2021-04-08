from django.shortcuts import render, get_object_or_404,redirect
from orders.models import order, Help, Refill
from orders.forms import statusForm
from accounts.models import Customer
from django.contrib import messages
def waiter_home(request):
    orders = order.objects.filter(status="finished")
    helpx = Help.objects.filter(unresolved=True)
    drink_reqs = Refill.objects.filter(unresolved=True)
    context = {
        'orders':orders,
        'help_requests':helpx,
        'drink_requests':drink_reqs,

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
    h = Help.objects.get_or_create(orderx=orderx)

    return redirect('homepage')

def delete_help_request(request):
    print(request)
    help_request_uniq = request.GET.get('pk')

    help_request,status = Help.objects.get_or_create(pk=help_request_uniq)
    help_request.unresolved = False
    help_request.resolved = True
    help_request.save()

    return redirect('waiter_home')