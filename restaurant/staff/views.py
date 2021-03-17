from django.shortcuts import render

# Create your views here.
def waiter_notif_view(request):
    return render(request, 'waiter_notif.html')

def kitchen_queue_view(request):
    return render(request, 'kitchen_queue.html')

def manager_home_view(request):
    return render(request, 'manager_home.html')

def manager_report_view(request):
    return render(request, 'manager_report.html')