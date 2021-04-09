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
        path('finish-pay/',choose_method, name="finish-pay"),
    path('pay/', start_payment, name="pay"),
    path('pay2/',split_payment, name="pay2"),
    path('pay3/',how_many_split, name="pay3"),
    path('cash-payment/',cash_payment, name="cash"),
    path('card-payment/',card_payment, name="card"),
        path('card/',card, name="card0"),

    path('sign-up',sign_up,name="sign_up"),

    path('login/', auth_views.LoginView.as_view, name='login'),
        path('logout/', auth_views.LogoutView.as_view, name='logout'),

        path('select-role/', index, name='index'),
    path('customer-homepage/', customer_home_page, name='customer-homepage'),
        path('homepage/', home_page, name='homepage'),

    path('accounts/',include('django.contrib.auth.urls')),

    path('menu/', menu_home, name='menu_home'), #set a path for a views.py function to be activated. eg localhost:/8000/menu/ will activate views.py's function 'menu_home'
    path('categories/<int:category_id>', views.cat_g, name='categories'),

    path('games/', games_home, name='games_home'), #set path for games home page
    path('snake/', games_snake, name='games-snake'), #set path for snake
    path('tictactoe/', games_ttt, name='games-tictactoe'), #set path for tic tac toe
    path('childmode/', set_childmode, name='set-childmode'),
    path('childmode-error1/', childmode_invalid, name='childmode-invalid'),
    path('childmode-error2/', childmode_matcherror, name='childmode-matcherror'),
    path('deactivatechild/', deactivate_child, name='deactivate-child'),
    path('deactivatechild-error/', deactivate_child_error, name='deactivate-child-error'),
    path('games-locked/', games_home_locked, name='games-home-locked'),
    path('snake-locked/', games_snake_locked, name='games-snake-locked'),
    path('tictactoe-locked/', games_ttt_locked, name='games-tictactoe-locked'),

    path('waiter-view/', waiter_home, name='waiter_home'), #set path for waiter notifications
    path('kitchen-view/', kitchen_home, name='kitchen_home'),    #set path for kitchen queue
    path('manager-home/', manager_home, name='manager_home'),    #set path for manager pages
    path('manager-report/', manager_report, name='manager_report')
]
