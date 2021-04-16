from django.contrib import admin
from games.models import childMode

# Register your models here.
from .models import Item, category

admin.site.register(category)
admin.site.register(childMode)
class admin_item(admin.ModelAdmin):
    list_display = ('name','price','description','calory_info','cat','image','pk')
    fields = ['name','price','description','calory_info','cat','image','pk']

    class Meta:
        model = Item
admin.site.register(Item, admin_item)
