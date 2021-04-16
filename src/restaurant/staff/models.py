from django.db import models
from orders.models import order
# Create your models here.


""" Overview: Database object that represents all cash payment requsests made by a customer"""
class pay_by_cash(models.Model):
    order = models.OneToOneField(order, null=True, on_delete=models.SET_NULL) #order that the pay request is associated with
    resolved = models.BooleanField(default=False)
    unresolved = models.BooleanField(default=True)
    