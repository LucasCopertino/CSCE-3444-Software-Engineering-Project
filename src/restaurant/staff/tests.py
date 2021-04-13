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
from .models import pay_by_cash
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
            #all django test functions must be prefixed with 'test_'
    def test_waiter_home(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('waiter_home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'waiter_notif.html')  
    def test_kitchen_home(self):
        response = self.client.get(reverse('kitchen_home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'kitchen_queue.html')
    def test_manager_home(self):
        response = self.client.get(reverse('manager_home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager_home.html')
    def test_manager_report(self):
        response = self.client.get(reverse('manager_report'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager_report.html')
    def test_change_stat(self):
        response = self.client.get(reverse('change-stat'), data={'pk':order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0].pk,'stat':'in progress'})
        self.assertEquals(response.status_code, 302)
    def test_HelpFunc(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('help'))

        self.assertEquals(response.status_code, 302)
    def test_delete_help_request(self):
        response = self.client.get(reverse('delete_help'), data={'pk':Help.objects.filter(orderx= order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0])[0].pk})
        self.assertEquals(response.status_code, 302)
    
    def test_delete_refill_request(self):
        response = self.client.get(reverse('delete_help'), data={'pk':Refill.objects.filter(orderx= order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0])[0].pk})
        self.assertEquals(response.status_code, 302)

    def test_delete_order_pickup(self):
        response = self.client.get(reverse('delete_order'), data={'pk':order.objects.filter(owner=Customer.objects.filter(user=self.n_user)[0],is_ordered=True,delivered=False)[0].pk})
        self.assertEquals(response.status_code, 302)

    def test_resolve_pay_by_cash(self):
        response = self.client.get(reverse('resolve_cash_pay_req'), data={'pk':order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0].pk})
        self.assertEquals(response.status_code, 302)

    def test_show_table_map(self):
        response = self.client.get(reverse('table_map'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'waiter_table_map.html')        
