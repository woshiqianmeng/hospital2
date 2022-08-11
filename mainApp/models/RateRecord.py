from django.db import models


class RateRecord(models.Model):
    appoint_id = models.IntegerField()
    # doctor_id = models.IntegerField()
    doctor_name = models.CharField(max_length=50)
    rate = models.IntegerField()