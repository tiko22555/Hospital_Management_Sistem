from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import Patient, Doctor, Appointment
from datetime import datetime


def profile(request):
    if request.user.is_authenticated:
        doctor = Doctor.objects.filter(user = request.user).first()
        patient = Patient.objects.filter(user = request.user).first()
        if doctor:
            return redirect("doctor_profile")
        elif patient:
            return redirect("patient_profile")
        else:
            return redirect("log_out")
    else:
        return redirect("login_")  


def doctor_profile(request):
    if request.user.is_authenticated:
        doctor = get_object_or_404(Doctor, user=request.user)

        if request.method == "POST":
            profile_picture = request.FILES['profile_picture']

            doctor.profile_picture = profile_picture
            doctor.save()
            return redirect('doctor_profile')


        return render(request, "clinic/doctor_profile.html", {"doctor": doctor})
    else:
        return redirect("login_")


    
def is_active(request):
    if request.user.is_authenticated:
        doctor = get_object_or_404(Doctor, user = request.user)
        if doctor.is_active:
            doctor.is_active = False
            doctor.save()
        else:
            doctor.is_active = True
            doctor.save()
        return redirect("doctor_profile")
    else:
        return redirect("login_")
    
def patient_profile(request):
    if request.user.is_authenticated:
        patient = get_object_or_404(Patient, user = request.user)
        app_list_past = Appointment.objects.filter(patient = patient, schedule__date__lte = datetime.now().date()).order_by("schedule")
        app_list = Appointment.objects.filter(patient = patient, schedule__date__gt = datetime.now().date()).order_by("schedule")
        return render(request, "clinic/patient_profile.html", {"patient":patient, "app_list":app_list, "app_list_past":app_list_past})
    else:
        return redirect("login_")
    
def delete_profile(request):
    if request.user.is_authenticated:
        patient = get_object_or_404(Patient, user = request.user)
        patient.is_deleted = True
        patient.save()
        return redirect("log_out")

    return redirect("login_")