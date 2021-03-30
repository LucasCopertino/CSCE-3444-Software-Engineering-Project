from django.shortcuts import render
from orders.models import order
def waiter_home(request):
    return render(request, 'waiter_notif.html') #page for waiter notifications

def kitchen_home(request):
    order_objs = order.objects.all()
    order_items = []
    for s in order_objs:
       order_items.append(s.items.all())

   
    context = {
        'orders':order_objs,
        'items':order_items
    }
    return render(request, 'kitchen_queue.html', context) #page for kitchen queue

def manager_home(request):
    return render(request, 'manager_home.html') #page for manager home

def manager_report(request):
    return render(request, 'manager_report.html')    #page for manager report
