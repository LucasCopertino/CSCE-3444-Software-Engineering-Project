from django.contrib import admin

# Register your models here.
from .models import order, orderItem, Help, Refill

admin.site.register(order)
admin.site.register(orderItem)
admin.site.register(Help)
admin.site.register(Refill)