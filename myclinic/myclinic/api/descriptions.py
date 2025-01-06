from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import Patient, Doctor, Appointment
from django.contrib.auth.decorators import login_required

@login_required
def appointment_description(request, app_id):
    """
    Displays the details of an appointment for the logged-in patient.

    """
    patient = get_object_or_404(Patient, user = request.user)
    app = get_object_or_404(Appointment, pk = app_id, patient = patient)
    return render(request, "clinic/appointment_description.html", {"app":app})

@login_required
def appointment_description_edit(request, app_id):
    """
    Allows the logged-in doctor to edit the description of an appointment.

    """
    doctor = get_object_or_404(Doctor, user = request.user)
    app = get_object_or_404(Appointment, pk = app_id, doctor = doctor)
    if request.method == "GET":
        return render(request, "clinic/appointment_description_edit.html", {"app":app})
    else:
        desc = request.POST["description"]
        app.description = desc
        app.save()
        return redirect("doctor_profile")

@login_required
def doctor_description(request):
    """
    Allows the logged-in doctor to view or update their profile description.

    """
    doctor = get_object_or_404(Doctor, user = request.user)
    if request.method == "GET":
        return render(request, "clinic/doctor_description.html", {"doctor":doctor})
    else:
        desc = request.POST["description"]
        doctor.description = desc
        doctor.save()
        return redirect("doctor_profile")