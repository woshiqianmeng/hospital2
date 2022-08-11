from django.urls import path, re_path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('patient_home', views.patient_home),
    path('doctor', views.doctor),
    re_path(r'^wait/(?P<appoint_id>\d+)$', views.wait, name="wait"),
    path("doctorHome", views.doctor_home),
    path('admin/', admin.site.urls),
    path('login', views.index_login),
    path('getlogin/email', views.fsyzm),
    re_path(r'patient_checkout/(?P<appoint_id>\d+)$', views.patient_checkout, name="patient_checkout"),
    path('checkout_payment', views.checkout_payment),
    re_path(r'^select_medicine/(?P<appoint_id>\d+)$', views.select_medicine, name="select_medicine"),
    re_path(r'getWaitingInfo/(?P<appoint_id>\d+)$', views.getWaitingInfo, name="getWaitingInfo"),
    re_path(r"^checkPrescription/(?P<appoint_id>\d+)$", views.checkIfPrescriptionAvailable, name="checkPrescription")
]
