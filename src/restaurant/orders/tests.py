# Create your tests here.
from django.test import TestCase
from django.urls import reverse, resolve
from menu.views import menu_home, cat_g
from menu.models import category, Item
from django.test import Client
from django.contrib.auth.models import User
from accounts.models import Customer
import datetime
from orders.models import orderItem, order, Table, Refill

# Create your tests here.
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        category.objects.create(
            name='test category'
        )
        category.objects.create(
            name='Drinks'
        )
        category.objects.create(
            name='Desserts'
        )
        Item.objects.create(
            name='test item',
            price =5.00,
            description = "test",
            calory_info =40,
            cat =category.objects.filter(name='test category')[0],

        )
        Item.objects.create(
            name='test ittem',
            price =5.00,
            description = "test",
            calory_info =40,
            cat =category.objects.filter(name='test category')[0],

        )
        Item.objects.create(
            name='test drink',
            price =5.00,
            description = "test",
            calory_info =40,
            cat =category.objects.filter(name='Drinks')[0],

        )
        self.user= User.objects.create_user(username='johnnn',password='johnpassworD1!')

        orderItem.objects.create(
            Item = Item.objects.filter(name='test item')[0],
            quantity = 2,
            owner = Customer.objects.filter(user=self.user)[0],
            cost = 10.0,
            is_ordered = False,
            order_id = '12e213',
        )
        orderItem.objects.create(
            Item = Item.objects.filter(name='test ittem')[0],
            quantity = 2,
            owner = Customer.objects.filter(user=self.user)[0],
            cost = 10.0,
            is_ordered = False,
            order_id = '12e213',
        )
        orderItem.objects.create(
            Item = Item.objects.filter(name='test drink')[0],
            quantity = 2,
            owner = Customer.objects.filter(user=self.user)[0],
            cost = 10.0,
            is_ordered = False,
            order_id = '12e213',
        )
        Table.objects.create(
            TableNum = 2,
            occupied =True,
            owner =  Customer.objects.filter(user=self.user)[0],
            order_status = 'browsing'
        )
        order.objects.create(
        owner =  Customer.objects.filter(user=self.user)[0],
        is_ordered = False,
        tip = 0.0,
        free_kids_meal = 0,
        delivered = False,
        cost = 0.0,
        table_num = 2,
        time = datetime.time(),
        total_items = 2,
        order_id = '12e213',
        status = 'ss',
        tax = 8.25,
        free_dessert_tries=0,
        )



        order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0].items.set(orderItem.objects.filter(Item=Item.objects.filter(name='test item')[0]))
        Refill.objects.create(
            owner =  Customer.objects.filter(user=self.user)[0],
            drink = Item.objects.filter(name='test drink')[0],
            orderx =  order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0],
            unresolved =True

        )
        #all django test functions must be prefixed with 'test_'
    def test_start_payment_test(self):
    
        response = self.client.get(reverse('pay'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment_1_start.html')   
    def test_split_payment_test(self):
    
        response = self.client.get(reverse('pay2'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment_2_split_choice.html')   
    def test_how_many_split_payment_test(self):
    
        response = self.client.get(reverse('pay3'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment_3_how_many_split.html')   

    def test_choose_method(self):
        response = self.client.get(reverse('finish-pay'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment_4_choose_method.html')
    def test_cash_payment(self):
        self.client.force_login(user=self.user)

       
        test_order = order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0]
        response = self.client.get(reverse('cash'))
        self.assertEquals(response.status_code, 302) #check for code 302 since function redirects to a diffeent url
    def test_card(self):
        response = self.client.get(reverse('card0'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,  'payment_5A_card.html')   
    def test_card_payment(self):
        self.client.force_login(user=self.user)

       
        response = self.client.get(reverse('card'))
        self.assertEquals(response.status_code, 200)

    def test_add_to_cart(self):
        self.client.force_login(user=self.user)
        
        response = self.client.get(reverse('add-to-order'),data={'id':Item.objects.filter(name='test ittem')[0].pk})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,  'menu.html')   

  
    def test_cart(self):
        self.client.force_login(user=self.user)   
        response = self.client.get(reverse('cart'))
        self.assertEquals(response.status_code, 200)
    def test_choose_meal(self):
        self.client.force_login(user=self.user)
        
        response = self.client.get(reverse('free_kids_meal'),data={'amount':2})
        self.assertEquals(response.status_code, 302)
    def test_tip_and_tip_btns(self):
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('tip'),data={'submit':5})
        self.assertEquals(response.status_code, 302)
    def test_refill_drink(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('drink_refill'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,  'drink_refill.html') 

    def test_refill_request(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('drink_refill_req'),data={'id':Item.objects.filter(name='test drink')[0].pk})
        self.assertTemplateUsed(response,  'menu.html')   
    def test_free_dessert(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('free_dessert'), data={'tries':order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0].free_dessert_tries})
        self.assertEquals(response.status_code, 200)
    def test_reduce_order_item(self):
        self.client.force_login(user=self.user)    
        response = self.client.get(reverse('reduce-order-item'),data={'id':Item.objects.filter(name='test ittem')[0].pk})
        self.assertEquals(response.status_code, 302)

