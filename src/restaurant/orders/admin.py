from django.contrib import admin

# Register your models here.
from .models import order, orderItem, Help, Refill, Table
#display databse objects on admin site
admin.site.register(order)
admin.site.register(orderItem)
admin.site.register(Help)
admin.site.register(Refill)
admin.site.register(Table)