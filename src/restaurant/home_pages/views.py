from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Table
from accounts.models import Customer
# Create your views here.
def index(request):
    return render(request, 'index.html')
@login_required(login_url='/login/')
def customer_home_page(request):
    return render(request, 'login_customer_home.html')
def home_page(request):
    return render(request, 'guest_home.html')
def select_table(request):
    table_objs = Table.objects.filter(occupied=False)
    context = {
        'tables':table_objs
    }
    return render(request,'select_table.html',context)
   
def table_selection(request):
    user_profile = get_object_or_404(Customer, user=request.user)

    if request.method=='GET' and request.GET.get('table_id')!=None :
        table_objs = Table.objects.filter(occupied=False)

        table_id = request.GET.get('table_id')
        table = table_objs.filter(TableNum = table_id)[0]
        table.occupied = True
        table.owner = user_profile
        print(table.TableNum)
        table.save()
        return redirect('select_table')