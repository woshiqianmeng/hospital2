from django.contrib import admin
from mainApp.models.UserProfile import Profile
from django_reverse_admin import ReverseModelAdmin


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'sex', 'role', 'doctor_rating')
    list_display_links = ['user']
    list_editable = ('name', 'sex', 'doctor_rating')


# Register your models here.注册
admin.site.register(Profile, CustomerAdmin)
