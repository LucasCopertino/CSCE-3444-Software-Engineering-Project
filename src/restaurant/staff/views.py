from django.shortcuts import render, redirect
from orders.models import order
from orders.forms import statusForm
def waiter_home(request):
    orders = order.objects.filter(status="finished")
    context = {
        'orders':orders
    }






    return render(request, 'waiter_notif.html', context) #page for waiter notifications

def kitchen_home(request):
    order_objs = order.objects.all()
    order_items = []
    change_stat = statusForm(instance=order_objs[0])
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
        order1 = order.objects.filter(pk=idx)[0]
        order1.status = stat
        print(order1.status)
        order1.save()
        print(order1.status)
    return redirect('kitchen_home')
