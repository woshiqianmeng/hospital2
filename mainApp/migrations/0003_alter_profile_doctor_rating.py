# Generated by Django 4.0.3 on 2022-03-17 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_appointmentrecord_profile_doctor_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='doctor_rating',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
