from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class AppointmentRecord(models.Model):
    patient_id = models.IntegerField()
    doctor_id = models.IntegerField()
    timestamp = models.TimeField(auto_now=True)
    condition = models.CharField(max_length=50, default=None, null=True)
    patient_description = models.TextField(null=True, default=None)
    handled = models.BooleanField(default=False)
