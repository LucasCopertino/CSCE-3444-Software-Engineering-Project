from django.contrib import admin

# Register your models here.
from .models import Item, category

admin.site.register(category)

class admin_item(admin.ModelAdmin):
    list_display = ('name','price','description','calory_info','cat')
    fields = ['name','price','description','calory_info','cat']

    class Meta:
        model = Item
admin.site.register(Item, admin_item)
