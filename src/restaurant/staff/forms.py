from django.forms import ModelForm
from menu.models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'description', 'calory_info', 'cat']