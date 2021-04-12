from django.db import models
from menu.models import Item
from accounts.models import Customer
import decimal
import datetime
from django.conf import settings

# Create your models here.

STATUS_CHOICES = [('Created', 'created'), ('In progress', 'in progress'), ('Finished','finished'),('Delivered','delivered')]
"""
Overview: A database table containing the orderitems created by customers during their sessions

"""
class orderItem(models.Model):
    Item = models.OneToOneField(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False,default=0)
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    cost = models.DecimalField(max_digits=7,decimal_places=3, default=10.0)
    is_ordered = models.BooleanField(default=False)
    order_id = models.CharField(max_length=50, null=False, default='abc')
    """
        Overview: function that sets how an object is referenced by default 
        Returns: two items - a string (object's name) and an integer(quantiy of objects)
    """
    def __str__(self):
        return '{0} - {1}'.format(self.Item.name, self.quantity)
    """
        Overview: function that sets how an gets the cost of an order item based on its quantity in the order
        Returns: a decimal 
    """
    def get_cost(self):
        return self.quantity * self.Item.price
"""
Overview: A database table containing the orders created by customers during their sessions

"""    
class order(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    tip = models.DecimalField(max_digits=7,decimal_places=2, default=0.0)
    free_kids_meal =  models.IntegerField( null=False, default=0)
    delivered = models.BooleanField(default=False)
    items = models.ManyToManyField(orderItem)
    cost = models.DecimalField(max_digits=7,decimal_places=2, default=0.00)
    table_num = models.IntegerField( null=False, default=0)
    time = models.DateTimeField(auto_now_add=True, null=False)
    total_items = models.IntegerField(default=1)
    order_id = models.CharField(max_length=50, null=False, default='abc')
    status = models.CharField(max_length=50, default="ss")
    tax = models.DecimalField(max_digits=6,decimal_places=2, default=8.25)
   

    """
        Overview: function that returns all the items in cart
    """
    def get_cart_items(self):
        return self.items.all()
    """
        Overview: function that gets total cost of order
        Returns: a decimal 
    """
    def get_cart_total(self):
        return sum([item.Item.price*item.quantity for item in self.items.all()])
    """
        Overview: function that adds order tip to cost
        Returns: a decimal 
    """
    def add_tip(self):
        rate = float(decimal.Decimal(self.tip)/decimal.Decimal(100))
        tip1 = decimal.Decimal(float(self.cost)*rate)
        self.tip = tip1
        return self.cost+tip1
    """
        Overview: function that gets the tax on order
        Returns: a decimal 
    """
    def get_tax(self):
        tax1 = float(decimal.Decimal(self.tax)/decimal.Decimal(100))
        return self.cost * decimal.Decimal(tax1)
    """
        Overview: function that sets how an object is referenced by default 

    """
    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.order_id)
"""
Overview: A database table containing the help requests created by customers during their sessions

"""
class Help(models.Model):
    orderx = models.ForeignKey(order, on_delete=models.SET_NULL, null=True)
    solved = models.BooleanField(default=False)
    unresolved = models.BooleanField(default=True)
"""
Overview: A database table containing the refill requests created by customers during their sessions

"""
class Refill(models.Model):
    orderx = models.ForeignKey(order, on_delete=models.SET_NULL, null=True)

    solved = models.BooleanField(default=False)
    unresolved = models.BooleanField(default=True)  
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    drink = models.OneToOneField(Item, on_delete=models.SET_NULL, null=True)
"""
Overview: A database table containing the tables available in the restaurant
"""
class Table(models.Model):
    TableNum = models.IntegerField(null=True)
    occupied = models.BooleanField(default=False)
    owner = models.OneToOneField(Customer, null=True, on_delete=models.SET_NULL, blank=True)
    order_status = models.CharField(max_length=12, null=True, blank=True, default='browsing')
    waiter_assigned = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)