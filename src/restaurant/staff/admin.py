from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(pay_by_cash)  #display all pay by cash objects in admin