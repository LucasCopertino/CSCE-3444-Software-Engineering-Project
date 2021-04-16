from django.forms import ModelForm
from .models import order
class statusForm(ModelForm):
    class Meta:
        model = order
        fields = ['status']