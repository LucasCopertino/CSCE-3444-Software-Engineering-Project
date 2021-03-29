from django.shortcuts import render, get_object_or_404
from accounts.models import *
from orders.models import *
from django.contrib import messages
from menu.models import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date,datetime
import random
import string
# Create your views here.

def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str

def cart(request):
    return render( request,'cart_page.html')

def start_payment(request):
    return render (request, 'payment_1_start.html')


def split_payment(request):
    return render(request, 'payment_2_split_choice.html')

def how_many_split(request):
    return render (request, 'payment_3_how_many_split.html')

def choose_method(request):
    return render (request, 'payment_4_choose_method.html')
def cash_payment(request):
    return render(request, 'payment_5B_cash.html')

def card_payment(request):
    return render(request, 'payment_5A_card.html')


def add_to_cart(request):
    if request.method == 'GET':

        # get the user profile
        user_profile = get_object_or_404(Customer, user=request.user)
        # filter products by id
        item_id = request.GET.get('id')

        orderitem = Item.objects.get(id=item_id)
        # check if the user already owns this product
    
        # create orderItem of the selected product
        order_item, status = orderItem.objects.get_or_create(Item=orderitem)
        order_item.quantity = order_item.quantity + 1
        order_item.owner = user_profile
        order_item.cost= order_item.get_cost()
        order_item.save()
        # create order associated with the user
        user_order, status = order.objects.get_or_create(owner=user_profile, is_ordered=False)
        user_order.items.add(order_item)
        user_order.cost=user_order.get_cart_total()
        user_order.save()
        if status:
            # generate a reference code
            user_order.order_id = generate_order_id()
            user_order.save()
       
        # show confirmation message and redirect back to the same page
        messages.info(request, "item added to cart")
    return render(request, 'menu.html')
def reduce_order_item(request):
    if request.method == 'GET':

        # get the user profile
        user_profile = get_object_or_404(Customer, user=request.user)
        # filter products by id
        item_id = request.GET.get('id')

        orderitem = Item.objects.get(id=item_id)
        print("yay debug")

        if order.objects.filter(owner=user_profile)[0].items.filter(Item=orderitem).exists():
            order_item = orderItem.objects.filter(Item=orderitem)[0]
            order_item.owner = user_profile

            if order_item.quantity > 0:
                order_item.quantity -= 1
                order_item.cost = order_item.get_cost()
                order_item.save()
            else:
                order_item.delete()
        user_order, status = order.objects.get_or_create(owner=user_profile, is_ordered=False)
        user_order.items.add(order_item)
        user_order.cost = user_order.get_cart_total()
        user_order.save()
        messages.info(request, "Removed from cart")
    return render(request, 'menu.html')

def cart(request):
    carts_customer = get_object_or_404(Customer, user=request.user)
    customer_order_items = orderItem.objects.filter(owner=carts_customer)
    customer_order = order.objects.filter(owner=carts_customer, is_ordered=False)
    context = {}

    if customer_order.exists():
        context = {'items':customer_order_items,'order':customer_order[0] }
        print("h")
    return render(request,'cart_page.html', context)

def checkout(request):
    x = 0