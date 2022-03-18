from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('patient_home/', views.patient_home),
    path('doctor/', views.doctor),
    path("wait/", views.wait),
    path("doctorHome/", views.doctor_home),
    path("settlement/", views.doctor_settlement),
    path("communication/", views.communication),
    path("medical/", views.mediacl),
    path('admin/', admin.site.urls),
    path('login/', views.index_login),
    path('patient_checkout', views.patient_checkout),
    path('checkout_payment', views.checkout_payment)
]
