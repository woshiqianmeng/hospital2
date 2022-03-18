from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    sex = models.IntegerField(choices=[(0, "MALE"), (1, "FEMALE")])
    avatar = models.FileField(upload_to='avatars')
    role = models.IntegerField(choices=[(0, "Doctor"), (1, "Patient")])
    doctor_rating = models.IntegerField(blank=True, default=None, null=True)



