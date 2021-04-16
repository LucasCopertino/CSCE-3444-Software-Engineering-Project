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
from .models import childMode


"""Overview: This is a test web server with a test database that we'll use to test all our backend logic."""
class TestViews(TestCase):
    """Function that sets up our server"""
    def setUp(self):
        self.client = Client()  #create dummy web client for requests 

#This block creates dummy items in our dummy database
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
        
        self.user= User.objects.create_user(username='john',password='johnpassworD1!')

        orderItem.objects.create(
            Item = Item.objects.filter(name='test item')[0],
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
        )
        self.n_user = User.objects.create_user(username='johdn',password='johnpassworD1!')

        order.objects.filter(owner=Customer.objects.filter(user=self.user)[0])[0].items.set(orderItem.objects.filter(Item=Item.objects.filter(name='test item')[0]))
        childMode.objects.create(
            customer = Customer.objects.filter(user=self.n_user)[0],
            passcode = 3243
        )

        

    def test_games_home(self):#TESTINT THE GAMES HOME VIEW AND URL
        response = self.client.get(reverse('games_home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Games_Page.html')   
    def test_games_home_guest(self):#TESTINT THE GUEST GAMES HOME VIEW AND URL
        response = self.client.get(reverse('games-home-guest'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Games_Page_Guest.html')    
    def test_games_home_locked(self):#TESTINT THE LCOKED GAMES HOME VIEW AND URL - CHILDMODE
        response = self.client.get(reverse('games-home-locked'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Games_Page_Locked.html') 
    def test_games_snake(self):#TESTINT THE SNAKE GAME VIEW AND URL
        response = self.client.get(reverse('games-snake'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snake.html')  
    def test_games_snake_locked(self):#TESTINT THE LOCKED SNAKE GAME VIEW AND URL - CHILDMODE
        response = self.client.get(reverse('games-snake-locked'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snake_locked.html')  
    def test_game_ttt(self):#TESTINT THE TICTACTOE GAME VIEW AND URL
        response = self.client.get(reverse('games-tictactoe'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tictactoe.html')  
    def test_games_ttt_locked(self):#TESTINT THE LOCKED TICTACTOE GAME VIEW AND URL - CHILDMODE
        response = self.client.get(reverse('games-tictactoe-locked'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tictactoe_locked.html')    
    def test_set_childmode(self):#TESTING SETTING CHILDMODE PASSWORD
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('set-childmode'),data={'att1':3243, 'att2':3243})
        self.assertEquals(response.status_code, 302)
    def test_deactivate_child(self):#TESTING DEACTIVATING CHILDMODE FOR USER
        self.client.force_login(user=self.n_user)
        response = self.client.post(reverse('deactivate-child'),data={'attempt':3243})
        self.assertEquals(response.status_code, 302)
