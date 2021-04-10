from django.db import models
from menu.models import Item
from accounts.models import Customer
import decimal
import datetime
# Create your models here.

STATUS_CHOICES = [('Created', 'created'), ('In progress', 'in progress'), ('Finished','finished'),('Delivered','delivered')]
class orderItem(models.Model):
    Item = models.OneToOneField(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False,default=0)
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    cost = models.DecimalField(max_digits=7,decimal_places=3, default=10.0)
    def __str__(self):
        return '{0} - {1}'.format(self.Item.name, self.quantity)
    def get_cost(self):
        return self.quantity * self.Item.price
    
class order(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    tip = models.DecimalField(max_digits=7,decimal_places=2, default=0.0)
    free_kids_meal =  models.IntegerField( null=False, default=0)
    delivered = models.BooleanField(default=False)
    items = models.ManyToManyField(orderItem)
    cost = models.DecimalField(max_digits=7,decimal_places=2, default=10.0)
    table_num = models.IntegerField( null=False, default=0)
    time = models.DateTimeField(auto_now_add=True, null=False)
    total_items = models.IntegerField(default=1)
    order_id = models.CharField(max_length=50, null=False, default='abc')
    status = models.CharField(max_length=50, default="ss")
    tax = models.DecimalField(max_digits=6,decimal_places=2, default=8.25)
    def __str__(self):
        return self.order_id
    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.Item.price*item.quantity for item in self.items.all()])
    def add_tip(self):
        rate = float(decimal.Decimal(self.tip)/decimal.Decimal(100))
        tip1 = decimal.Decimal(float(self.cost)*rate)
        self.tip = tip1
        return self.cost+tip1
    def get_tax(self):
        tax1 = float(decimal.Decimal(self.tax)/decimal.Decimal(100))
        return self.cost * decimal.Decimal(tax1)

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.order_id)
class Help(models.Model):
    orderx = models.ForeignKey(order, on_delete=models.SET_NULL, null=True)
    solved = models.BooleanField(default=False)
    unresolved = models.BooleanField(default=True)
class Refill(models.Model):
    orderx = models.ForeignKey(order, on_delete=models.SET_NULL, null=True)

    solved = models.BooleanField(default=False)
    unresolved = models.BooleanField(default=True)  
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    drink = models.OneToOneField(Item, on_delete=models.SET_NULL, null=True)
    
class Table(models.Model):
    TableNum = models.IntegerField(null=True)
    occupied = models.BooleanField(default=False)
    owner = models.OneToOneField(Customer, null=True, on_delete=models.SET_NULL, blank=True)