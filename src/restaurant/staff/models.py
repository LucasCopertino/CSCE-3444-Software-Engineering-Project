from django.db import models
from orders.models import order
# Create your models here.
class pay_by_cash(models.Model):
    order = models.OneToOneField(order, null=True, on_delete=models.SET_NULL)
    resolved = models.BooleanField(default=False)
    unresolved = models.BooleanField(default=True)
    