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
from orders.views import cart
from staff.views import waiter_notif_view, kitchen_queue_view, manager_home_view, manager_report_view
from home_pages.views import index_view, customer_home_view
from games.views import snake_view, ticTacToe_view

urlpatterns = [
    path('', index_view, name='default_home'),
    path('admin/', admin.site.urls),
    path('cart/',cart, name="cart"),
    path('customer-login/', customer_login, name='customer_login'),
    path('menu/', menu_home, name='menu_home'), #set a path for a views.py function to be activated. eg localhost:/8000/menu/ will activate views.py's function 'menu_home'
    path('waiter-notifications/', waiter_notif_view, name='waiter_notifications'),
    path('customer-home/', customer_home_view, name='customer_home'),
    path('kitchen-queue/', kitchen_queue_view, name='kitchen_queue'),
    path('manager-home/', manager_home_view, name='mananger_home'),
    path('manager-report/', manager_report_view, name='manager_report'),
    path('snake/', snake_view, name='snake'),
    path('tic-tac-toe/', ticTacToe_view, name="tic_tac_toe")
]
