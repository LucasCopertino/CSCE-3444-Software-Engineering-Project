from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

import stripe
STRIPE_PUB_KEY = 'pk_test_51IMeMeCiuu3zPBMk89bXdF2Xa5iy9gJo6pEZoKmPoWSAB1QlpxuN0Cnxj2omWn0wpPHZXB3Awk42Vy0esrXXOuAd00MQ0AJkhp'
STRIPE_PRIV_KEY = 'sk_test_51IMeMeCiuu3zPBMkGAyiJKf2ABr0YmkU7DyZ3IHs0cJhIaTl7zjCGWpdirVZhRNxhKzWWhs4OQEf3zyzUeL2wkW100wiwO2OKK'
stripe.api_key = STRIPE_PRIV_KEY
# Create your models here.

""" Customer objec in database"""
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True) #unique relaionship with a1uthentication model
    pay_id = models.CharField(max_length=200, null=True, blank=True)
    reward_points = models.IntegerField(default=0, null=False, blank=False)
    reward_points_activated = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
""" 
Overview:Create a customer profile after a user signs up
Type: Function
 """
def post_save_profile_create(sender, instance, created, *args, **kwargs):
    user_profile, created = Customer.objects.get_or_create(user=instance)

    if user_profile.pay_id is None or user_profile.pay_id == '':
        new_stripe_id = stripe.Customer.create(email='test@gmail.com') 
        user_profile.pay_id = new_stripe_id['id']
        user_profile.save()
post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)
