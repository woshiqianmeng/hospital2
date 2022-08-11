from django.db import models


class Condition(models.Model):
    name = models.CharField(max_length=150)
