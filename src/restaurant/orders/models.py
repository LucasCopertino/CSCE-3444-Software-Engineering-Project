from django.db import models
from menu.models import Item
from accounts.models import Customer
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

    items = models.ManyToManyField(orderItem)
    cost = models.DecimalField(max_digits=7,decimal_places=2, default=10.0)
    table_num = models.IntegerField( null=False, default=0)
    time = models.DateTimeField(null=True)
    total_items = models.IntegerField(default=1)
    order_id = models.CharField(max_length=50, null=False, default='abc')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    def __str__(self):
        return self.order_id
    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.Item.price*item.quantity for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.order_id)