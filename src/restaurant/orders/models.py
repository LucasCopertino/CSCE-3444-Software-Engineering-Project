from django.db import models
from menu.models import Item
# Create your models here.

STATUS_CHOICES = [('Created', 'created'), ('In progress', 'in progress'), ('Finished','finished'),('Delivered','delivered')]
class order(models.Model):
    table_num = models.IntegerField( null=False, default=0)
    time = models.DateTimeField()
    total_items = models.IntegerField(default=1)
    Item = models.ManyToManyField(Item)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    order_id = models.IntegerField(null=True)
    def __str__(self):
        return self.order_id