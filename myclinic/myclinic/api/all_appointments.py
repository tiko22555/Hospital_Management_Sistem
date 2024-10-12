from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import  Doctor, Appointment
from datetime import datetime, timedelta

    
def all_appointments(request):
    if request.user.is_authenticated:
        doctor = get_object_or_404(Doctor, user = request.user)
        app_list = list(Appointment.objects.filter(doctor = doctor, schedule__gt = datetime.now()+ timedelta(hours=4)))
        return render(request, "clinic/appointments.html", {"app_list":app_list, "doctor":doctor})
    else:
        return redirect("login_")