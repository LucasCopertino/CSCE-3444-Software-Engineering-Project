from django.db import models

class user(models.Model):
    userName = models.CharField(default='abc', null=False, max_length=32)
    password = models.CharField(default='abc', null=False, max_length=128)
    def __str__(self):
        return self.userName
