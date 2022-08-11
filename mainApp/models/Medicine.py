from django.db import models


class Medicine(models.Model):
    name = models.CharField(max_length=150)
    img = models.FileField(upload_to="medicine_img")
    price = models.IntegerField()
    supply_num = models.IntegerField()
