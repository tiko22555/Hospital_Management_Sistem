from django.shortcuts import render, redirect, get_object_or_404
from ..clinic.models import Patient, Doctor
from datetime import datetime



def appointment_success(request):
    if request.user.is_authenticated:
        patient_id = request.GET.get('patient_id')
        patient = get_object_or_404(Patient, pk = patient_id)
        doctor_id = request.GET.get('doctor_id')
        doctor = get_object_or_404(Doctor, pk = doctor_id)
        time_str = request.GET.get('time')
        appointment_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M')
        return render(request, 'clinic/appointment_success.html', {"doctor":doctor, "patient":patient, 'appointment_time': appointment_time})
    else:
        return redirect("login_")