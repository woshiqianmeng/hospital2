import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
from .models.UserProfile import Profile
from django.db import Error, transaction
from .enums.consts import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from .models.AppointmentRecord import AppointmentRecord
from .models.Medicine import Medicine
from .models.DoctorPrescription import DoctorPrescription
from .models.OrderRecord import OrderRecord
from .models.RateRecord import RateRecord
from .models.Condition import Condition
from .EmailScript import email
import json
import time

def index(request):
    return render(request, "index.html", {})


def index_login(request):
    account = request.POST['account']
    password = request.POST['password']
    verification_code = request.POST['verification_code']

    stamp = int(time.time())
    expiration_time =stamp
    user = authenticate(request, username=account, password=password)
    if user is not None:
        login(request, user)
        print(request.user.profile.verification_code,request.user.profile.expiration_time)
        if int(request.user.profile.expiration_time)>=expiration_time and request.user.profile.verification_code==verification_code:

            if request.user.is_authenticated:
                if request.user.profile.role == ROLE_PATIENT:
                    return redirect("/patient_home")
                elif request.user.profile.role == ROLE_DOCTOR:
                    return redirect("/doctorHome")
        else:
            return render(request, 'index.html', {'login_yzm': True})

    else:
        return render(request, 'index.html', {'login_fail': True})


def checkout_payment(request):
    return render(request, "checkout_payment.html", {})


from random import SystemRandom
def getrate_random():

    sr = SystemRandom()
    n = sr.choice(range(1000, 10000))
    pin = format(n, '04')
    return pin

# 发送验证码接口
def fsyzm(request):
    if request.method == "GET":
        account = request.GET['account']

        user = User.objects.filter(username=account).values('id','username')
        # db = RateRecord(appoint_id=appoint_id, doctor_id=doctor_id, rate=rate)
        print(account,user)
        if user is not None:
            print(user[0]['id'])
            profile = Profile.objects.get(user_id=user[0]['id'])
            profile.verification_code =getrate_random()
            stamp = int(time.time())
            profile.expiration_time = stamp+5*60
            print('我验证：', profile.verification_code, profile.expiration_time)
            profile.save()
        email.demo2(account,profile.verification_code)
        return HttpResponse('ok')


def patient_checkout(request, appoint_id):
    if request.method == "POST":
        med_ids = request.POST.getlist("checked_med_id")
        med_nums = request.POST.getlist("num")
        rate = request.POST.get("rate")
        address = request.POST.get("address")
        try:
            with transaction.atomic():
                for idx in range(len(med_ids)):
                    db = OrderRecord(appoint_id=appoint_id, medicine_id=med_ids[idx],
                                     order_num=med_nums[idx], address=address)
                    db.save()
                print(Profile.objects.get(id=appoint_id),appoint_id)
                doctor_name = Profile.objects.get(id=appoint_id).name
                db = RateRecord(appoint_id=appoint_id, doctor_name=doctor_name, rate=rate)
                db.save()
                return redirect("/checkout_payment")
        except Error:
            return HttpResponseBadRequest()
    else:
        ps = list(DoctorPrescription.objects.filter(appoint_id=appoint_id))
        objs = []
        for p in ps:
            if p.medicine_num != 0:
                medicine = Medicine.objects.filter(id=p.medicine_id)[0]
                p.medicine = medicine
                objs.append(p)
        return render(request, "patient_checkout.html", {"ps": objs, "appoint_id": appoint_id})


def register(request):
    if request.method == 'POST':
        account = request.POST.get("account")
        username = request.POST.get("name")
        password = request.POST.get("password")
        sex = int(request.POST.get("sex", "-1"))
        avatar = request.FILES["avatar"]
        account_role = int(request.POST.get("role", "-1"))

        if request.POST.get("account") and request.POST.get("password"):
            with transaction.atomic():
                user = User.objects.create_user(username=account, password=password)

                if request.FILES["avatar"]:
                    user_profile = Profile(user=user, name=username, sex=sex, avatar=avatar,
                                           role=account_role)
                    user.save()
                    user_profile.save()
                    return redirect("/")


    return render(request, "register.html", {})


def patient_home(request):
    if request.method == "POST":
        conditions = ",".join(request.POST.getlist("condition"))
        patient_des = request.POST["description"]
        request.session["condition"] = conditions
        request.session["patient_des"] = patient_des
        return redirect("/doctor")
    elif request.method == "GET":
        db = list(Condition.objects.all())
        return render(request, "patient_home.html", {"conditions": db})


def doctor(request):
    if request.method == "POST":
        if request.body:
            decoded_body = request.body.decode('utf-8')
            json_body = json.loads(decoded_body)
            doc_id = json_body.get("selectedDoc")
            if doc_id:
                patient_id = request.user.id
                db = AppointmentRecord(doctor_id=doc_id,
                                       patient_id=patient_id,
                                       condition=request.session["condition"],
                                       patient_description=request.session["patient_des"])
                db.save()
                request.session["appointment_id"] = db.id
                return JsonResponse({"success": 1, "appoint_id": db.id})
        return JsonResponse({"success": 0})
    else:
        doctors = Profile.objects.filter(role=0).order_by("-doctor_rating")[:10]
        doctors = list(doctors)
        for doc in doctors:
            if doc.doctor_rating:
                doc.rate_loop = list(range(doc.doctor_rating))
            else:
                doc.rate_loop = []
        print(doctors)
    return render(request, "doctor.html", {"doctor_profiles": doctors})


def wait(request, appoint_id):
    return render(request, "wait.html", {"appoint_id": appoint_id})


def doctor_home(request):
    if request.method == "GET":
        current_user = request.user
        appoint_record = AppointmentRecord.objects.filter(doctor_id=current_user.id,
                                                          handled=False).order_by(
            "timestamp")
        appoint_record = list(appoint_record)
        patient_info = []
        for record in appoint_record:
            obj = User.objects.filter(id=record.patient_id)[0]
            obj.appoint_id = record.id
            obj.patient_description = record.patient_description
            obj.conditions = record.condition
            patient_info.append(obj)

        return render(request, "doctorHome.html", {"appoint_objs": patient_info})
    elif request.method == "POST":
        pass


def select_medicine(request, appoint_id):
    if request.method == "GET":
        medicines = list(Medicine.objects.filter())
        record = AppointmentRecord.objects.filter(id=appoint_id)[0]
        conditions = record.condition
        patient_des = record.patient_description
        return render(request,
                      "select_medicine.html",
                      {"medicines": medicines,
                       "conditions": conditions,
                       "description": patient_des,
                       "appoint_id": appoint_id})
    elif request.method == "POST":
        med_ids = request.POST.getlist("med_id")
        med_nums = request.POST.getlist("num")
        appoint_id = int(appoint_id)
        if med_ids and med_nums and appoint_id is not None and len(med_ids) == len(med_nums):
            with transaction.atomic():
                for idx in range(len(med_ids)):
                    if med_nums[idx] != 0:
                        med_id = int(med_ids[idx])
                        med_num = int(med_nums[idx])
                        db = DoctorPrescription(appoint_id=appoint_id,
                                                medicine_id=med_id,
                                                medicine_num=med_num)
                        db.save()
                    else:
                        continue
                record = AppointmentRecord.objects.filter(id=appoint_id)[0]
                record.handled = True
                record.save()
                return redirect('/doctorHome')
        else:
            return HttpResponseBadRequest()



def getWaitingInfo(request, appoint_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            appointment_id = appoint_id
            appointment_record = AppointmentRecord.objects.filter(id=appointment_id).first()
            if appointment_record:
                app_doc_id = appointment_record.doctor_id
                app_time = appointment_record.timestamp
                record = AppointmentRecord.objects.filter(doctor_id=app_doc_id, handled=False)
                record = record.filter(timestamp__lt=app_time)
                record = list(record)
                return JsonResponse({"queue_length": len(record)})
            else:
                return JsonResponse({"queue_length": 0})


def checkIfPrescriptionAvailable(request, appoint_id):
    if request.method == "GET":
        record = DoctorPrescription.objects.filter(appoint_id=appoint_id)[0]
        if record:
            return JsonResponse({"success": 1})
        else:
            return JsonResponse({"success": 0, "msg": "Not found"})
