from django.contrib import admin
from mainApp.models.UserProfile import Profile
from mainApp.models.Medicine import Medicine
from mainApp.models.DoctorPrescription import DoctorPrescription
from mainApp.models.AppointmentRecord import AppointmentRecord
from mainApp.models.Condition import Condition
from mainApp.models.RateRecord import RateRecord
from mainApp.models.OrderRecord import OrderRecord
from mainApp.models.User import User
from django_reverse_admin import ReverseModelAdmin


class CustomerProfileAdmin(admin.ModelAdmin):
    # 添加搜索框模糊查询支持的字段
    search_fields = ['name']
    list_display = ('id', 'user','name', 'sex', 'role', 'doctor_rating','expiration_time','verification_code')
    list_display_links = ['user']
    list_editable = ('name', 'sex', 'doctor_rating')


class CustomMedicineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'img', 'price', 'supply_num')
    list_display_links = ['id']
    list_editable = ('name', 'img', 'price', 'supply_num')


admin.site.register(Profile, CustomerProfileAdmin)
admin.site.register(Medicine, CustomMedicineAdmin)
admin.site.register(DoctorPrescription)
admin.site.register(AppointmentRecord)
admin.site.register(Condition)
# admin.site.register(User)
admin.site.register(RateRecord)
admin.site.register(OrderRecord)
