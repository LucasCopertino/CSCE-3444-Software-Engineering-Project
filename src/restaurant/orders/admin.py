from django.contrib import admin

# Register your models here.
from .models import order, orderItem

admin.site.register(order)
admin.site.register(orderItem)