"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from menu.views import menu_home, cat_g
from accounts.views import customer_login,sign_up
from orders.views import *
from home_pages.views import *
from games.views import *
from staff.views import *
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from menu import views
urlpatterns = [
    path('admin/', admin.site.urls,name='admin1'),
        path('',index, name="blank"),
        path('add-to-order', add_to_cart, name='add-to-order'),
        path('reduce-order-item', reduce_order_item, name='reduce-order-item'),

    path('cart/',cart, name="cart"),
        path('free-kids-meal/',choose_meal, name="free_kids_meal"),

        path('finish-pay/',choose_method, name="finish-pay"),
    path('pay/', start_payment, name="pay"),
    path('pay2/',split_payment, name="pay2"),
    path('pay3/',how_many_split, name="pay3"),
            path('choose-tip/',choose_tip, name="choose-tip"),

        path('tip/',tip, name="tip"),

    path('cash-payment/',cash_payment, name="cash"),
    path('card-payment/',card_payment, name="card"),
        path('card/',card, name="card0"),
        path('help/',HelpFunc, name="help"),

    path('sign-up',sign_up,name="sign_up"),

    path('login/', auth_views.LoginView.as_view, name='login'),
        path('logout/', auth_views.LogoutView.as_view, name='logout'),

        path('select-role/', index, name='index'),
    path('customer-homepage/', customer_home_page, name='customer-homepage'),
        path('homepage/', home_page, name='homepage'),

    path('accounts/',include('django.contrib.auth.urls')),
    path('status/',change_stat, name='change-stat'),

    path('menu/', menu_home, name='menu_home'), #set a path for a views.py function to be activated. eg localhost:/8000/menu/ will activate views.py's function 'menu_home'
    path('categories/<int:category_id>', views.cat_g, name='categories'),
    path('drink-refill', refill_drink,name='drink_refill'),
        path('drink-refill-req', refill_request,name='drink_refill_req'),

    path('games/', games_home, name='games_home'), #set path for games home page
    path('snake/', games_snake, name='games-snake'), #set path for snake
    path('tictactoe/', games_ttt, name='games-tictactoe'), #set path for tic tac toe
    path('childmode/', set_childmode, name='set-childmode'),
    path('deactivatechild/', deactivate_child, name='deactivate-child'),

    path('waiter-view/', waiter_home, name='waiter_home'), #set path for waiter notifications
    path('kitchen-view/', kitchen_home, name='kitchen_home'),    #set path for kitchen queue
    path('manager-home/', manager_home, name='manager_home'),    #set path for manager pages
    path('manager-report/', manager_report, name='manager_report'),
    path('delete-help/',delete_help_request, name="delete_help"),
    path('delete-refill/',delete_refill_request, name="delete_refill"),
    path('delete-order/',delete_order_pickup, name="delete_order"),
    path('pay-resolve/',resolve_pay_by_cash, name="resolve_cash_pay_req"),


]
