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
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from menu import views
urlpatterns = [
    path('admin/', admin.site.urls,name='admin1'),
        path('',index, name="blank"),

    path('cart/',cart, name="cart"),
        path('finish-pay/',choose_method, name="finish-pay"),
    path('pay/', start_payment, name="pay"),
    path('pay2/',split_payment, name="pay2"),
    path('pay3/',how_many_split, name="pay3"),
    path('cash-payment/',cash_payment, name="cash"),
    path('card-payment/',card_payment, name="card"),
    path('sign-up',sign_up,name="sign_up"),

    path('login/', auth_views.LoginView.as_view, name='login'),
        path('logout/', auth_views.LogoutView.as_view, name='logout'),

        path('select-role/', index, name='index'),
    path('customer-homepage/', customer_home_page, name='customer-homepage'),
        path('homepage/', home_page, name='homepage'),

    path('accounts/',include('django.contrib.auth.urls')),
    path('categories/<int:category_id>', views.cat_g, name='categories'),
    path('menu/', menu_home, name='menu_home'), #set a path for a views.py function to be activated. eg localhost:/8000/menu/ will activate views.py's function 'menu_home'
        path('dinner/', menu_home, name='dinner_menu')
]
