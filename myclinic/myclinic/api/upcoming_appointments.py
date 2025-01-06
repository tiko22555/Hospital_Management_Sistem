from django.shortcuts import render, get_object_or_404
from ..clinic.models import  Doctor, Appointment
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

@login_required
def upcoming_appointments(request):
    """
    Returns all upcoming appointments for the logged-in doctor.
    """
    doctor = get_object_or_404(Doctor, user = request.user)
    app_list = list(Appointment.objects.filter(doctor = doctor, schedule__gt = datetime.now()+ timedelta(hours=4)))
    return render(request, "clinic/appointments.html", {"app_list":app_list, "doctor":doctor})