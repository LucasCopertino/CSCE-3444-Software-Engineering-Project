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
from django.urls import path
from menu.views import menu_home
from accounts.views import customer_login
from orders.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/',cart, name="cart"),
        path('finish-pay/',choose_method, name="cart"),
    path('pay/', start_payment, name="cart"),
    path('pay2/',split_payment, name="cart"),
    path('pay3/',how_many_split, name="cart"),
    path('cash-payment/',cash_payment, name="cart"),
    path('card-payment/',card_payment, name="cart"),

    path('customer-login/', customer_login, name='customer_login'),
    path('menu/', menu_home, name='menu_home') #set a path for a views.py function to be activated. eg localhost:/8000/menu/ will activate views.py's function 'menu_home'
]
