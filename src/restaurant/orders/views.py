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
from django.contrib.auth.decorators import login_required
import stripe
from django.http import HttpResponseRedirect, JsonResponse
from flask import jsonify
STRIPE_PUB_KEY = 'pk_test_51IMeMeCiuu3zPBMk89bXdF2Xa5iy9gJo6pEZoKmPoWSAB1QlpxuN0Cnxj2omWn0wpPHZXB3Awk42Vy0esrXXOuAd00MQ0AJkhp'
STRIPE_PRIV_KEY = 'sk_test_51IMeMeCiuu3zPBMkGAyiJKf2ABr0YmkU7DyZ3IHs0cJhIaTl7zjCGWpdirVZhRNxhKzWWhs4OQEf3zyzUeL2wkW100wiwO2OKK'
stripe.api_key = STRIPE_PRIV_KEY
# Create your views here.


"""
Overview: Generate hashed order id by using the date and time order was created
Returns: A string containing the order id



 """
def generate_order_id():
    date_str = datetime.date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str
"""
Overview: View for starting the payment process
Returns: a html page



 """

@login_required
def start_payment(request):
    return render (request, 'payment_1_start.html')


def split_payment(request):
    return render(request, 'payment_2_split_choice.html')

def how_many_split(request):
    return render (request, 'payment_3_how_many_split.html')
"""
Overview: View for choosing the payment type
Returns: a html page

"""

@login_required
def choose_method(request):
    return render (request, 'payment_4_choose_method.html')
@login_required
def cash_payment(request):
    carts_customer = get_object_or_404(Customer, user=request.user) #get the customer by using the authentication modela and comparing with our customer model
    customer_order = get_object_or_404(order,owner=carts_customer, is_ordered=False) #get the customer's order by making use of databse relationships
    context = {
        'order':customer_order
    }  #a json object to return to our client
    #update customer reward points
    integer_cost = int(customer_order.cost)
    reward_points_for_order = 0
    for dollar in range(integer_cost):
        reward_points_for_order+=1
    carts_customer.reward_points += reward_points_for_order
    carts_customer.save()


    pay_by_cash.objects.create(order=customer_order) #create a pay by cash object in the database for the waiter to resolve 
    return redirect ('menu_home')
"""
Overview: View for starting the card payment
Returns: a html page



 """
@login_required
def card(request):
    return render(request, 'payment_5A_card.html')
"""
Overview: card the payment process
Returns: a json response to our stripe account on stripe.com 


 """
@login_required
def card_payment(request):
    carts_customer = get_object_or_404(Customer, user=request.user) #get the customer by using the authentication modela and comparing with our customer model
    customer_order_count = order.objects.filter(owner=carts_customer, is_ordered=False).count() #get the customer's order by making use of databse relationships
    if customer_order_count <=0:
        order.objects.create(owner=carts_customer, is_ordered=False, order_id=generate_order_id())
        customer_order  = order.objects.filter(owner=carts_customer, is_ordered=False)[0] #get the customer's order by making use of databse relationships

    else:
        customer_order=order.objects.filter(owner=carts_customer, is_ordered=False)[0]
    context = {
        'order':customer_order
    }  #a json object to return to our client
    customer_order_items = orderItem.objects.filter(owner=carts_customer,is_ordered=False) #get all the order items belonging to customer
    for item in customer_order_items: #for loop to change the state of the items so they are sorted 
        item.is_ordered = True #now they don't have to show up where they are not needed
        item.save()
     #update customer reward points
    integer_cost = int(customer_order.cost)
    reward_points_for_order = 0
    for dollar in range(integer_cost):
        reward_points_for_order+=1
    carts_customer.reward_points += reward_points_for_order
    carts_customer.save()
#stripe payment process
    try:
        client_stripe = "pk_test_51IMeMeCiuu3zPBMk89bXdF2Xa5iy9gJo6pEZoKmPoWSAB1QlpxuN0Cnxj2omWn0wpPHZXB3Awk42Vy0esrXXOuAd00MQ0AJkhp"
        #create stripe session and supply necessary information 
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
        customer_order.status='in progress' #change the state of the customer order for better sorting. 

        customer_order.save()
    except Exception as e:
        return JsonResponse(str(e), safe=False)
    return JsonResponse({'sessionId':session.id})

"""
Overview: increase item in cart / create an order
Returns: a json response to our stripe account on stripe.com 


 """
@login_required
def add_to_cart(request):
    if request.method == 'GET':

        # get the user profile
        user_profile = get_object_or_404(Customer, user=request.user)
        # filter products by id
        item_id = request.GET.get('id')

        orderitem = Item.objects.get(pk=item_id)
        # check if the user already owns this product

        # create orderItem of the selected product
        order_item = orderItem.objects.create(Item=orderitem)
        order_item.quantity = order_item.quantity + 1
        order_item.owner = user_profile
        order_item.cost= order_item.get_cost()
        order_item.save()
        # create order associated with the user
        user_order_count=order.objects.filter(owner=user_profile, is_ordered=False).count()
        if user_order_count<=0:
            user_order = order.objects.create(owner=user_profile, is_ordered=False)
        else:
            user_order = order.objects.filter(owner=user_profile, is_ordered=False).first()
        user_order.items.add(order_item)
        user_order.cost=user_order.get_cart_total()
                ##asociate order with a table

        table = Table.objects.filter(owner=user_profile)[0]
        user_order.table_num = table.TableNum
        taxx = user_order.get_tax()
        user_order.cost += taxx
        user_order.save()
        if user_order.order_id == 'abc':
            user_order.order_id = generate_order_id()
            user_order.save()

        #assoicate order item with order some more (create more relationships)

        order_item.order_id = user_order.order_id
        user_order.cost = user_order.get_cart_total()
        user_order.save()

        order_item.save()
        # show confirmation message and redirect back to the same page
        messages.info(request, "item added to cart")
    return render(request, 'menu.html')
"""
Overview: reduce item in cart / delete item from order
Returns: a html page


 """
@login_required
def reduce_order_item(request):
    if request.method == 'GET':

        # get the user profile
        user_profile = get_object_or_404(Customer, user=request.user)
        # filter products by id
        item_id = request.GET.get('id')
        

        orderitem = Item.objects.get(pk=item_id)
        user_order_count=order.objects.filter(owner=user_profile, is_ordered=False).count()
        if user_order_count<=0:
            user_order = order.objects.create(owner=user_profile, is_ordered=False)
        else:
            user_order = order.objects.filter(owner=user_profile, is_ordered=False).first()        

     #ensure that an order still.count()>0 for the customer
        if user_order:
            order_item_count = orderItem.objects.filter(Item=orderitem, owner=user_profile).count()
            if order_item_count <=0:
                order_item = orderItem.objects.create(Item=orderitem, owner=user_profile)
            else:
                order_item = orderItem.objects.filter(Item=orderitem, owner=user_profile).first()

            order_item.owner = user_profile #set relationships

            #reduce the item quantity and ensure negatives dont happen
            if order_item.quantity > 0:
                order_item.quantity -= 1
                order_item.cost = order_item.get_cost() #recalculate cost of the order
                order_item.save()
            else:
                order_item.delete() #if items in cart is 0 delete the item
            
            user_order.items.add(order_item)
            user_order.cost = user_order.get_cart_total()
        
            taxx = user_order.get_tax()
            user_order.cost += taxx
            user_order.save()
            print("yay debug")

        messages.info(request, "Removed from cart")
    return render(request, 'menu.html')
"""
Overview: Show customer order details 
            Perform sunday 4pm weekend deal
            get and set tax

Returns: A html page, json objects


 """
@login_required
def cart(request):
    rn = datetime.datetime.now()  #check time cart is accessed
   
    carts_customer = get_object_or_404(Customer, user=request.user)
    user_order_count=order.objects.filter(owner=carts_customer, is_ordered=False).count()
    if user_order_count<=0:
        customer_order = order.objects.create(owner=carts_customer, is_ordered=False)
    else:
        customer_order = order.objects.filter(owner=carts_customer, is_ordered=False).first()
    customer_order_items = customer_order.items.all()
    context = {}
    freebie = 0 #store number of entrees
    taxx = customer_order.get_tax() #placeholder for json object attribute 
    for order_item in customer_order_items: #search for all adult entrees in order and take count
        if order_item.Item.cat.name == 'Entrees':
            freebie+=1
    freebies = [] #list to store range of number of kids meals to select from 
    for i in range(freebie+1):
        freebies.append(i)
   
    if rn.hour in range(16,24) and rn.weekday()==6:
        print(rn.hour)
        #return different json object to client since it is a sunday at 4. Return a json object with frre kids meals information and options
        context = {'items':customer_order_items,'order':customer_order,'tax':taxx, 'freebies':freebies, 'max':freebie}
        return render(request,'sunday_4pm_cart_page.html', context)
    else:
        #retutn this json object every other day there is not a free kids meal deal
         context = {'items':customer_order_items,'order':customer_order,'tax':taxx}
         return render(request,'cart_page.html', context)
"""
Overview: Choose number of free kids meal
Returns: redirects to the cart


 """
@login_required
def choose_meal(request):
    if request.method == 'GET':
        amount = request.GET.get('amount')
        print(amount)
        carts_customer = get_object_or_404(Customer, user=request.user)
        customer_order = order.objects.filter(owner=carts_customer, is_ordered=False)[0]
        if amount:
            customer_order.free_kids_meal = amount #set number of free kids meal on order to the number sent from frontend with jQuery. This is useful in the kitchen view

        customer_order.save()
        print(customer_order.free_kids_meal)
    return redirect ('cart')

    
@login_required

def show_free_entrees(request):
    carts_customer = get_object_or_404(Customer, user=request.user)
    if (int(carts_customer.reward_points/1500)>=int(carts_customer.reward_points_activated)+1): #check if user is eleigible for rewards
        no_entrees = False
    else:
        no_entrees = True

    cat = category.objects.filter(name='Entrees')[0]
    entrees = Item.objects.filter(cat=cat)
    return render(request, 'rewards.html', {'entrees':entrees, 'customer':carts_customer,'yea':no_entrees})
@login_required
def use_reward_get_entree(request, free_entree_id):
    carts_customer = get_object_or_404(Customer, user=request.user)
    
    cat = category.objects.filter(name='Entrees')[0]
    entrees = Item.objects.filter(cat=cat)
    no_entrees = False
    if request.method == 'GET':
        print(free_entree_id)
        carts_customer = get_object_or_404(Customer, user=request.user)
        if (int(carts_customer.reward_points/1500)>=int(carts_customer.reward_points_activated)+1):
            carts_customer.reward_points_activated+=1
            carts_customer.save()
            user_order_count = order.objects.filter(owner=carts_customer, is_ordered=False).count()
            if user_order_count <=0:
                user_order =  order.objects.create(owner=carts_customer, is_ordered=False)
            else:
                user_order =  order.objects.filter(owner=carts_customer, is_ordered=False)[0]

            if free_entree_id:
                
                free_entree = Item.objects.get(pk=free_entree_id)
                # check if the user already owns this product

                # create orderItem of the selected product
                free_entree, status = orderItem.objects.get_or_create(Item=free_entree)
                free_entree.quantity = free_entree.quantity + 1
                free_entree.owner = carts_customer
                free_entree.cost= free_entree.get_cost()
                free_entree.free = True
                print("Free entree gotten")
                free_entree.save()
                # create order associated with the user
                user_order=order.objects.filter(owner=carts_customer, is_ordered=False)[0]
                user_order.items.add(free_entree)
                user_order.cost=user_order.get_cart_total()
                no_entrees = True
                
                user_order.save()
                if status:
                    # generate a reference code
                    user_order.order_id = generate_order_id()
                    user_order.save()

                #assoicate order item with order some more (create more relationships)

                free_entree.order_id = user_order.order_id
                free_entree.save()
                # show confirmation message and redirect back to the same page
        return render(request, 'rewards.html', {'entrees':entrees, 'customer':carts_customer,'yea':no_entrees})




def choose_tip(request):
    return render(request, 'payment_1.5_tip.html')
"""
Overview: card the payment process
Returns:redirect to cart

 """
@login_required
def tip(request):
    if request.method == 'POST':
       tip_rate = request.POST.get('submit')
       cust = get_object_or_404(Customer,user=request.user)
       ordery = order.objects.filter(owner=cust,is_ordered=False)
       orderx = ordery.first()
       orderx.tip = tip_rate
       orderx.save()
       orderx.cost = orderx.add_tip() #call class funcition
       orderx.save()
    return redirect('cart')


"""
Overview: Handle the tip buttons on the tip selection page
Returns:json object, html page

 """
@login_required
def tip_btns(request):
    if request.method == 'GET':
         tip_rate = request.GET.get('btnVal')
         print("tip rate is ", tip_rate)
         cust = get_object_or_404(Customer,user=request.user)
         ordery = order.objects.filter(owner=cust,is_ordered=False)       
         orderx = ordery.first()
         orderx.tip = tip_rate
         orderx.save()
         orderx.cost = orderx.add_tip() #call class funcition
         orderx.save()
         return redirect('cart')

"""
Overview: Show the refull drink page and display drinks for refill
Returns:json object, html page

 """
@login_required
def refill_drink(request):
    catt  = category.objects.filter(name="Drinks").first()
    drinks = Item.objects.filter(cat=catt)
    context = {
        'drinks':drinks
    }
    return render(request, 'drink_refill.html',context)
"""
Overview: create a refill request for the waiter view to handle
Returns:json object, html page

 """
@login_required
def refill_request(request):
    drink_pk = request.GET.get('id')
    cust = get_object_or_404(Customer, user=request.user)
    orderx = order.objects.filter(owner=cust)[0]

    drink1 = Item.objects.filter(pk=drink_pk).first()
    req = Refill.objects.get_or_create(owner=cust,drink=drink1, orderx=orderx, unresolved=True) #create a refill request or get from backend if.count()>0
    return render(request, 'menu.html')

@login_required
def free_dessert(request):
  cust = get_object_or_404(Customer, user=request.user)  
  ordery = order.objects.filter(owner=cust,is_ordered=False)[0]
  cat = category.objects.filter(name='Desserts')[0]
  print(request.GET.get('win'))
  if request.GET.get('win')=='true' and ordery.free_dessert==False: #ensure that free deserts vouchers are limited to one per order
      ordery.free_dessert = True
      ordery.save()
      order_items = orderItem.objects.filter(order_id=ordery.order_id)
      count = 10000 #set a lrage number for placeholder value. this will check if there was a dessrt in the cart
      for item in order_items:
          print(count)

          if item.Item.cat == cat and count==10000: #CHECK FOR DESSERTS IN ORDER BUT MAKE SURE USER IS LIMITED TO EXACT # OF FREE ENTREES
              ordery.cost -= item.Item.price
              ordery.save()

              print(item.cost)
              ordery.free_dessert_cost = item.Item.price
            
              ordery.save()
              count=1
          else:
              pass
      if count == 10000:
          ordery.free_dessert_hold == True
          ordery.save()
  ordery.free_dessert_tries = request.GET.get('tries')
  ordery.save()
  return redirect('cart')
@login_required

#remove a free dessert tag on an order when customer gets a free dessert
def remove_free_dessert_hold(order_id):
    cat = category.objects.filter(name='Desserts').first()
    ordery = order.objects.filter(order_id=order_id).first()
    order_items = orderItem.objects.filter(order_id=ordery.order_id)
    count = 10000 #set a lrage number for placeholder value. this will check if there was a dessrt in the cart
    if ordery.free_dessert_hold == True:
        for item in order_items:
            if item.Item.cat == cat and count<1:
                ordery.cost -= item.cost
                ordery.free_dessert_cost = item.cost
                ordery.free_dessert = True
                ordery.save()
                count=1
            else:
                pass
        ordery.free_dessert_hold = False
        ordery.save()
    else:
        pass
    """fUNCTION THAT ENABLES CUSTOMERS ADD COMMENTS TO ORDERS IN CART"""
def add_comments(request):
    if request.method == 'POST': 
       comment = request.POST.get('submit')
       cust = get_object_or_404(Customer,user=request.user)
       ordery = order.objects.filter(owner=cust,is_ordered=False)
       orderx = ordery.first()
       orderx.comments = comment
       orderx.save()
       
    return redirect('cart')
