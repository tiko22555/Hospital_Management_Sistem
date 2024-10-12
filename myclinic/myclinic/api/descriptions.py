from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import Patient, Doctor, Appointment

def description(request, app_id):
    if request.user.is_authenticated:
        patient = get_object_or_404(Patient, user = request.user)
        app = get_object_or_404(Appointment, pk = app_id, patient = patient)
        return render(request, "clinic/description.html", {"app":app})
    else:
        return redirect("login_")

def description_edit(request, app_id):
    if request.user.is_authenticated:
        doctor = get_object_or_404(Doctor, user = request.user)
        app = get_object_or_404(Appointment, pk = app_id, doctor = doctor)
        if request.method == "GET":
            return render(request, "clinic/description_edit.html", {"app":app})
        else:
            desc = request.POST["description"]
            app.description = desc
            app.save()
            return redirect("doctor_profile")
    else:
        return redirect("login_")
def doctor_description(request):
    if request.user.is_authenticated:
        doctor = get_object_or_404(Doctor, user = request.user)
        if request.method == "GET":
            return render(request, "clinic/doctor_description.html", {"doctor":doctor})
        else:
            desc = request.POST["description"]
            doctor.description = desc
            doctor.save()
            return redirect("doctor_profile")
    return redirect("login_")