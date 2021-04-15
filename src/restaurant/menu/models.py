from django.db import models

##
#Create models i.e tables in the database we are using

"""necessaary class for sorting menu items"""
class category(models.Model):
    name = models.CharField(default='abc', null=False, max_length=32)
    def __str__(self): 
        return self.name 

"""menu items in databse"""
class Item(models.Model):
    name = models.CharField(default='abc', null=False, max_length=32)
    price = models.DecimalField(decimal_places=2, max_digits=4, default=5.00)
    description = models.CharField(default='abc', null=False, max_length=200)
    image = models.ImageField(null=True, blank=False)
    calory_info = models.IntegerField(default=50)
    cat = models.ForeignKey(category, on_delete=models.SET_NULL, null=True)

    def __str__(self): 
        return self.name 


