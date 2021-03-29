from django.shortcuts import render

def waiter_home(request):
    return render(request, 'waiter_notif.html') #page for waiter notifications

def kitchen_home(request):
    return render(request, 'kitchen_queue.html') #page for kitchen queue

def manager_home(request):
    return render(request, 'manager_home.html') #page for manager home

def manager_report(request):
    return render(request, 'manager_report.html')    #page for manager report
