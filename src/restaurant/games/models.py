from django.db import models
from accounts.models import Customer

class childMode(models.Model):
    passcode = models.CharField(default='1234', null=False, max_length=4)       #to store the passcode set by the user for child mode unlock
    customer = models.OneToOneField(Customer, null=True, on_delete=models.SET_NULL) #to relate to the customer account

    def __str__(self):
        return self.customer.user.username

