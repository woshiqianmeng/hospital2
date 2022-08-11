from django.db import models
from django.conf import settings
from .Medicine import Medicine


class DoctorPrescription(models.Model):
    class META:
        unique_together = (('appointment_id', 'medicine_id'),)

    appoint_id = models.IntegerField()
    medicine_id = models.IntegerField()
    medicine_num = models.IntegerField()
