from django.db import models
from django.contrib.auth.models import User


class AppointmentRecord(models.Model):
    patient_id = models.IntegerField()
    doctor_id = models.IntegerField()
