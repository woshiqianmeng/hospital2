from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=50)
    last_login = models.TimeField(auto_now=True)
    is_superuser = models.IntegerField(blank=True, default=None, null=True)
    username = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, default='')
    is_staff = models.BooleanField(default=False)
    is_active =  models.BooleanField(default=False)
    date_joined= models.TimeField(auto_now=True)
    first_name= models.CharField(max_length=30)