from django.test import TestCase
from django.urls import reverse, resolve
from menu.views import menu_home, cat_g
from menu.models import category, Item
from django.test import Client
from django.contrib.auth.models import User
from accounts.models import Customer
import datetime
from orders.models import orderItem, order, Table, Refill, Help
from django.test import RequestFactory
from staff.models import pay_by_cash
class TestViews(TestCase):
    def setUp(self):
            self.client = Client()

            category.objects.create(
                name='test category'
            )
            category.objects.create(
                name='Drinks'
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
                Item = Item.objects.filter(name='test drink')[0],
                quantity = 2,
                owner = Customer.objects.filter(user=self.user)[0],
                cost = 10.0,
                is_ordered = False,
                order_id = '12e213',
            )
            orderItem.objects.create(
                Item = Item.objects.filter(name='test item')[0],
                quantity = 2,
                owner = Customer.objects.filter(user=self.user)[0],
                cost = 10.0,
                is_ordered = True,
                order_id = '11e213',
            )
            Table.objects.create(
                TableNum = 2,
                occupied =False,
                order_status = 'browsing'
            )
            Table.objects.create(
                TableNum = 4,
                occupied =False,
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
            )
            self.n_user = User.objects.create_user(username='johdn',password='johnpassworD1!')

            order.objects.create(
            owner =  Customer.objects.filter(user=self.n_user)[0],
            is_ordered = True,
            tip = 0.0,
            free_kids_meal = 0,
            delivered = False,
            cost = 0.0,
            table_num = 2,
            time = datetime.time(),
            total_items = 2,
            order_id = '11e213',
            status = 'finished',
            tax = 8.25,
            )



            order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0].items.set(orderItem.objects.filter(Item=Item.objects.filter(name='test item')[0]))
            Refill.objects.create(
                owner =  Customer.objects.filter(user=self.user)[0],
                drink = Item.objects.filter(name='test drink')[0],
                orderx =  order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0],
                unresolved =True


            )
            Help.objects.create(
                orderx=  order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0]
            )
            pay_by_cash.objects.create(
                order=order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0]

            )

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')  
    
    def test_customer_home_page(self):
        response = self.client.get(reverse('customer-homepage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_customer_home.html')  
    def test_home_page(self):
        response = self.client.get(reverse('homepage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'guest_home.html')     
    def test_select_table(self):
        response = self.client.get(reverse('select_table'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'select_table.html')  
    def test_table_selection(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('table-selection'), data={'table_id':2})
        self.assertEquals(response.status_code, 302)   
    def test_logOut(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('free_table'))
        self.assertEquals(response.status_code, 302)   


 