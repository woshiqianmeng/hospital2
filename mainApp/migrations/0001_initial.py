# Generated by Django 4.0.3 on 2022-03-16 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('sex', models.IntegerField(choices=[(0, 'MALE'), (1, 'FEMALE')])),
                ('avatar', models.FileField(upload_to='avatars')),
                ('role', models.IntegerField(choices=[(0, 'Doctor'), (1, 'Patient')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]