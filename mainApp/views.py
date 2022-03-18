from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from .models.UserProfile import Profile
from django.db import Error, transaction
from django.contrib.auth import authenticate, login
from .enums.consts import *
from django.contrib.auth.hashers import make_password, check_password
from .models.AppointmentRecord import AppointmentRecord


def index(request):
    return render(request, "index.html", {})


def index_login(request):
    account = request.POST['account']
    password = request.POST['password']
    user = authenticate(request, username=account, password=password)
    if user is not None:
        login(request, user)
        if request.user.is_authenticated:
            if request.user.profile.role == ROLE_PATIENT:
                return redirect("/patient_home/")
            elif request.user.profile.role == ROLE_DOCTOR:
                return redirect("/doctorHome/")
    else:
        # todo : 登录失败逻辑
        pass


def checkout_payment(request):
    return render(request, "checkout_payment.html", {})


def patient_checkout(request):
    if request.method == "POST":
        print(request.POST)
        return redirect("/checkout_payment")
    else:
        debug_data = {
            "debug_data": [
                {"med_id": 0, "medicine_name": "Synthroid ", "num": 3},
                {"med_id": 1, "medicine_name": "Crestor  ", "num": 4},
                {"med_id": 2, "medicine_name": "Ventolin  ", "num": 6}
            ]
        }
        return render(request, "patient_checkout.html", debug_data)


def register(request):
    # if this is a POST request we need to process the form data
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
                    # file = request.FILES["avatar"]
                    # avatar_path = f"{account}_avatar.{file.name.split('.')[1]}"
                    # with open(f"/media/avatars/{avatar_path}", "wb+") as f:
                    #     f.write(file)

                    user_profile = Profile(user=user, name=username, sex=sex, avatar=avatar,
                                           role=account_role)
                    user.save()
                    user_profile.save()
                    return redirect("/")

                # return JsonResponse({'Error': "error"})

    return render(request, "register.html", {})


def patient_home(request):
    return render(request, "patient_home.html", {})


def doctor(request):
    if request.method == "POST":
        print(request.body)
        return HttpResponseRedirect("")
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


def wait(request):
    return render(request, "wait.html", {})


def doctor_home(request):
    return render(request, "doctorHome.html", {})


def doctor_settlement(request):
    return render(request, "settlement.html", {})


def communication(request):
    return render(request, "communication.html", {})


def mediacl(request):
    return render(request, "medical.html", {})
