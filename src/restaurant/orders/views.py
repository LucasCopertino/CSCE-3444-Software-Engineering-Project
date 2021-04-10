from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import *
from orders.models import *
from django.contrib import messages
from menu.models import *
from staff.models import *
from django.urls import reverse
import datetime
import random
import string
import stripe
from django.http import HttpResponseRedirect, JsonResponse
from flask import jsonify
STRIPE_PUB_KEY = 'pk_test_51IMeMeCiuu3zPBMk89bXdF2Xa5iy9gJo6pEZoKmPoWSAB1QlpxuN0Cnxj2omWn0wpPHZXB3Awk42Vy0esrXXOuAd00MQ0AJkhp'
STRIPE_PRIV_KEY = 'sk_test_51IMeMeCiuu3zPBMkGAyiJKf2ABr0YmkU7DyZ3IHs0cJhIaTl7zjCGWpdirVZhRNxhKzWWhs4OQEf3zyzUeL2wkW100wiwO2OKK'
stripe.api_key = STRIPE_PRIV_KEY
# Create your views here.

def generate_order_id():
    date_str = datetime.date.today().strftime('%Y%m%d')[2:] + str(datetime.now().second)
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
    carts_customer = get_object_or_404(Customer, user=request.user)
    customer_order = get_object_or_404(order,owner=carts_customer, is_ordered=False)
    context = {
        'order':customer_order
    }  
    pay_by_cash.objects.create(order=customer_order)
    return redirect ('menu_home')

def card(request):
    return render(request, 'payment_5A_card.html')

def card_payment(request):
    carts_customer = get_object_or_404(Customer, user=request.user)
    customer_order = get_object_or_404(order,owner=carts_customer, is_ordered=False)
    context = {
        'order':customer_order
    }

    try:
        client_stripe = "pk_test_51IMeMeCiuu3zPBMk89bXdF2Xa5iy9gJo6pEZoKmPoWSAB1QlpxuN0Cnxj2omWn0wpPHZXB3Awk42Vy0esrXXOuAd00MQ0AJkhp"
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items = [
                {
                    'price_data':{
                        'currency':'usd',
                        'unit_amount':int(customer_order.cost*100),
                        'product_data':{
                            'name':customer_order.owner.user.username,
                            'images':['https://i.imgur.com/EHyR2nP.png']  ##how will we send images to stripe? do we need to create s3 buckets to store product images
                        },
                    },
                    'quantity':1
                }],
                mode='payment',
                success_url='http://127.0.0.1:8000/menu',
                cancel_url='http://localhost:8000/menu')
        customer_order.is_ordered=True
        customer_order.status='in progress'

        customer_order.save()
    except Exception as e:
        return JsonResponse(str(e), safe=False)
    return JsonResponse({'sessionId':session.id})



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
                ##asociate order with a table

        table = Table.objects.filter(owner=user_profile)[0]
        user_order.table_num = table.TableNum
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
            order_item = orderItem.objects.filter(Item=orderitem).first()
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
    rn = datetime.datetime.now()
   
    carts_customer = get_object_or_404(Customer, user=request.user)
    customer_order_items = orderItem.objects.filter(owner=carts_customer)
    customer_order = order.objects.filter(owner=carts_customer, is_ordered=False)
    context = {}
    freebie = 0
    taxx = 0.00
    for order_item in customer_order_items:
        if order_item.Item.cat.name == 'Entrees':
            freebie+=1
    freebies = []
    for i in range(freebie+1):
        freebies.append(i)
   
    if customer_order.exists():
        taxx = customer_order.first().get_tax()
        customer_order.first().cost += taxx
        customer_order.first().save()
    if rn.hour in range(16,24) and rn.weekday()==6:
        print(rn.hour)
        context = {'items':customer_order_items,'order':customer_order.first(),'tax':taxx, 'freebies':freebies, 'max':freebie}
        return render(request,'sunday_4pm_cart_page.html', context)
    else:
         context = {'items':customer_order_items,'order':customer_order.first(),'tax':taxx}
         return render(request,'cart_page.html', context)
def choose_meal(request):
    if request.method == 'GET':
        amount = request.GET.get('amount')
        print(amount)
        carts_customer = get_object_or_404(Customer, user=request.user)
        customer_order = order.objects.filter(owner=carts_customer, is_ordered=False)[0]
        if amount:
            customer_order.free_kids_meal = amount

        customer_order.save()
        print(customer_order.free_kids_meal)
    return redirect ('cart')
def choose_tip(request):
    return render(request, 'payment_1.5_tip.html')
def tip(request):
    if request.method == 'POST':
       tip_rate = request.POST.get('submit')
       cust = get_object_or_404(Customer,user=request.user)
       ordery = order.objects.filter(owner=cust,is_ordered=False)
       orderx = ordery.first()
       orderx.tip = tip_rate
       orderx.save()
       orderx.cost = orderx.add_tip()
       orderx.save()
    return redirect('cart')
def refill_drink(request):
    catt  = category.objects.filter(name="Drinks").first()
    drinks = Item.objects.filter(cat=catt)
    context = {
        'drinks':drinks
    }
    return render(request, 'drink_refill.html',context)
def refill_request(request):
    drink_pk = request.GET.get('id')
    cust = get_object_or_404(Customer, user=request.user)
    orderx = order.objects.filter(owner=cust)[0]

    drink1 = Item.objects.filter(pk=drink_pk).first()
    req = Refill.objects.get_or_create(owner=cust,drink=drink1, orderx=orderx, unresolved=True)
    return render(request, 'menu.html')

    