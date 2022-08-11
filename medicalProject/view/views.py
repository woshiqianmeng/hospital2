from django.shortcuts import render


def index(request):
    return render(request, "index.html", {})





def register(request):
    return render(request, "register.html", {})


def patition_home(request):
    return render(request, "patient_home.html", {})


def doctor(request):
    return render(request, "doctor.html", {})


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
